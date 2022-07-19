#!/bin/bash
fission spec init
fission env create --spec --name create-user-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name create-user-fn --env create-user-env --src "./func/*" --entrypoint main.create_user --executortype newdeploy --maxscale 1
fission route create --spec --name create-user-rt --method POST --url /onboarding/create-user --function create-user-fn
