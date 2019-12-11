#!/bin/bash

set -e
set -x
cd "${EMF_ROOT:-/cygdrive/c/cygwin64/home/ziji/g/EMF}"

# Map-independent
./src/dynlevy.pl -t effects -N64 > ./EMF/common/scripted_effects/emf_dynlevy_effects.txt
# Vanila map
./src/dynlevy.pl -t laws    -N64 --stride 5 --offset 15 > ./EMF/common/laws/zz~emf_dynlevy_laws.txt
./src/dynlevy.pl -t events  -N64 --stride 5 --offset 15 > ./EMF/events/emf_dynlevy_codegen.txt
./src/dynlevy.pl -t i18n    -N64 --stride 5 --offset 15 > ./EMF/localisation/zz~emf_dynlevy.csv
# SWMH map
./src/dynlevy.pl -t laws    -N64 --stride 8 --offset 16 > ./EMF+SWMH/common/laws/zz~emf_dynlevy_laws.txt
./src/dynlevy.pl -t events  -N64 --stride 8 --offset 16 > ./EMF+SWMH/events/emf_dynlevy_codegen.txt
./src/dynlevy.pl -t i18n    -N64 --stride 8 --offset 16 > ./EMF+SWMH/localisation/zz~emf_dynlevy.csv
