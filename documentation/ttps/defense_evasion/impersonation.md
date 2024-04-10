# Impersonation

## Description

A compromised account can be used to communicate with other individuals within the company in order to impersonate the victim and obtain information and access.

## Example of Attack

An attacker has compromised an account of an IT developer. They can contact the IT team to request the installation or configuration of access to a machine as part of their activity in order to gain additional access for the attack.

## MITRE documentation

- Tactic : Defense Evasion
- Technique : Impersonation
- Sub-technique : /
- ID : [T1656](https://attack.mitre.org/techniques/T1656/)

## Detection

There is no specific detection method available.

### Google Workspace related events

/

## Investigation

It is possible to trace all events on the domain, especially regarding Meet (meetings) and Chat (messages) exchanges, to discover if any exchanges have taken place and investigate them.

Internal or external email communications may have occurred. It is necessary to investigate the email activity of the compromised account.


## Recommendations

There are no specific recommendations.
