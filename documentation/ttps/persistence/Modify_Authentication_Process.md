# Modify Authentication Process

## Description

Depending on the configuration of the Google Workspace domain, a domain user can modify the login methods for their account.

## Example of Attack

An attacker could disable multi-factor authentication for the hijacked account in order to facilitate persistence on it.

## MITRE documentation

- Tactic : Persistence
- Technique : Modify Authentication Process
- Sub-technique : Multi-Factor Authentication
- ID : [T1556.006](https://attack.mitre.org/techniques/T1556/006/)

## Detection

Disabling 2FA for an account generates an event in the Google Workspace logs.

### Related Google Workspace Events

- 2sv_disable

## Remediation

It is possible to temporarily disable the account to contain the attack and to verify the malicious actions performed on the account to avoid missing any other methods of persistence or modified configurations.

It is then necessary to ensure with the legitimate user the reactivation of their 2FA method on the Google account.

## Recommendations

Google Workspace offers various features including :

### 2FA activation

It is possible to offer (or even enforce) and configure the accepted 2FA methods on accounts.
