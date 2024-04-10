## Infrastructure documentation

## GW Forensic container

You can use Docker to utilize GW Forensic.

This avoids installing Python and necessary libraries directly on the workstation and makes its usage easier.

To do this, you can use the Dockerfile provided in this directory to build the image and subsequently use it.

### Build

```
docker build -t gwforensic .
```

### Run

```
docker run --rm -v <DATA_DIR>/:/data gwforensic config.yml
```

## GW Forensic with OpenSearch

You can use OpenSearch as a log analysis tool to identify malicious patterns.

To do this, deploy an OpenSearch instance with the Dashboards interface on the investigation infrastructure to visualize exported events.

In the same directory, a "docker-compose.yml" file can be used locally to ingest data directly from GW Forensic.

If you use GW Forensic with docker, do not forget to use the same network to enable communications between containers.

### Installation & Launch

```
docker-compose up -d
```

### Usage

Visit the OpenSearch Dashboards interface, typically at: http://127.0.0.1:5601/.

Create a new index using the naming convention used in the GW Forensic configuration file, then explore the data!

