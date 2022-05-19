#!/bin/bash
fission spec init
fission env create --spec --name create-user-env --image nexus.sigame.com.br/python-env-3.8:0.0.5 --builder nexus.sigame.com.br/python-builder-3.8:0.0.2
fission fn create --spec --name create-user-fn --env create-user-env --src "./func/*" --entrypoint main.create_user --executortype newdeploy --maxscale 1
fission route create --spec --method POST --url /create_user --function create-user-fn
