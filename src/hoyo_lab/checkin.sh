#!/bin/sh

script_dir="$( cd "$( dirname "$0" )" && pwd )"
echo $script_dir
cd "$script_dir"
cd ..
cd ..

python3 src/hoyo_lab/sdk/checkin.py
