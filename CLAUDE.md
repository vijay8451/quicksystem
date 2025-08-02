# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Installation and Setup

Install dependencies and the tool:
```bash
sh setup.sh
```

This installs the tool in development mode using pip. Requires Python 3.12 or later.

Configuration setup:
```bash
cp quicksystem.properties.sample quicksystem.properties
# Edit quicksystem.properties with your specific values
```

## Architecture Overview

This is a Python CLI tool built with Click that automates Red Hat Satellite system provisioning and installation through Beaker and Jenkins integration.

### Core Components

- **quicksystem.py** - Main CLI interface with Click commands
- **beakerclient.py** - Beaker lab system reservation and provisioning using Fabric for SSH operations
- **jenkinsjob.py** - Jenkins job automation for Satellite installation using jenkinsapi
- **propertyreader.py** - Configuration management using configparser for `quicksystem.properties`
- **sender.py** - Email notification system for deployment reports
- **msg.py** - Console output utilities (echo_error, echo_normal, echo_success)

### Key Workflows

1. **System Reservation**: Uses Beaker client to reserve random systems from the lab
2. **System Provisioning**: Provisions reserved systems with specified distro trees
3. **Satellite Installation**: Triggers Jenkins installer job with configuration parameters
4. **Content Host Setup**: Provisions additional systems to act as content hosts
5. **Email Reporting**: Sends deployment status reports via email

### Configuration Structure

The tool relies on `quicksystem.properties` with sections:
- `[RandomSystem]` - System count configuration
- `[Beaker]` - Beaker credentials and environment settings
- `[JenkinsInstaller]` - Jenkins URL, job name, and Satellite version parameters
- `[TheSystem]` - Specific system hostname and distro tree
- `[ContentHost]` - Content host count configuration
- `[Emails]` - Email sender/recipient configuration
- `[Logs]` - Logging level (INFO/DEBUG)

## Development Commands

Run the CLI tool:
```bash
quicksystem --help
```

Install in development mode:
```bash
pip3 install --editable .
```

## Testing

No specific test framework is configured. Test manually using the CLI commands with proper configuration.