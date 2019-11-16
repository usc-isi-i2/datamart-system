#!/bin/bash

echo $0 $@

base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $base

function usage {
    echo "Usage: start-datamart.sh [-d] [-w] [-e]"
    echo "       stop-datamart.sh [-d] [-w] [-e]"
    echo
    echo "Start/stop ISI datamart."
    echo 
    echo "Without any argument start/stop all ISI datamart related services."
    echo "Use -d to start/stop ISI datamart server"
    echo "Use -w to start/stop Wikidta Blazegraph"
    echo "Use -e to start/stop Elasticsearch"
}

if [[ ! -e env.sh ]]; then
    echo Environment variable file env.sh does not exists. Run ./setup.py.
    exit 1
fi

source env.sh

start_datamart=1
prefix="Starting"
if [[ $0 =~ "stop" ]]; then
    start_datamart=0
    prefix="Stopping"
fi

datamart=0
wikidata=0
elasticsearch=0
while getopts ":dwe" opt; do
    case ${opt} in
	d ) datamart=1
	    ;;
	w ) wikidata=1
	    ;;
	e ) elasticsearch=1
	    ;;
	? ) usage
	    exit 1
	    ;;
    esac
done

if [[ "$datamart" -eq 0 && "$wikidata" -eq 0 && "$elasticsearch" -eq 0 ]] ; then
    echo All services
    datamart=1
    wikidata=1
    elasticsearch=1
fi

if [[ ! -e $base/log ]]; then
    mkdir $base/log
fi

if [[ "$wikidata" -eq 1 ]]; then
    echo $prefix Wikidata
    cd data/wikidata/
    if [[ "$start_datamart" -eq 1 ]]; then
	echo "./start.sh"
	./start.sh
    else
	echo "./stop.sh"
	./stop.sh
    fi
    cd $base
fi

if [[ "$elasticsearch" -eq 1 ]]; then
    echo $prefix Elasticsearch
    cd wikibase-docker/
    if [[ "$start_datamart" -eq 1 ]]; then
	echo "nohup docker-compose up &> $base/log/elasticsearch.log &"
	nohup docker-compose up &> $base/log/elasticsearch.log &
    else
	echo "docker-compose down"
	docker-compose down
    fi
    cd $base
fi

if [[ "$datamart" -eq 1 ]]; then
    echo $prefix Datamart
    cd datamart-upload
    # source env-datamachines.sh
    if [[ "$start_datamart" -eq 1 ]]; then
	echo "docker-compose up &> $base/log/datamart.log &"
	nohup docker-compose up &> $base/log/datamart.log &
    else
	echo "docker-compose down"
	docker-compose down
    fi
    cd $base
fi

