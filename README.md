# quicksystem

This is a cli tool to reserve, provision a system on Beaker and use Jenkins job for Satellite .

[Features](https://github.com/vijay8451/quicksystem#1-features) | [Installation and 
Configuration](https://github.com/vijay8451/quicksystem#2-installation-and-configuration) | [Examples](https://github.com/vijay8451/quicksystem#3-examples) | [Version](https://github.com/vijay8451/quicksystem#5-version) | [License]()

## 1. Features
 
 * Reserve and provision any random system over Beaker for Satellite and Content Host.
 * Re-provision a already reserved system .
 * Install Satellite using Jenkins installer job .
 * Install Satellite on already reserved system .
 * Setup Beaker client .
 * Send report over email for Satellite and Content host.

## 2. Installation and Configuration:

Step 1: to Install:
```bash
# git clone https://github.com/vijay8451/quicksystem.git
# sh setup.sh
```
Step 2: Copy the `quicksystem.properties.sample` and put the values, for more details refer 
commented provided under `quicksystem.properties.sample`: 
```bash
# cp quicksystem.properties.sample quicksystem.properties
# vi quicksystem.properties
```
or using separate virtual env:

```bash
# python36 -m venv < myenv >
# source < myenv >/bin/active
# git clone https://github.com/vijay8451/quicksystem.git
# sh setup.sh

# cp quicksystem.properties.sample quicksystem.properties
# vi quicksystem.properties
```
## 3. Examples
 * To list all options:
 ```bash
# quicksystem 
Usage: quicksystem [OPTIONS] COMMAND [ARGS]...

  CLI tool to reserve, provision a system and use Jenkins job for Satellite.

Options:
  --help  Show this message and exit.

Commands:
  content-host       Reserve and provision content host.
  jenkins-installer  Install Satellite using Jenkins installer job.
  random-system      Reserve and provision any random system.
  setup-client       Setup beaker client.
  thesystem          Provision a already reserved system.

``` 
 * Reserve and provision any random system for Satellite:
 ```bash
# quicksystem random-system
```
 * Reserve and provision any random system for Satellite and content host:
 ```bash
# quicksystem random-system --help
Usage: quicksystem random-system [OPTIONS]

  Reserve and provision any random system.

Options:
  --jenkins-job TEXT   to run installer job i.e. --jenkins-job=True
  --content-host TEXT  to reserve and provision content hosts
                       i.e. --content-host=True
  --help               Show this message and exit.

# quicksystem random-system --content-host True --jenkins-job True
```
 *  Provision a already reserved system:
 ```bash
# quicksystem thesystem --help
Usage: quicksystem thesystem [OPTIONS]

  Provision a already reserved system.

Options:
  --jenkins-job TEXT  to run installer job i.e. --jenkins-job=True
  --help              Show this message and exit.

# quicksystem thesystem --jenkins-job True
```
 * Setup beaker client:
 ```bash
# quicksystem setup-client
```
## 4. License
[MIT](https://choosealicense.com/licenses/mit/)

## 5. Version
[Version](https://github.com/vijay8451/quicksystem/blob/master/setup.py#L11)
