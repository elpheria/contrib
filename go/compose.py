#!/usr/bin/env python3

import os, sys
from urllib.parse import urlparse
from shutil import which
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='run tests after docker-compose',
                    action='store_true')
args = parser.parse_args()

# Gopkg.lock should always be present, so we check on it
# to see if we're positioned correctly
try:
    open('./Gopkg.lock', 'r')
except:
    print('please, run this script from root project\'s dir')
    sys.exit(1)

try:
    uri = os.environ['DOCKER_HOST']
    docker_host = urlparse(uri).hostname
except:
    docker_host = '127.0.0.1'

try:
    f = open('.env', 'r')

    for line in f:
        s = line.split('=')
        os.environ[s[0]] = s[1].rstrip('\r\n')
except FileNotFoundError:
    os.environ['DOCKER_SERVICECODE_PWD'] = '.'
    os.environ['SERVICE_CONSUL_HOSTNAME'] = 'consul'

if os.uname().sysname == 'Darwin':
    # info: add your ssh key to docker if you don't want to be asked for password
    if which('rsync') == None:
        print('rsync should be available in PATH. bye.')
        sys.exit(1)

    os.system('ssh docker@' + docker_host + ' "rm -rf *"')
    os.system('rsync -avzhe ssh --progress . docker@' + docker_host + ':' +
              os.environ['DOCKER_SERVICECODE_PWD'])

if which('docker-compose') == None:
    print('docker-compose should be available in PATH. bye.')
    sys.exit(1)

if args.test == True:
    os.system('docker-compose -f docker-compose.test.yml up --abort-on-container-exit')
else:
    os.system('docker-compose up')
