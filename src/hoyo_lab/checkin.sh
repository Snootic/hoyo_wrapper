#!/bin/sh

script_dir="$( cd "$( dirname "$0" )" && pwd )"
echo $script_dir
cd "$script_dir"
cd ..

python3 hoyo_lab/sdk/checkin.py
