# Indicator Removal

## Description

It is possible to delete items on the Google Workspace platform.


## Exemple d’attaque

An attacker may attempt to erase their tracks by deleting information across various Google Workspace services:
- Gmail
- Drive
- ...

and also on potentially compromised hardware (Chromebook).


## MITRE documentation

- Tactic : Defense Evasion
- Technique : Indicator Removal
- Sub-technique : /
- ID : [T1070](https://attack.mitre.org/techniques/T1070/)

## Detection

Some deletion events generate logs within the platform (see below).

### Google Workspace related events

- trash
- DEVICE_ACTION_EVENT

## Investigation

It is necessary to investigate the various events leading to the deletion of items. Points of attention may include:
- Items stored in Google Drive (risk of generating a lot of noise)
- Items stored in Gmail - deletion of emails, threads
- Deletion actions on hardware: memory wiping, for example.

## Recommendations

There are no specific recommendations.
