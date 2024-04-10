# Gather Victim Network Information

## Description

The use of Google Workspace involves configuring several fields at the domain's DNS level.

## Exemple d’attaque

The use of Google Workspace typically involves configuring specific DNS entries including:
- An MX record linked to one or more Google subdomains
- An SPF record associated with the use of Google:
```
include:_spf.google.com
```

- A DKIM record (if configured) associated with the use of Google:
By default, the proposed selector is "google."

- A TXT record associated with the use of Google for domain configuration and validation.

An attacker can then perform DNS queries to identify potential entries related to Google based on the observed patterns above.

## MITRE documentation

- Tactic : Reconnaissance
- Technique : Gather Victim Network Information
- Sub-technique : DNS
- ID : [T1590](https://attack.mitre.org/techniques/T1590/)

## Detection

No detection is available.

### Evenements Google Workspace liés

/

## Remediation

No remediation is available.

Reconnaissance does not have any impact.

## Recommendations

/
