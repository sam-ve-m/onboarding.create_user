#!/bin/bash
fission spec init
fission env create --spec --name create-user-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/python-builder-3.8:0.0.2
fission fn create --spec --name create-user-fn --env create-user-env --src "./func/*" --entrypoint main.create_user  --rpp 100000
fission route create --spec --method POST --url /create-user --function create-user-fn
