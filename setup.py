#!/usr/bin/env python
from __future__ import print_function
from string import Template

import argparse
import glob
import json
import os
import subprocess
import sys

TEST_RUN = 0
def run_command(command):
    if TEST_RUN:
        print('Command: ', command)
    else:
        print('Command: ', command)
        print(subprocess.check_output(command, shell=True))
        
def extract(datafile, destination):
    command = "cd " + destination
    if datafile.endswith('.tgz'):
        command += "; tar xzf " + datafile
    elif datafile.endswith('.zip'):
        command += "; unzip " + datafile
    command += "; pwd"
    run_command(command)
    
    
def setup(config, services):
    template_mapping = {}
    template_mapping["augment_seed_datasets_dir"]=config["augment_seed_datasets_dir"]

    setup_data_dir = config['setup_data_dir']
    setup_specs = config['setup_specification']

    if not os.path.exists(setup_data_dir):
        print('Cannot find directory containing setup data needed for the Datamart.')
        print('Directory missing:', setup_data_dir)
        sys.exit(1)

    # Extract data files
    for spec in setup_specs:
        name = spec['name']
        data_files = sorted(glob.glob(os.path.join(setup_data_dir, spec['data_file'])))
        if len(data_files) == 0:
            print('Cannot find data files for: file_spec')
            sys.exit(1)
        if len(data_files) > 1:
            print('Found multiple data files for:', name)
            print('  Using file:',  data_files[0])
        if 'destination' in spec:
            destination = os.path.abspath(spec['destination'])
            template_mapping[name] = destination
            if not os.path.exists(destination):
                command = "pwd; mkdir -p " + destination
                run_command(command)
        if name in services and spec['action'] == 'extract':
            extract(data_files[0], spec['destination'])

    # Create env.sh for datamart-upload's docker-compose.yml
    templates = ['wikibase-docker/env.sh-template', 'datamart-upload/env.sh-template', 'env.sh-template']
    for template in templates:
        env_file = None
        if not os.path.exists(template):
            print('Template file not found, skipping:', template)
            continue
        env_file = template[:-9]
        env_template = open(template, 'r').read()
        env_template = Template(env_template)
        with open('env.sh', 'w') as fd:
            print(env_template.substitute(**template_mapping), file=fd)
    if env_file:
        print()
        print('Environment file created:', env_file)
        print()

    # Special handling for Elasticsearch:
    if 'elasticsearch' in services:
        for spec in setup_specs:
            if 'elasticsearch' in spec:
                break
        raw_es_data_dir = setup_data_dir + '/wikidata_es_raw_format_data'
        print("Setting up Elasticsearh index")
        print("  This may take a while...")
        run_command("source ./env.sh; cd wikibase-docker/; docker-compose up -d")
        run_command("cd " + raw_es_data_dir + "/; ./load_es_bulk.sh")
        run_command("cd " + raw_es_data_dir + "/; ./load_wiki_fb_embeddings.sh")
        run_command("sleep 60; source ./env.sh; cd wikibase-docker/; docker-compose down")


if __name__ == '__main__':
    with open('config.json', 'rt') as df:
        config = json.load(df)
    parser = argparse.ArgumentParser(description='ISI Datamart setup script.')
    parser.add_argument('-s', '--setup', action='append',
                        help='Setup specific services. Use --list to see service names')
    parser.add_argument('-l', '--list', action='store_true')
    args = parser.parse_args()

    if args.list:
        print('Available services:')
        for spec in config['setup_specification']:
            print('  ', spec['name'])
        sys.exit(0)
    
    if args.setup:
        services = args.setup
    else:
        services = [spec['name'] for spec in config['setup_specification']]
    setup(config, services)
