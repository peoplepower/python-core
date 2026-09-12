# Architecture

* [CareDaily Entry Point and Factories](entry-point-factories.md) - How the CareDaily class hands out configured API instances via explicit if-chain factories, and the checklist for adding a new API class.
* [Configuration System](configuration.md) - Profile-based INI files under ~/.caredaily/, the env vars that override them, and the config vs credentials section-naming asymmetry.
* [Repo Layout](repo-layout.md) - The three parts of the caredaily package (SDK, CLI, Pydantic models) and the map of the source tree.
* [Request Flow and RestAdapter](request-flow.md) - The single path every SDK call takes through the API base class and RestAdapter, auth headers by key type, Result parsing, and error handling.
