#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess
from pathlib import Path

from localpaths import rootpath

# this script shall be invoked by hiphub when certain files change in the EMF repository due to a commit. at this time,
# that is just EMF+SWMH/map/geographical_region.txt.  we invoke the same program that cuts SWMH into MiniSWMH with a
# special option to tell it to only generate EMF+MiniSWMH/map/geographical_region.txt from the aforementioned file
# rather than do its full set of operations. additionally, EMF+SWMH history is auto-generated from here, and so are some
# misc. bits of code (e.g., holding slot trigger for SWMH for the prosperity land reclamation event).

version = 'v10.6-BETA'
version_path = rootpath / 'EMF/EMF/version.txt'
emf_src_path = rootpath / 'EMF/src'

scons_bin_path = Path('/usr/bin/scons')
mapcut_bin_path_default = Path('/usr/local/bin/mapcut')
mapcut_path = rootpath / 'ck2utils/mapcut'
cut_titles = ['e_rajastan', 'e_mali', 'k_sahara', 'k_fezzan', 'k_kanem', 'k_hausaland', 'k_canarias']
emf_holding_slot_path = emf_src_path / 'holding_slot_trigger.py'
emf_swmh_history_path = emf_src_path / 'emf_swmh_history.py'
cadet_codegen_path = emf_src_path / 'cadet_codegen.py'
religion_codegen_path = emf_src_path / 'religion_codegen.py'
revolt_codegen_path = emf_src_path / 'revolt_codegen.py'
traits_codegen_path = emf_src_path / 'traits_codegen.py'
trait_notify_path = emf_src_path / 'trait-notify.pl'


def build_mapcut():
    print(">> attempting to build mapcut from source...")
    os.chdir(str(mapcut_path))
    try:
        output = subprocess.check_output(str(scons_bin_path), universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> scons failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        sys.exit(1)


def main():
    rc = 0

    if mapcut_bin_path_default.exists():
        mapcut_bin_path = mapcut_bin_path_default
    else:
        mapcut_bin = 'mapcut' if sys.platform.startswith('linux') or sys.platform.startswith('darwin') else 'mapcut.exe'
        mapcut_bin_path = mapcut_path / mapcut_bin

    if not mapcut_bin_path.exists():
        build_mapcut()
    if not mapcut_bin_path.exists():
        sys.stderr.write('mapcut binary not found: {}\n'.format(mapcut_bin_path))
        rc = 2

    print(">> executing mapcut...")
    try:
        output = subprocess.check_output([str(mapcut_bin_path), '--emf'] + cut_titles,
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> mapcut failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 3

    print(">> executing holding slot trigger generator...")
    try:
        output = subprocess.check_output(['/usr/bin/python3', str(emf_holding_slot_path)],
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> build failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 4

    print(">> executing EMF+SWMH history generator...")
    try:
        output = subprocess.check_output(['/usr/bin/python3', str(emf_swmh_history_path)],
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> build failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 5

    print(">> executing cadet codegen...")
    try:
        output = subprocess.check_output(['/usr/bin/python3', str(cadet_codegen_path)],
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> build failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 6

    print(">> executing religion codegen...")
    try:
        output = subprocess.check_output(['/usr/bin/python3', str(religion_codegen_path)],
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> build failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 7

    print(">> executing revolt codegen...")
    try:
        output = subprocess.check_output(['/usr/bin/python3', str(revolt_codegen_path)],
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> build failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 8

    print(">> executing traits codegen...")
    try:
        output = subprocess.check_output(['/usr/bin/python3', str(traits_codegen_path)],
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> build failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        rc = 9

    with version_path.open('w') as f:
        print('{} - {}'.format(version, datetime.date.today()), file=f)

    return rc


if __name__ == '__main__':
    sys.exit(main())
