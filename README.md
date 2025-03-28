# Big Data (Università degli Studi Roma Tre)
## What's inside this repository?
Helper scripts to setup the environment and a docker compose to setup a hdfs cluster

## Requirements
- Docker engine and docker compose
- Java 8 or 11 (only version supported by hadoop) and JAVA_HOME setup properly
- wget (should be available by default on most distros)
- tar (should be available by default on most distros)

## How to use?
- Run setup_environment.sh to download hadoop (we're interested in hdfs client to be used from CLI)
- Run start.sh to launch cluster via docker compose
- Run stop.sh to stop cluster
