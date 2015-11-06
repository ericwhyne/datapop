#!/bin/bash
./datapop-publish.py
aws s3 cp index.html s3://ericwhyne-staticblogstuff/index.html
