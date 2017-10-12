#!/bin/bash

mypath=`realpath $0`
mybase=`dirname $mypath`

dbname=conversations

if [[ -n `psql -lqt | cut -d \| -f 1 | grep -w "$dbname"` ]]; then
    dropdb $dbname
fi
createdb $dbname

cd $mybase
psql -af create.sql $dbname
#psql -af load.sql $dbname