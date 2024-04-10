# Account Access Removal

## Description

A user account can be removed from the domain.

Specific rights can be removed from an account in the domain.

## Example of Attack

If an attacker compromises a privileged account with the ability to delete accounts or remove privileges, they can use it to disable accounts that could be used for remediation.

## MITRE documentation

- Tactic : Impact
- Technique : Account Access Removal
- Sub-technique : /
- ID : [T1531](https://attack.mitre.org/techniques/T1531/)

## Détection

Some events can generate logs within the domain.


### Google Workspace-related Events

- DELETE_USER
- UPDATE_DOMAIN_PRIMARY_ADMIN_EMAIL
- CHROME_OS_REMOVE_USER
- GRANT_ADMIN_PRIVILEGE
- GRANT_DELEGATED_ADMIN_PRIVILEGES

## Remediation

The super administrator account must be used to address the compromised administrator account.

The compromised account must be temporarily suspended, and its related sessions and applications revoked.

## Recommendations

Several features can be implemented to limit the risk of compromise of administrator accounts.

### Enabling the Advanced Protection Program

It is possible to activate the program on accounts to enhance security and access to data: enforcing the use of 2FA, limiting the rights granted to third-party applications (via OAuth tokens)... More information is available on the official program page : https://landing.google.com/advancedprotection/

![img](../resources/advanced_program.png)

### 2FA activation

It is possible to offer (or enforce) and configure accepted 2FA methods on accounts.

### Implementation of Context-Aware Access Rules

It is possible to implement access rules to restrict access to Google services. For example, limiting access to a specific IP address or a specific version of Google Chrome.

> Compatible editions for this feature: Frontline Standard; Enterprise Standard and Enterprise Plus; Education Standard and Education Plus; Enterprise Essentials Plus; Cloud Identity Premium.

> The administration portal is typically not sensitive to context-aware access rules.
