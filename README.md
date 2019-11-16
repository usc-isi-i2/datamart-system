# ISI Datamart System

This repository contains scripts to install the complete ISI Datamart system, and to start/start the
ISI Datamart system.

## Installation

### Required Files

To install the datamart system you will need the ISI Datamart setup data directory of files, which
is about 600G. The content of the directory is:

- blazegraph.jnl.20191108.tgz
- datasets_uploads.20191108.tgz
- password_tokens.20191108.tgz
- redis.20191108.tgz
- wikidata-code.20191108.tgz
- wikidata.jnl.20191025.zip
- wikidata_es_raw_format_data/

Running the Elasticsearch services requires about 1.7TB of disk space. Running Wikidata requires
about 800GB of disk space.

Also, you will need the D3M seed augmentation datasets.

### Details

Clone the ISI Datamart System Repo

```
git clone --recurse-submodules git@github.com:usc-isi-i2/datamart-system.git
```

Edit the configuration files [config.json](config.json). The `setup_data_dir` field should point to
the ISI Datamart setup data directory. The `augment_seed_datasets_dir` should point to the D3M seed
augmentation dataset directory.

```
    "setup_data_dir": "/data/datamart-setup-data",
    "augment_seed_datasets_dir": "/data/datasets/seed_datasets_data_augmentation",
```

By default the configuration file will extract/upload Wikidata and Elasticsearch to  `./data` directory relative to `datamart-system` repository directory. Edit the `config.json` file to change the location.

Uploading the Elasticsearch data takes a very long time.

To run the setup, do:

```
./setup.py
```

The setup.py script will create an environment variable file, `env.sh` need to start/stop the ISI Datamart.

## Starting and Stopping the ISI Datamart

To start the Datamart:

```
source env.sh
./start-datamart.sh
```

To stop the Datamart:

```
source env.sh
./stop-datamart.sh
```

Parts of the Datamart can be started/stopped independently.

- Use `-e` option to start/stop Elasticsearch
- Use `-w` option to start/stop Wikidata
- Use `-d` option to start/stop Datamart REST and related services


