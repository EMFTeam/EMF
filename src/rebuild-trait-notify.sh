#!/bin/bash

set -e
set -x
cd "${EMF_ROOT:-/cygdrive/c/cygwin64/home/ziji/g/EMF}"

./src/trait-notify.pl -t effects > EMF/common/scripted_effects/emf_notify_codegen_effects.txt
./src/trait-notify.pl -t events > EMF/events/emf_notify_codegen.txt
./src/trait-notify.pl -t localisation > EMF/localisation/1_emf_notify_codegen.csv

