# Data Handling and Safety

## Synthetic data only

Every data point in this project is fictional:

- record references use the record-syn prefix;
- identities use the synthetic suffix;
- public addresses use reserved documentation ranges;
- image names use the example.invalid domain;
- session and change references are fabricated.

Do not replace fixtures with real sensitive data, personal data, credentials,
production logs, exported database rows, token values, or configuration files.

## Safe operating boundary

The repository is designed for a local machine and does not require privileged
access, an external account, or network scanning. If you later connect an
equivalent lab to Wazuh, Elastic, Kubernetes, or a cloud sandbox:

1. Use only a tenant, cluster, or hosts you own or are explicitly authorized to
   test.
2. Keep the lab separate from business-critical and production systems.
3. Use test accounts and synthetic records.
4. Review logs and screenshots before publishing them.
5. Never store credentials in Git.

## Privacy-aware detection design

The scenarios use access counts and synthetic record references. In a real
environment, the SIEM should receive only the information needed to identify
unusual access behavior. Business content should remain outside routine SOC
telemetry whenever possible.

## Publication checklist

Before publishing to GitHub:

- run make validate;
- inspect Git status for files outside this project;
- confirm no personal or organizational data is present;
- use a generic fictional organization name;
- review screenshots and remove unexpected system information.
