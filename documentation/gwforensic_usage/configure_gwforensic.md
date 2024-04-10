# GW Forensic Usage

## Configuration

You can configure GW Forensic by modifying the config.yml file at the root of the project. 
You can customize the following settings:

### Sources

You can specify the list of sources to collect:

- `sources` : List of sources to collect.
    - `all` : all sources
    - `login`, `admin`,`drive`,`token`,`chat`,`meet`,`calendar`,`groups`,`groups_enterprise`,`chrome`,`context_aware_access`,`gcp`,`rules`,`saml`,`user_accounts`,`data_studio`,`mobile`,`keep`,`jamboard`,`access_transparency`,`currents`

### Users

You can specify the list of users to collect.

- `users` : List of users whose logs will be collected.
    - `all` : all users
    - email address

### Date

You can specify a date range to collect.

- `date` : Specific time range.
    - empty : all possible logs
    - specific start/end date: only the specified period, in RFC-3339 format (Example: `2024-03-01-10:26:35.120Z`)

### Export

You can configure the export method (only one at a time).

If using CSV or JSON, each source will produce a file containing all events from that source for the specified users. If you have chosen 2 sources (login, drive), 2 output files will be generated.

- `export` : User export method.
    - `csv` : CSV format
    - `json` : JSON format
    - `opensearch` : Directly sent to OpenSearch server


- `exportFolder` : Directory where results are stored.
  - Example : `./export/`

> Please note that an `export_ips.csv` file will always be generated regardless of the selected export method (csv, json, opensearch).


### Export Configuration

If you have chosen OpenSearch or Timesketch as the export method, certain additional fields must be filled out for real-time export to work.

- `opensearch` : Fields to fill in case of OpenSearch export.

- `timesketch` : Fields to fill in case of Timesketch export.

> Please note that the tool may not function properly if an index already exists with the same name. If you encounter an error, please check this and specify a new index name in the `config.yml` file.

## Configuration Example

### Collect all logs in CSV for only jane.doe@gwforensic.cloud user

```
sources:
  - "all"
users:
  - "jane.doe@gwforensic.cloud"
date:
  start: ""
  end: ""
export: "csv"
exportFolder: "./export/"
opensearch:
  url: "127.0.0.1"
  port: 9200
  user: "admin"
  password: "admin"
  index_name: "gwforensic-investigation-001"
timesketch:
  sketch: 0
  timestamp_description: "GW Event Log"
  timeline_name: "gw_logs_export_" # _source_logs
```

### Collect all login & drive logs in CSV for John & Jane Doe users

```
sources:
  - "login"
  - "drive"
users:
  - "john.doe@gwforensic.cloud"
  - "jane.doe@gwforensic.cloud"
date:
  start: ""
  end: ""
export: "csv"
exportFolder: "./export/"
opensearch:
  url: "127.0.0.1"
  port: 9200
  user: "admin"
  password: "admin"
  index_name: "gwforensic-investigation-001"
timesketch:
  sketch: 0
  timestamp_description: "GW Event Log"
  timeline_name: "gw_logs_export_" # _source_logs
```

### Collect all logs in OpenSearch for Jall users during the first april

```
sources:
  - "all"
users:
  - "all"
date:
  start: "2024-04-01T00:00:01.000Z"
  end: "2024-04-01T23:59:59.000Z"
export: "opensearch"
exportFolder: "./export/"
opensearch:
  url: "127.0.0.1"
  port: 9200
  user: "admin"
  password: "admin"
  index_name: "gwforensic-investigation-001"
timesketch:
  sketch: 0
  timestamp_description: "GW Event Log"
  timeline_name: "gw_logs_export_" # _source_logs
```

