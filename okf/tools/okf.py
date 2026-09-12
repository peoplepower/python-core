#!/usr/bin/env python3
"""okf.py — dependency-free tooling for Open Knowledge Format (OKF) v0.2 bundles.

Subcommands:
  validate  [BUNDLE_DIR]  Check conformance per SPEC.md §11. Exit 1 on errors.
  index     [BUNDLE_DIR]  Generate index.md files for progressive disclosure (§8).
  viz       [BUNDLE_DIR]  Generate a self-contained HTML visualization of the
                          bundle: knowledge graph plus health/coverage views.
  freshness [BUNDLE_DIR]  Score every concept 0-100 for staleness from git
                          history, 'generated.at', 'stale_after' (§5.5), and
                          the declared 'sources' (§5.1).

Frontmatter is parsed with a minimal YAML-subset parser (scalars, flow lists,
flow maps, block lists of scalars/maps, nested block maps) so the tool has
zero dependencies. Anything a full YAML parser would accept but this one
can't is reported as a parse error — keep frontmatter simple, per the spirit
of the spec.
"""

import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

RESERVED = {"index.md", "log.md"}
# Non-concept documentation the tool tolerates at any level (the spec itself,
# a repo README). They are excluded from validation, indexing, and the graph.
SKIP_FILES = {"SPEC.md", "README.md"}
SKIP_DIRS = {".git", ".claude", "node_modules", "__pycache__", "tools"}

OKF_VERSION = "0.2"
STATUS_VALUES = {"draft", "stable", "deprecated"}


# ---------------------------------------------------------------- frontmatter

class FrontmatterError(Exception):
    pass


def split_frontmatter(text):
    """Return (frontmatter_lines, body) or raise FrontmatterError."""
    if not text.startswith("---\n") and text.strip() != "---":
        raise FrontmatterError("file does not start with a '---' frontmatter delimiter")
    lines = text.split("\n")
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    raise FrontmatterError("frontmatter block is never closed with '---'")


KEY_RE = re.compile(r"^([A-Za-z0-9_.-]+):(.*)$")


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def _split_flow(inner):
    """Split flow-collection innards on top-level commas, respecting quotes
    and nested brackets."""
    parts, buf, depth, quote = [], [], 0, None
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch in "[{":
            depth += 1
            buf.append(ch)
        elif ch in "]}":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf)
    if tail.strip():
        parts.append(tail)
    return [p.strip() for p in parts]


def _parse_value(text):
    """Parse a scalar, flow list '[...]', or flow map '{...}'."""
    text = text.strip()
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [_parse_value(p) for p in _split_flow(inner)] if inner else []
    if text.startswith("{") and text.endswith("}"):
        inner = text[1:-1].strip()
        out = {}
        for part in _split_flow(inner):
            if ":" not in part:
                raise FrontmatterError(f"cannot parse flow-map entry: {part!r}")
            k, v = part.split(":", 1)
            out[k.strip()] = _parse_value(v)
        return out
    return _unquote(text)


def _prepare_lines(raw_lines):
    """[(indent, content)] with blank and comment-only lines removed."""
    out = []
    for raw in raw_lines:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        stripped = raw.lstrip(" ")
        if "\t" in raw[:len(raw) - len(raw.lstrip())]:
            raise FrontmatterError("tabs are not allowed in frontmatter indentation")
        out.append((len(raw) - len(stripped), stripped.rstrip()))
    return out


def _parse_map(lines, i, indent):
    data = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
        _, text = lines[i]
        m = KEY_RE.match(text)
        if not m:
            raise FrontmatterError(f"cannot parse line: {text!r}")
        key, rest = m.group(1), m.group(2).strip()
        i += 1
        if rest and not rest.startswith("#"):
            data[key] = _parse_value(rest)
        elif i < len(lines) and lines[i][0] > indent:
            child_indent = lines[i][0]
            if lines[i][1].startswith("- "):
                data[key], i = _parse_list(lines, i, child_indent)
            else:
                data[key], i = _parse_map(lines, i, child_indent)
        else:
            data[key] = ""
    return data, i


def _parse_list(lines, i, indent):
    items = []
    while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
        head = lines[i][1][2:].strip()
        i += 1
        m = KEY_RE.match(head)
        if m and not head.startswith(("{", "[")):
            # A block-map list item: first key on the dash line, further keys
            # on the following, deeper-indented lines.
            entry = {}
            key, rest = m.group(1), m.group(2).strip()
            if not rest:
                raise FrontmatterError(
                    f"nested block values inside list items are not supported: {head!r}")
            entry[key] = _parse_value(rest)
            while i < len(lines) and lines[i][0] > indent:
                m2 = KEY_RE.match(lines[i][1])
                if not m2:
                    raise FrontmatterError(
                        f"cannot parse list-item line: {lines[i][1]!r}")
                rest2 = m2.group(2).strip()
                if not rest2:
                    raise FrontmatterError(
                        f"nested block values inside list items are not supported: {lines[i][1]!r}")
                entry[m2.group(1)] = _parse_value(rest2)
                i += 1
            items.append(entry)
        else:
            items.append(_parse_value(head))
    return items, i


def parse_frontmatter(raw_lines):
    """Parse the YAML subset OKF uses. Returns a dict."""
    lines = _prepare_lines(raw_lines)
    data, i = _parse_map(lines, 0, 0)
    if i != len(lines):
        raise FrontmatterError(f"unexpected indentation: {lines[i][1]!r}")
    return data


def read_doc(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm_lines, body = split_frontmatter(text)
    return parse_frontmatter(fm_lines), body


# --------------------------------------------------------- v0.2 field helpers

def normalized_verified(fm):
    """'verified' as a list of {by, at} dicts; a bare mapping is a
    one-element list (§5.2)."""
    v = fm.get("verified")
    if isinstance(v, dict):
        return [v]
    if isinstance(v, list):
        return [e for e in v if isinstance(e, dict)]
    return []


def trust_tier(fm):
    """unverified | machine-confirmed | human-reviewed (§5.3)."""
    entries = normalized_verified(fm)
    if not entries:
        return "unverified"
    if any(str(e.get("by", "")).startswith("human:") for e in entries):
        return "human-reviewed"
    return "machine-confirmed"


def generated_at(fm):
    """The concept's last-meaningful-change timestamp: generated.at, falling
    back to the v0.1 legacy 'timestamp' (§13.1)."""
    gen = fm.get("generated")
    if isinstance(gen, dict) and isinstance(gen.get("at"), str):
        return gen["at"]
    ts = fm.get("timestamp")
    return ts if isinstance(ts, str) else None


def source_entries(fm):
    """'sources' as (dict_entries, legacy_string_entries)."""
    src = fm.get("sources")
    if isinstance(src, str):
        src = [src] if src else []
    elif not isinstance(src, list):
        src = []
    dicts = [e for e in src if isinstance(e, dict)]
    strings = [e for e in src if isinstance(e, str) and e]
    return dicts, strings


# ------------------------------------------------------------------ discovery

def walk_bundle(root):
    """Yield (dirpath, subdirs, md_files) for every directory, skipping
    SKIP_DIRS and SKIP_FILES."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        md = sorted(f for f in filenames if f.endswith(".md") and f not in SKIP_FILES)
        yield dirpath, list(dirnames), md


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FOOTNOTE_USE_RE = re.compile(r"\[\^([^\]\s]+)\](?!:)")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISO_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?)?$")
# §5: every timestamp-valued key is a datetime with an explicit UTC offset;
# consumers MUST ignore date-only or offset-less values (§11).
ISO_TS_STRICT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})$")
SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
BUNDLE_LINK_RE = re.compile(r"^bundle://([A-Za-z0-9._-]+)/(.+)$")

# Cross-bundle links use bundle://<name>/<path>, resolved through a registry:
# a concept file whose frontmatter carries a 'bundles' list of
# { name, path, remote?, description? } entries. $OKF_REGISTRY overrides the
# default location. Inside a bundle, plain relative/bundle-relative links
# remain the norm — only links that cross a bundle boundary are qualified.
REGISTRY_DEFAULT = os.path.expanduser("~/.okf/registry.md")
_REGISTRY_CACHE = None


def load_registry():
    """Return {name: absolute-bundle-root} from the registry, or {} if absent."""
    global _REGISTRY_CACHE
    if _REGISTRY_CACHE is not None:
        return _REGISTRY_CACHE
    reg_path = os.environ.get("OKF_REGISTRY", REGISTRY_DEFAULT)
    bundles = {}
    if os.path.exists(reg_path):
        try:
            fm, _ = read_doc(reg_path)
        except (FrontmatterError, OSError):
            fm = {}
        for entry in fm.get("bundles") or []:
            if isinstance(entry, dict) and entry.get("name") and entry.get("path"):
                bundles[entry["name"]] = os.path.expanduser(entry["path"])
    _REGISTRY_CACHE = bundles
    return bundles


def resolve_path(root, from_path, target):
    """Resolve a path-valued field (§6.2) to an existing local file, or None.

    Bundle-relative '/x' resolves against the bundle root; as a leniency, an
    absolute path that exists on this filesystem is also accepted.
    """
    if target.startswith("/"):
        cand = os.path.join(root, target.lstrip("/"))
        if os.path.exists(cand):
            return cand
        return target if os.path.exists(target) else None
    cand = os.path.normpath(os.path.join(os.path.dirname(from_path), target))
    return cand if os.path.exists(cand) else None


# ------------------------------------------------------------------- validate

class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, path, msg):
        self.errors.append((path, msg))

    def warn(self, path, msg):
        self.warnings.append((path, msg))


def extract_links(root, path, body):
    """Return [{"raw", "resolved", "broken"}] for every bundle link in body.

    "resolved" is the bundle-relative posix path of the target (None when the
    target does not exist), so it can be matched against concept ids.
    """
    # Links inside fenced code blocks or inline code are examples, not claims.
    body = re.sub(r"^(```|~~~).*?^\1\s*$", "", body, flags=re.M | re.S)
    body = re.sub(r"`[^`\n]*`", "", body)
    links = []
    for target in LINK_RE.findall(body):
        bm = BUNDLE_LINK_RE.match(target)
        if bm:
            name, sub = bm.group(1), bm.group(2).split("#")[0]
            other_root = load_registry().get(name)
            if other_root is None:
                links.append({"raw": target, "resolved": None, "broken": True,
                              "bundle": name, "bundle_unknown": True})
                continue
            cand = os.path.join(other_root, sub)
            # Links may address the concept id (path minus .md) or the file.
            exists = os.path.exists(cand) or os.path.exists(cand + ".md")
            links.append({"raw": target, "resolved": None, "broken": not exists,
                          "bundle": name})
            continue
        if SCHEME_RE.match(target) or target.startswith("#"):
            continue  # external URL or in-page anchor
        target = target.split("#")[0]
        if not target:
            continue
        if target.startswith("/"):
            resolved = os.path.join(root, target.lstrip("/"))
        else:
            resolved = os.path.join(os.path.dirname(path), target)
        broken = not os.path.exists(resolved)
        rel = None
        if not broken:
            rel = os.path.relpath(os.path.normpath(resolved), root).replace(os.sep, "/")
        links.append({"raw": target, "resolved": rel, "broken": broken})
    return links


def check_links(root, path, body, report):
    for link in extract_links(root, path, body):
        if link.get("bundle_unknown"):
            report.warn(path, f"bundle:// link to a bundle not in the registry "
                              f"(tolerated): {link['raw']}")
        elif link["broken"] and link.get("bundle"):
            report.warn(path, f"broken cross-bundle link (tolerated): {link['raw']}")
        elif link["broken"]:
            report.warn(path, f"broken link (tolerated by spec): {link['raw']}")


def _check_ts(report, path, label, value):
    if not isinstance(value, str) or not value:
        return
    if not ISO_TS_RE.match(value):
        report.warn(path, f"'{label}' is not ISO 8601: {value!r}")
    elif not ISO_TS_STRICT_RE.match(value):
        report.warn(path, f"'{label}' has no time and explicit UTC offset, so conformant consumers ignore it (§5, §11): {value!r}")


REPO_SLUG_RE = re.compile(r"^[^/\s:]+/[^/\s:]+:\S")


def _looks_like_path(res):
    """Heuristic: is a sources[].resource a followable path, as opposed to a
    URL, an <org>/<repo>:<path> slug, or a population/scope descriptor (§5.1)?
    Slugs resolve against local checkouts and are 'freshness' concerns, not
    validate's — warning on them here would flood bundles that document code."""
    if SCHEME_RE.match(res) or REPO_SLUG_RE.match(res):
        return False
    return res.startswith(("/", "./", "../")) or ("/" in res and " " not in res)


def validate_trust_fields(root, path, fm, report):
    """The provenance, trust, and lifecycle families (§5)."""
    if "timestamp" in fm:
        report.warn(path, "'timestamp' is a v0.1 legacy field; use generated.at (§13.1)")
        _check_ts(report, path, "timestamp", fm.get("timestamp"))

    gen = fm.get("generated")
    if gen is not None and gen != "":
        if not isinstance(gen, dict):
            report.warn(path, "'generated' should be a { by, at } mapping (§5.2)")
        else:
            if not gen.get("by"):
                report.warn(path, "'generated' has no 'by' actor (§5.2)")
            _check_ts(report, path, "generated.at", gen.get("at"))

    v = fm.get("verified")
    if v is not None and v != "":
        entries = normalized_verified(fm)
        if not entries:
            report.warn(path, "'verified' should be a { by, at } mapping or a list of them (§5.2)")
        for e in entries:
            if not e.get("by"):
                report.warn(path, "a 'verified' entry has no 'by' actor (§5.2)")
            _check_ts(report, path, "verified[].at", e.get("at"))

    status = fm.get("status")
    if isinstance(status, str) and status and status not in STATUS_VALUES:
        report.warn(path, f"'status' is not one of draft|stable|deprecated: {status!r} (§5.4)")

    _check_ts(report, path, "stale_after", fm.get("stale_after"))

    uw = fm.get("usage_window")
    if isinstance(uw, dict):
        _check_ts(report, path, "usage_window.from", uw.get("from"))
        _check_ts(report, path, "usage_window.to", uw.get("to"))

    dict_sources, _legacy = source_entries(fm)
    if "sources" in fm and not isinstance(fm.get("sources"), (list, str)):
        report.warn(path, "'sources' should be a list (§5.1)")
    for entry in dict_sources:
        res = entry.get("resource")
        if not res:
            report.warn(path, "a 'sources' entry has no 'resource' (§5.1)")
            continue
        _check_ts(report, path, "sources[].last_modified", entry.get("last_modified"))
        if isinstance(res, str) and _looks_like_path(res) \
                and resolve_path(root, path, res) is None:
            report.warn(path, f"source resource path not found (tolerated): {res}")


def validate_footnotes(path, fm, body, report):
    """Footnote labels are join keys into sources[].id (§5.1)."""
    dict_sources, _ = source_entries(fm)
    ids = {e.get("id") for e in dict_sources if e.get("id")}
    if not ids:
        return
    for label in set(FOOTNOTE_USE_RE.findall(body)):
        if label not in ids:
            report.warn(path, f"footnote [^{label}] matches no sources[].id (§5.1)")


def validate_computation(root, path, fm, body, report):
    """Attested Computation contract fields (§10)."""
    if not fm.get("runtime"):
        report.error(path, "Attested Computation requires 'runtime' (§10.2)")

    params = fm.get("parameters")
    if params is not None and params != "":
        if not isinstance(params, list):
            report.warn(path, "'parameters' should be a list of { name, type, required } (§10.2)")
        else:
            for p in params:
                if not isinstance(p, dict) or not p.get("name"):
                    report.warn(path, f"a 'parameters' entry has no 'name': {p!r} (§10.2)")

    comp = fm.get("computation")
    if isinstance(comp, str) and comp:
        if resolve_path(root, path, comp) is None:
            report.warn(path, f"'computation' path not found (tolerated): {comp}")
    elif not re.search(r"^#\s+Computation\s*$", body, re.M):
        report.warn(path, "no 'computation' path and no '# Computation' body section (§10.3)")

    for field in ("executor", "attester"):
        block = fm.get(field)
        if block is None or block == "":
            report.warn(path, f"no '{field}' declared (§10.2)")
            continue
        if not isinstance(block, dict) or not block.get("resource"):
            report.warn(path, f"'{field}' has no 'resource' (§10.2)")
    att = fm.get("attester")
    if isinstance(att, dict) and isinstance(att.get("resource"), str) \
            and _looks_like_path(att["resource"]) \
            and resolve_path(root, path, att["resource"]) is None:
        report.warn(path, f"'attester.resource' path not found (tolerated): {att['resource']}")


def validate_concept(root, path, report):
    try:
        fm, body = read_doc(path)
    except FrontmatterError as e:
        report.error(path, f"frontmatter: {e}")
        return
    type_val = fm.get("type")
    if not isinstance(type_val, str) or not type_val.strip():
        report.error(path, "missing or empty required 'type' field")
    if "description" not in fm:
        report.warn(path, "no 'description' — index entries and previews will be empty")
    tags = fm.get("tags")
    if tags is not None and not isinstance(tags, list):
        report.warn(path, "'tags' should be a YAML list")
    validate_trust_fields(root, path, fm, report)
    validate_footnotes(path, fm, body, report)
    if isinstance(type_val, str) and type_val.strip() == "Attested Computation":
        validate_computation(root, path, fm, body, report)
    check_links(root, path, body, report)


def validate_index(root, path, report):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    is_root = os.path.dirname(os.path.abspath(path)) == os.path.abspath(root)
    body = text
    if text.startswith("---"):
        if not is_root:
            report.error(path, "frontmatter is only permitted in the bundle-root index.md (§12)")
        try:
            fm_lines, body = split_frontmatter(text)
            fm = parse_frontmatter(fm_lines)
            if is_root and "okf_version" not in fm:
                report.warn(path, "root index frontmatter present but no 'okf_version' declared")
        except FrontmatterError as e:
            report.error(path, f"frontmatter: {e}")
            return
    if not re.search(r"^\s*[*-] \[[^\]]+\]\([^)]+\)", body, re.M):
        report.warn(path, "index has no '* [Title](url) - description' entries (§8)")
    check_links(root, path, body, report)


def validate_log(root, path, report):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if text.startswith("---"):
        report.error(path, "log.md must not contain frontmatter")
        return
    dates = re.findall(r"^## +(.+?)\s*$", text, re.M)
    if not dates:
        report.warn(path, "log has no '## YYYY-MM-DD' date headings (§9)")
    for d in dates:
        if not ISO_DATE_RE.match(d):
            report.error(path, f"log date heading is not ISO 8601 YYYY-MM-DD: {d!r}")
    check_links(root, path, text, report)


def run_validation(root):
    """Validate every file in the bundle. Returns (Report, concept count)."""
    report = Report()
    n_concepts = 0
    for dirpath, _dirs, md_files in walk_bundle(root):
        for name in md_files:
            path = os.path.join(dirpath, name)
            if name == "index.md":
                validate_index(root, path, report)
            elif name == "log.md":
                validate_log(root, path, report)
            else:
                n_concepts += 1
                validate_concept(root, path, report)
    return report, n_concepts


def cmd_validate(root):
    report, n_concepts = run_validation(root)

    rel = lambda p: os.path.relpath(p, root)
    for path, msg in report.errors:
        print(f"ERROR   {rel(path)}: {msg}")
    for path, msg in report.warnings:
        print(f"warning {rel(path)}: {msg}")
    status = "FAIL" if report.errors else "OK"
    print(f"{status}: {n_concepts} concept(s), "
          f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 1 if report.errors else 0


# ---------------------------------------------------------------------- index

def concept_meta(path):
    """Best-effort (title, description, type) for an index entry."""
    stem = os.path.splitext(os.path.basename(path))[0]
    try:
        fm, _ = read_doc(path)
    except (FrontmatterError, OSError):
        return stem, "", "Concept"
    title = fm.get("title") or stem
    desc = fm.get("description") or ""
    ctype = fm.get("type") if isinstance(fm.get("type"), str) and fm.get("type") else "Concept"
    return str(title), str(desc), str(ctype)


def dir_has_content(dirpath):
    for _, _, md_files in walk_bundle(dirpath):
        if any(f not in RESERVED for f in md_files):
            return True
    return False


def build_index(root, dirpath, subdirs, md_files):
    is_root = os.path.abspath(dirpath) == os.path.abspath(root)
    concepts = [f for f in md_files if f not in RESERVED]

    by_type = {}
    for name in concepts:
        title, desc, ctype = concept_meta(os.path.join(dirpath, name))
        by_type.setdefault(ctype, []).append((title, name, desc))

    lines = []
    if is_root:
        lines += ["---", f'okf_version: "{OKF_VERSION}"', "---", ""]
    for ctype in sorted(by_type):
        lines.append(f"# {ctype}")
        lines.append("")
        for title, name, desc in sorted(by_type[ctype]):
            suffix = f" - {desc}" if desc else ""
            lines.append(f"* [{title}]({name}){suffix}")
        lines.append("")
    content_dirs = [d for d in subdirs if dir_has_content(os.path.join(dirpath, d))]
    if content_dirs:
        lines.append("# Directories")
        lines.append("")
        for d in content_dirs:
            lines.append(f"* [{d}]({d}/) - see [{d}/index.md]({d}/index.md)")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _index_is_hand_authored(path):
    """A root index whose frontmatter carries more than okf_version is
    hand-authored; regenerating it would destroy content."""
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if not text.startswith("---"):
            return False
        fm = parse_frontmatter(split_frontmatter(text)[0])
        return bool(set(fm) - {"okf_version"})
    except (FrontmatterError, OSError):
        return False


def cmd_index(root):
    written = 0
    for dirpath, subdirs, md_files in walk_bundle(root):
        is_root = os.path.abspath(dirpath) == os.path.abspath(root)
        concepts = [f for f in md_files if f not in RESERVED]
        content_dirs = [d for d in subdirs if dir_has_content(os.path.join(dirpath, d))]
        if not concepts and not content_dirs:
            continue
        if not is_root and not dir_has_content(dirpath):
            continue
        target = os.path.join(dirpath, "index.md")
        if os.path.exists(target) and _index_is_hand_authored(target):
            print(f"skip  {os.path.relpath(target, root)} (hand-authored frontmatter)")
            continue
        out = build_index(root, dirpath, subdirs, md_files)
        old = None
        if os.path.exists(target):
            with open(target, encoding="utf-8") as f:
                old = f.read()
        if old != out:
            with open(target, "w", encoding="utf-8") as f:
                f.write(out)
            written += 1
            print(f"wrote {os.path.relpath(target, root)}")
    print(f"done: {written} index file(s) updated")
    return 0


# ------------------------------------------------------------------ freshness
#
# Scoring model (after https://dosu.dev/blog/score-documentation-freshness-in-ci):
#   age penalty   — how much longer ago the concept was touched than the
#                   sources it derives from: (doc_age - source_age) / 3, cap 30
#   shelf penalty — days past 'stale_after' (§5.5) ×2, cap 30; concepts with
#                   no stale_after fall back to a default 365-day shelf life
#                   (legacy 'ttl_days' is honored)
#   drift penalty — each declared source path that no longer exists: 10, cap 40
#   score = max(0, 100 - penalties);  fresh ≥ 65 > review ≥ 35 > stale
# A concept past its 'stale_after' is stale by definition (§5.5) and is
# banded 'stale' regardless of score.
#
# The concept's own age comes from the bundle's git history, falling back to
# 'generated.at' (§5.2), the legacy 'timestamp', then file mtime. Source
# recency comes from each source's 'last_modified' signal (§5.1) and, for
# path-valued resources that exist locally, the file's own git/mtime age.
#
# Legacy v0.1 string sources of the form '<org>/<repo>:<path>' are still
# honored: the repo is located by scanning --repos-root (default: the
# bundle's parent directory) for git checkouts whose 'origin' remote matches
# the slug. A repo that is not checked out here makes its sources
# unverifiable, which is not the same as drift.

DEFAULT_TTL_DAYS = 365
FRESH_MIN = 65   # score >= FRESH_MIN  -> "fresh"
REVIEW_MIN = 35  # score >= REVIEW_MIN -> "review", below -> "stale"


def _slug_from_remote_url(url):
    """'https://github.com/org/repo.git' / 'git@host:org/repo' -> 'org/repo'."""
    url = url.strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    parts = [p for p in re.split(r"[/:]", url) if p]
    return "/".join(parts[-2:]).lower() if len(parts) >= 2 else None


def _discover_repos(repos_root, max_depth=4):
    """Scan repos_root for git checkouts: 'org/repo' slug -> local path."""
    repos = {}
    base_depth = repos_root.rstrip(os.sep).count(os.sep)
    for dirpath, dirnames, _files in os.walk(repos_root):
        if dirpath.count(os.sep) - base_depth >= max_depth:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames
                       if not d.startswith(".") and d not in ("node_modules", "__pycache__")]
        if not os.path.isdir(os.path.join(dirpath, ".git")):
            continue
        dirnames[:] = []  # do not descend into a checkout
        try:
            out = subprocess.run(["git", "-C", dirpath, "remote", "get-url", "origin"],
                                 capture_output=True, text=True, timeout=15)
            slug = _slug_from_remote_url(out.stdout) if out.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            slug = None
        if slug:
            repos.setdefault(slug, dirpath)
    return repos


def _git_last_epoch(repo, rel_path):
    """Epoch of the last commit touching rel_path, or None."""
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "-1", "--format=%ct", "--", rel_path],
            capture_output=True, text=True, timeout=30)
        s = out.stdout.strip()
        return int(s) if s else None
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def _bundle_commit_times(root):
    """One git pass over the bundle: rel path -> epoch of last commit."""
    times = {}
    try:
        out = subprocess.run(["git", "-C", root, "log", "--format=@%ct", "--name-only"],
                             capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return times
    epoch = None
    for line in out.stdout.splitlines():
        if line.startswith("@"):
            try:
                epoch = int(line[1:])
            except ValueError:
                epoch = None
        elif line.strip() and epoch is not None:
            times.setdefault(line.strip(), epoch)
    return times


def _parse_ts_epoch(ts):
    if not isinstance(ts, str) or not ISO_TS_RE.match(ts):
        return None
    try:
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00").replace(" ", "T"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.timestamp()


def _score_legacy_source(src, repo_map, missing, unresolved, source_epochs):
    """A v0.1 '<org>/<repo>:<path>' string source."""
    slug, _, sub = src.partition(":")
    repo_dir = repo_map.get(slug.strip().lower())
    if repo_dir is None:
        unresolved.append(src)
        return
    full = os.path.normpath(os.path.join(repo_dir, sub)) if sub else repo_dir
    matches = sorted(glob.glob(full)) if re.search(r"[*?\[]", sub) \
        else ([full] if os.path.exists(full) else [])
    if not matches:
        missing.append(src)
        return
    for m in matches:
        epoch = _git_last_epoch(repo_dir, os.path.relpath(m, repo_dir))
        source_epochs.append(epoch or os.path.getmtime(m))


def _score_v2_source(root, path, entry, missing, unresolved, source_epochs):
    """A v0.2 structured sources entry (§5.1)."""
    lm_epoch = _parse_ts_epoch(entry.get("last_modified"))
    if lm_epoch is not None:
        source_epochs.append(lm_epoch)
    res = entry.get("resource")
    if not isinstance(res, str) or not res:
        return
    if not _looks_like_path(res):
        # URL or scope descriptor: last_modified is the only usable signal.
        if lm_epoch is None:
            unresolved.append(res)
        return
    resolved = resolve_path(root, path, res)
    if resolved is None:
        missing.append(res)
        return
    if lm_epoch is None:
        rel = os.path.relpath(resolved, root)
        epoch = None
        if not rel.startswith(".."):
            epoch = _git_last_epoch(root, rel.replace(os.sep, "/"))
        try:
            source_epochs.append(epoch or os.path.getmtime(resolved))
        except OSError:
            pass


def compute_freshness(root, repos_root=None):
    """Score every concept. Returns rows sorted worst-first."""
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    repos_root = os.path.abspath(repos_root or os.path.join(root, os.pardir))
    bundle_times = _bundle_commit_times(root)
    repo_map = None  # discovered lazily, only if legacy string sources exist
    rows = []
    for dirpath, _dirs, md_files in walk_bundle(root):
        for name in md_files:
            if name in RESERVED:
                continue
            path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(path, root).replace(os.sep, "/")
            try:
                fm, _ = read_doc(path)
            except (FrontmatterError, OSError):
                fm = {}

            doc_epoch = (bundle_times.get(rel_path)
                         or _parse_ts_epoch(generated_at(fm))
                         or os.path.getmtime(path))
            doc_days = max(0.0, (now - doc_epoch) / 86400)

            dict_sources, legacy_sources = source_entries(fm)
            missing, unresolved, source_epochs = [], [], []
            for entry in dict_sources:
                _score_v2_source(root, path, entry, missing, unresolved, source_epochs)
            if legacy_sources and repo_map is None:
                repo_map = _discover_repos(repos_root)
            for src in legacy_sources:
                _score_legacy_source(src, repo_map or {}, missing, unresolved, source_epochs)

            source_days = None
            age_pen = 0.0
            if source_epochs:
                source_days = max(0.0, (now - max(source_epochs)) / 86400)
                age_pen = min(30.0, max(0.0, (doc_days - source_days) / 3))

            stale_after = fm.get("stale_after")
            stale_epoch = _parse_ts_epoch(stale_after)
            past_stale = stale_epoch is not None and now >= stale_epoch
            if stale_epoch is not None:
                shelf_pen = min(30.0, max(0.0, (now - stale_epoch) / 86400 * 2))
            else:
                try:
                    ttl = int(str(fm.get("ttl_days")))
                except (TypeError, ValueError):
                    ttl = DEFAULT_TTL_DAYS
                shelf_pen = min(30.0, max(0.0, (doc_days - ttl) * 2))
            drift_pen = min(40.0, 10.0 * len(missing))
            score = int(max(0, round(100 - age_pen - shelf_pen - drift_pen)))
            band = "fresh" if score >= FRESH_MIN else ("review" if score >= REVIEW_MIN else "stale")
            if past_stale:
                band = "stale"  # §5.5: now >= stale_after is stale, full stop

            reasons = []
            if past_stale:
                reasons.append(f"{(now - stale_epoch) / 86400:.0f}d past stale_after")
            if age_pen:
                reasons.append(f"source changed {doc_days - source_days:.0f}d after concept")
            if shelf_pen and not past_stale and stale_epoch is None:
                reasons.append(f"{doc_days - ttl:.0f}d past default shelf life of {ttl}d")
            if drift_pen:
                reasons.append(f"{len(missing)} missing source path(s)")
            if unresolved:
                reasons.append(f"{len(unresolved)} source(s) not verifiable here")
            rows.append({
                "id": rel_path, "score": score, "band": band,
                "docDays": round(doc_days),
                "sourceDays": None if source_days is None else round(source_days),
                "staleAfter": stale_after if isinstance(stale_after, str) else None,
                "sources": len(dict_sources) + len(legacy_sources),
                "missingSources": missing, "unresolvedSources": unresolved,
                "reasons": reasons,
            })
    rows.sort(key=lambda r: (r["score"], r["id"]))
    return rows


def cmd_freshness(root, repos_root, as_json, show_all, fail_under):
    rows = compute_freshness(root, repos_root)
    if as_json:
        print(json.dumps(rows, indent=2))
    else:
        bands = {"fresh": 0, "review": 0, "stale": 0}
        for r in rows:
            bands[r["band"]] += 1
        shown = rows if show_all else [r for r in rows if r["band"] != "fresh"]
        if shown:
            width = max(len(r["id"]) for r in shown)
            print(f"{'score':>5}  {'band':<6}  {'doc-age':>7}  {'src-age':>7}  concept")
            for r in shown:
                src = f"{r['sourceDays']}d" if r["sourceDays"] is not None else "-"
                print(f"{r['score']:>5}  {r['band']:<6}  {r['docDays']:>6}d  {src:>7}  "
                      f"{r['id']:<{width}}  {'; '.join(r['reasons'])}")
        sourced = sum(1 for r in rows if r["sources"])
        n_unresolved = sum(1 for r in rows if r["unresolvedSources"])
        note = f", {n_unresolved} with source(s) not verifiable here" if n_unresolved else ""
        print(f"\n{len(rows)} concept(s): {bands['fresh']} fresh, {bands['review']} to review, "
              f"{bands['stale']} stale; {sourced} declare sources "
              f"({len(rows) - sourced} scored on shelf life alone{note})")
    if fail_under is not None and any(r["score"] < fail_under for r in rows):
        return 1
    return 0


# ------------------------------------------------------------------------ viz

def collect_viz_data(root):
    """Build the JSON payload embedded in the visualization HTML."""
    report, n_concepts = run_validation(root)
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    rel = lambda p: os.path.relpath(p, root).replace(os.sep, "/")

    issues_by_file = {}
    findings = []
    for level, pairs in (("error", report.errors), ("warning", report.warnings)):
        for path, msg in pairs:
            issues_by_file.setdefault(rel(path), []).append({"level": level, "msg": msg})
            findings.append({"level": level, "file": rel(path), "msg": msg})

    nodes, edges = [], []
    broken_links = []
    for dirpath, _dirs, md_files in walk_bundle(root):
        for name in md_files:
            path = os.path.join(dirpath, name)
            node_id = rel(path)
            if name in RESERVED:
                # index.md/log.md link to everything; keep them out of the
                # graph but still surface their broken links in health.
                try:
                    with open(path, encoding="utf-8") as f:
                        text = f.read()
                except OSError:
                    continue
                for link in extract_links(root, path, text):
                    if link["broken"]:
                        broken_links.append({"from": node_id, "target": link["raw"]})
                continue
            try:
                fm, body = read_doc(path)
            except (FrontmatterError, OSError):
                fm, body = {}, ""
            for link in extract_links(root, path, body):
                if link["broken"]:
                    broken_links.append({"from": node_id, "target": link["raw"]})
                    edges.append({"source": node_id, "target": link["raw"], "broken": True})
                elif link["resolved"] and link["resolved"].endswith(".md") \
                        and os.path.basename(link["resolved"]) not in RESERVED:
                    edges.append({"source": node_id, "target": link["resolved"], "broken": False})
            dir_name = os.path.dirname(node_id) or "."
            tags = fm.get("tags")
            gen = fm.get("generated") if isinstance(fm.get("generated"), dict) else {}
            verified = normalized_verified(fm)
            stale_after = fm.get("stale_after") if isinstance(fm.get("stale_after"), str) else None
            stale_epoch = _parse_ts_epoch(stale_after)
            src_dicts, src_strings = source_entries(fm)
            nodes.append({
                "id": node_id,
                "dir": dir_name,
                "type": fm.get("type") if isinstance(fm.get("type"), str) else None,
                "title": str(fm.get("title") or os.path.splitext(name)[0]),
                "description": str(fm.get("description") or ""),
                "tags": tags if isinstance(tags, list) else [],
                "status": fm.get("status") if isinstance(fm.get("status"), str)
                          and fm.get("status") else "stable",
                "trust": trust_tier(fm),
                "generatedBy": str(gen.get("by") or "") or None,
                "generatedAt": generated_at(fm),
                "verified": [{"by": str(e.get("by") or ""), "at": str(e.get("at") or "")}
                             for e in verified],
                "staleAfter": stale_after,
                "stale": bool(stale_epoch is not None and now >= stale_epoch),
                "runtime": fm.get("runtime") if isinstance(fm.get("runtime"), str) else None,
                "sources": [{"id": str(e.get("id") or ""),
                             "title": str(e.get("title") or ""),
                             "resource": str(e.get("resource") or "")}
                            for e in src_dicts]
                           + [{"id": "", "title": "", "resource": s} for s in src_strings],
                "in": 0, "out": 0,
                "issues": issues_by_file.get(node_id, []),
                "markdown": body,
            })

    node_ids = {n["id"] for n in nodes}
    # Drop edges whose target is not a concept node (e.g. links to non-concept
    # files) unless broken.
    edges = [e for e in edges if e["broken"] or e["target"] in node_ids]
    degree_in, degree_out = {}, {}
    for e in edges:
        if e["broken"]:
            continue
        degree_out[e["source"]] = degree_out.get(e["source"], 0) + 1
        degree_in[e["target"]] = degree_in.get(e["target"], 0) + 1
    for n in nodes:
        n["in"] = degree_in.get(n["id"], 0)
        n["out"] = degree_out.get(n["id"], 0)

    by_type, by_dir, by_tag, by_trust, by_status = {}, {}, {}, {}, {}
    for n in nodes:
        by_type[n["type"] or "(none)"] = by_type.get(n["type"] or "(none)", 0) + 1
        top = n["dir"].split("/")[0] if n["dir"] != "." else "(root)"
        by_dir[top] = by_dir.get(top, 0) + 1
        for t in n["tags"]:
            by_tag[t] = by_tag.get(t, 0) + 1
        by_trust[n["trust"]] = by_trust.get(n["trust"], 0) + 1
        by_status[n["status"]] = by_status.get(n["status"], 0) + 1

    return {
        "generated": datetime.datetime.now(datetime.timezone.utc)
                     .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bundle": os.path.basename(root),
        "okfVersion": OKF_VERSION,
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "concepts": n_concepts,
            "errors": len(report.errors),
            "warnings": len(report.warnings),
            "byType": by_type, "byDir": by_dir, "byTag": by_tag,
            "byTrust": by_trust, "byStatus": by_status,
        },
        "health": {
            "orphans": sorted(n["id"] for n in nodes if n["in"] == 0),
            "brokenLinks": broken_links,
            "missingDescription": sorted(n["id"] for n in nodes if not n["description"]),
            "missingGenerated": sorted(n["id"] for n in nodes if not n["generatedAt"]),
            "unverified": sorted(n["id"] for n in nodes if n["trust"] == "unverified"),
            "pastStale": sorted(n["id"] for n in nodes if n["stale"]),
            "findings": findings,
            "freshness": compute_freshness(root),
        },
    }


def cmd_viz(root, out_path):
    data = collect_viz_data(root)
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "viz_template.html")
    with open(template_path, encoding="utf-8") as f:
        template = f.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = template.replace('"__OKF_DATA_JSON__"', payload)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {os.path.relpath(out_path, root)} "
          f"({len(data['nodes'])} nodes, {len(data['edges'])} edges, "
          f"{data['stats']['errors']} errors, {data['stats']['warnings']} warnings)")
    return 0


# ----------------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        description="OKF v0.2 bundle tooling (validate, index, viz, freshness)")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("validate", "check bundle conformance (§11)"),
                            ("index", "generate index.md files (§8)")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("bundle", nargs="?", default=".", help="bundle root (default: cwd)")
    p = sub.add_parser("viz", help="generate a self-contained HTML visualization")
    p.add_argument("bundle", nargs="?", default=".", help="bundle root (default: cwd)")
    p.add_argument("-o", "--output", default=None,
                   help="output file (default: <bundle>/okf-viz.html)")
    p = sub.add_parser("freshness", help="score concepts 0-100 for staleness")
    p.add_argument("bundle", nargs="?", default=".", help="bundle root (default: cwd)")
    p.add_argument("--repos-root", default=None,
                   help="directory legacy '<org>/<repo>:<path>' sources are resolved "
                        "against (default: the bundle's parent directory)")
    p.add_argument("--json", action="store_true", help="emit all rows as JSON")
    p.add_argument("--all", action="store_true", help="list every concept, not just sub-fresh ones")
    p.add_argument("--fail-under", type=int, default=None, metavar="N",
                   help="exit 1 if any concept scores below N")
    args = parser.parse_args()
    root = os.path.abspath(args.bundle)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    if args.command == "validate":
        return cmd_validate(root)
    if args.command == "index":
        return cmd_index(root)
    if args.command == "freshness":
        return cmd_freshness(root, args.repos_root, args.json, args.all, args.fail_under)
    return cmd_viz(root, args.output or os.path.join(root, "okf-viz.html"))


if __name__ == "__main__":
    sys.exit(main())
