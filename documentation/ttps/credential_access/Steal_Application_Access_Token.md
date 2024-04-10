# Steal Application Access Token

## Description

Third-party applications can interact with a Google account to perform operations on its behalf.

## Example of attack

An attacker could obtain access tokens to impersonate an account and retrieve information: either by creating a fake application where the user grants permission for the application to perform actions on their behalf, or by retrieving tokens from legitimate applications that have been compromised.

## MITRE documentation

- Tactic : Credential Access
- Technique : Steal Application Access Token
- Sub-technique : /
- ID : [T1528](https://attack.mitre.org/techniques/T1528/)

## Detection

It is possible to identify suspicious rights permissions in token log events.

### Google Workspace related events

- authorize
- request

## Remediation

The analyst can review the applications authorized by the user from the user's page on the admin panel. 

In the case of suspicious applications, permissions must be revoked by removing them.


## Recommendations

Google Workspace offers several features to reduce this risk.

### Enabling the Advanced Protection Program

It is possible to activate the program on accounts to enhance security and access to data: enforcing the use of 2FA, limiting the rights granted to third-party applications (via OAuth tokens)... More information is available on the official program page : https://landing.google.com/advancedprotection/

![img](../resources/advanced_program.png)


### Enabling a list of authorized applications.

It is possible to define a list of applications authorized to be executed on domain accounts. If an application is not on this list, a customizable error message can be displayed.
