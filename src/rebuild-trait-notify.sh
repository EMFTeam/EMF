#!/usr/bin/bash

set -e
set -x
cd "${EMF_ROOT:-/cygdrive/c/cygwin64/home/ziji/g/EMF}"

./src/trait-notify.pl -t effects > EMF/common/scripted_effects/emf_notify_effects.txt
./src/trait-notify.pl -t events > EMF/events/emf_notify.txt
./src/trait-notify.pl -t localisation > EMF/localisation/zz~emf_notify.csv

