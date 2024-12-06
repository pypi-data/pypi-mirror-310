![](https://img.shields.io/badge/Standard%20Security%20Action-gold?style=for-the-badge&logo=trendmicro&logoColor=red&link=https%3A%2F%2Ftrendmicro.atlassian.net%2Fwiki%2Fspaces%2Frdsecpub%2Fpages%2F616997839%2FStandard%2BSecurity%2BGitHub%2BActions)

# fortify-getorcreateapp

Support Library for creating and querying fortify versions and applications.

## Installation

```pip install fortify-getorcreateapp```

## Command line Usage

As a python library with a cli entry point, the functionality can be easily accessed through CLI:

```
$fortify-getorcreateapp --h

usage: fortify-getorcreateapp [-h] [--jid JID] app_name version_name

Print Fortify application and version ids of given fortify application name and version names. Create version and application if they don't exist. Requires
environment variables 'FORTIFY_TOKEN' and 'FORTIFY_URL' to be set. FORTIFY_TOKEN must be an automation token for a (service) account capable of creating a
version and assign users to versions. FORTIFY_URL is the base url for the fortify service (e.g. https://codescan-ssc.mycompany.com/ssc) . It does not include the
path to the api endpoing e.g. 'api/v1'.

positional arguments:
  app_name      application name
  version_name  version name

options:
  -h, --help    show this help message and exit
  --jid JID     PDG_XXXXXX - identifier added to version description, used to synchronized with dashboard. Please set manually if not set upon creation. Consult
                #rdsec with this message if needed.
```

## Build

```make```

## Contribute

This is part of the Standard github actions and as such it is subject to the same process (no direct writes, PRs reviewed by GRC). If you have a contribution please fork and submit a PR.


## FAQ

A: "Why is this not simply part of the github action that uses it?"

B: Because the functionality is used across other projects and scripts, it's right encapsulation is a library.
