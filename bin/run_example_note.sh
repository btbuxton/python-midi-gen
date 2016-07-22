#!/bin/bash

export PYTHONPATH=$(realpath $(dirname $0)/..)

echo $PYTHONPATH
python ../midi_gen/example/note.py
