#!/usr/bin/env python
from __future__ import print_function
from string import Template

import glob
import json
import os
import subprocess
import sys

def untar(datafile, destination):
    if not os.path.exists(destination):
        print('Creating path:', destination)
        command = "pwd; mkdir -p " + destination
        print(command)
        print(subprocess.check_output(command, shell=True))
    command = "cd " + destination
    if datafile.endswith('.tgz'):
        command += "; tar xzf " + datafile
    elif datafile.endswith('.zip'):
        command += "; unzip " + datafile
    command += "; pwd"
    print(command)
    print(subprocess.check_output(command, shell=True))
    
    
    
with open('config.json', 'rt') as df:
    config = json.load(df)

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
        print(data_files)
    # untar(data_files[0], spec['destination'])
    template_mapping[name] = os.path.abspath(spec['destination'])

# Create env.sh for datamart-upload's docker-compose.yml
env_template = open('datamart-upload/env.sh-template', 'r').read()
env_template = Template(env_template)
with open('datamart-upload/env.sh', 'w') as fd:
    print(env_template.substitute(**template_mapping), file=fd)


