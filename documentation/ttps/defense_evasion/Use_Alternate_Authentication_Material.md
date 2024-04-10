# Use Alternate Authentication Material

## Description

To access Google Workspace data, it is possible to use the API instead of the graphical interface.

## Example of Attack

An attacker can use an API token to access Google data in an automated manner.

> There is also a way to bypass contextual access rules by going through the API.

## MITRE documentation

- Tactic : Defense Evasion
- Technique : Use Alternate Authentication Material
- Sub-technique : /
- ID : [T1550](https://attack.mitre.org/techniques/T1550/)

## Detection

It is possible to identify the permission access and usage of a third-party application (via token) to access items. This generates events in the logs.

> The verbosity of token usage is significant.

### Google Workspace related events

- ACCESS_DENY_EVENT
- authorize
- request

## Remediation

It is possible to revoke access to the application by removing it from the user's profile in the admin console.

![img](../resources/app_token_connected.png)

## Recommendations

Google Workspace offers an application filtering solution.

### Enabling a list of authorized applications.

It is possible to define a list of applications authorized to be executed on domain accounts. If an application is not on this list, a customizable error message can be displayed.

### Enabling the Advanced Protection Program

It is possible to activate the program on accounts to enhance security and access to data: enforcing the use of 2FA, limiting the rights granted to third-party applications (via OAuth tokens)... More information is available on the official program page : https://landing.google.com/advancedprotection/

![img](../resources/advanced_program.png)
