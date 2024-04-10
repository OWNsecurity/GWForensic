# System Shutdown/Reboot

## Description

It is possible to perform operations on virtual machines attached to a GCP project.

## Example of Attack

An attacker who has compromised a Google account with access to virtual machines within a GCP project has the ability to shut down the machines.

## MITRE documentation

- Tactic : Impact
- Technique : System Shutdown/Reboot
- Sub-technique : /
- ID : [T1529](https://attack.mitre.org/techniques/T1529/)

## Detection

There are no detection events that can be used.

### Google Workspace related events

/

## Remediation

In case of suspicious reboot events, it may be interesting to review the accounts with access to the machines and verify that no suspicious behavior is observed on them, such as unusual connections...


## Recommendations

Several security features can be implemented.

### 2FA activation

It is possible to offer (or enforce) and configure accepted 2FA methods on accounts.

### Implementation of Context-Aware Access Rules on GCP

It is possible to implement access rules to restrict access to Google services. For example, limiting access to a specific IP address or a specific version of Google Chrome.

> Compatible editions for this feature: Frontline Standard; Enterprise Standard and Enterprise Plus; Education Standard and Education Plus; Enterprise Essentials Plus; Cloud Identity Premium.

> The administration portal is typically not sensitive to context-aware access rules.
