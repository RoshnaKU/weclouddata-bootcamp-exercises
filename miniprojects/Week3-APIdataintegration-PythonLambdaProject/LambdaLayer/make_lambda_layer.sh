#!/bin/bash
mkdir my-lambda-layer && cd my-lambda-layer
mkdir -p aws-layer/python/lib/python3.10/site-packages
pip3 install -r requirements.txt --target aws-layer/python/lib/python3.10/site-packages
cd aws-layer
zip -r9 lambda-layer.zip .

aws lambda publish-layer-version \
    --layer-name Data-Preprocessing \
    --description "My Python layer" \
    --zip-file fileb://lambda-layer.zip \
    --compatible-runtimes python3.10