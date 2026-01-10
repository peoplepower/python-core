<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

# CareDaily

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/license/apache-2-0)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/peoplepower/python-core?sort=semver)](https://github.com/peoplepower/python-core/tree/latest)
[![Documentation](https://img.shields.io/badge/docs-apidocs-blue.svg)](https://app.peoplepowerco.com/cloud/apidocs/html/cloud.html)

Python SDK and CLI tool for interacting with the CareDaily API platform.

[**CareDaily**](#caredaily) |
[**Just Watch It Work**](#just-watch-it-work) |
[**Getting Started**](#getting-started) |
[**Explore the docs**](#explore-the-docs) |
[**Sign Up**](https://app.caredaily.ai/signup)

## About

The CareDaily Python SDK provides a comprehensive interface to the CareDaily cloud platform (powered by People Power Company). It offers both programmatic access through Python classes and a command-line interface for managing smart home devices, user accounts, locations, and AI-powered services.

This package enables developers to:
- Build applications that integrate with CareDaily services
- Manage user authentication and authorization
- Control and monitor IoT devices
- Access AI and machine learning capabilities
- Manage administrative tasks and analytics

## Just watch it work

```bash
# Install the package
pip install caredaily

# Initialize your configuration
caredaily configure init

# Test connectivity
caredaily ping
```

## Getting Started

### Installation

Install from PyPI (when published):
```bash
pip install caredaily
```

Or install from source:
```bash
git clone https://github.com/peoplepower/python-core.git
cd python-core
pip install -e ".[dev]"
```

### Configuration

Before using the SDK or CLI, you need to configure your credentials:

```bash
# Initialize configuration (creates ~/.caredaily/config and ~/.caredaily/credentials)
caredaily configure init

# Set up a profile interactively
caredaily configure interactive --profile myprofile

# Or use environment variable to specify profile
export CAREDAILY_PROFILE=myprofile
```

Your configuration files will be stored in `~/.caredaily/`:
- `config`: Hostname, SSL settings, proxy configuration
- `credentials`: API keys (kept separate for security)

### Using the CLI

```bash
# Check cloud connectivity
caredaily cloud-connectivity --check-availability

# Login with username and password
caredaily login --username myuser --password mypass

# Get cloud version
caredaily cloud-connectivity --version

# Use a specific profile
caredaily --profile production ping
```

### Using the SDK

```python
from caredaily import CareDaily, Authentication, CloudConnectivity

# Initialize with default profile
client = CareDaily()

# Or use a specific profile
client = CareDaily(profile="production")

# Check cloud connectivity
result = client.app_api(CloudConnectivity).check_availability()
print(result.data)

# Login with credentials
auth_result = client.app_api(Authentication).login_by_username(
    username="myuser",
    password="mypass"
)
print(auth_result.data)

# Access different API types
from caredaily import Locations, Devices

# Get user information
user_information = client.app_api(UserAccounts).get_user_information()

# Get devices
devices = client.app_api(Devices).get_devices()
```

### API Examples

#### Working with Locations
```python
from caredaily import CareDaily, Locations

client = CareDaily()
locations_api = client.app_api(Locations)

# Get all locations for the user
result = locations_api.get_user_information()
for location in result.data.get('locations', []):
    print(f"Location: {location['name']}")
```

#### Working with Devices
```python
from caredaily import CareDaily, Devices

client = CareDaily()
devices_api = client.app_api(Devices)

# Get all devices
result = devices_api.get_devices()
for device in result.data.get('devices', []):
    print(f"Device: {device['id']} - {device['type']}")
```

#### Admin Operations
```python
from caredaily import CareDaily, Users, Organizations

client = CareDaily()  # Must use admin API key

# Get organization users
users_api = client.admin_api(Users)
result = users_api.get_users(organizationId=123)

# Get organization details
orgs_api = client.admin_api(Organizations)
result = orgs_api.get_organization(organizationId=123)
```

### Development

For development setup and testing:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=caredaily --cov-report=html

# Run linter
ruff check src/

# Format code
ruff format src/
```

## Explore the Docs

CareDaily provides several API documentation resources to help you build and integrate with the platform:

- **[Cloud API Docs](https://app.peoplepowerco.com/cloud/apidocs/cloud.html)**
Comprehensive reference for the main CareDaily cloud API, including endpoints for device management, user accounts, locations, and core platform services.
- **[Admin API Docs](https://app.peoplepowerco.com/cloud/apidocs/admin.html)**
Documentation for administrative APIs, covering organization management, user administration, analytics, and advanced configuration options for enterprise use.
- **[Bots API Docs](https://app.peoplepowerco.com/cloud/apidocs/bots.html)**
Details on the Bots API, which enables automation, custom bot creation, and integration with CareDaily's AI-powered services for smart home and IoT workflows.

## Get Involved

- Ask and answer questions on [StackOverflow](https://stackoverflow.com/questions/tagged/caredaily-python) using the **caredaily-python** tag

- Help find and fix issues by [**reporting bugs**](https://github.com/peoplepower/python-core/issues/new?labels=bug&template=bug-report---.md).
- Have a new idea?  Have a suggestion? [**Request a feature**](https://github.com/peoplepower/python-core/issues/new?labels=enhancement&template=feature-request---.md) to get our attention.

## Contributor Guide

Interested in contributing? Check out our
[CONTRIBUTING.md](https://github.com/peoplepower/python-core/blob/master/CONTRIBUTING.md)
to find resources around contributing along with a detailed guide on
how to set up a development environment.

## Activity

<a href="https://next.ossinsight.io/widgets/official/compose-org-active-contributors?period=past_12_months&activity=active&owner_id=113403165" target="_blank" style="display: block" align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://next.ossinsight.io/widgets/official/compose-org-active-contributors/thumbnail.png?owner_id=113403165&period=past_12_months&activity=active&image_size=2x3&color_scheme=dark" width="273" height="auto">
    <img alt="Active participants of pingcap - past 28 days" src="https://next.ossinsight.io/widgets/official/compose-org-active-contributors/thumbnail.png?owner_id=113403165&period=past_12_months&activity=active&image_size=2x3&color_scheme=light" width="273" height="auto">
  </picture>
</a>

<!-- Made with [OSS Insight](https://ossinsight.io/) -->