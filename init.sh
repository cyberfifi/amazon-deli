#!/usr/bin/env bash

( cat template.yaml;
) >credentials.yaml

echo -e "\033[0;32m credentials.yaml file generated. Please update it with your real information. \033[0m"
