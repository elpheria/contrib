#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

if ([[ ! -d $BASEDIR/../../node_modules ]] || [[ ! `ls -A ./node_modules` ]]) && [ "$NODE_ENV" != "DEBUG" ]
then
	npm install
fi

if ([[ ! -d $BASEDIR/../../dist ]] || [[ ! `ls -A ./dist` ]]) && [ "$NODE_ENV" != "DEBUG" ]
then
	mkdir -p $BASEDIR/../../dist
	bash $BASEDIR/beautify_source.sh
	$BASEDIR/../../node_modules/.bin/eslint --fix -c ./.eslintrc.json './src/**/*.js' './test/**/*.js'
	$BASEDIR/../../node_modules/.bin/babel src -d $BASEDIR/../../dist
fi

if [ "$NODE_ENV" != "DEBUG" ]
then
	npm prune --production
	docker build -f $BASEDIR/../../docker/Dockerfile .
else
	docker build -f $BASEDIR/../../docker/Dockerfile.debug .
fi
