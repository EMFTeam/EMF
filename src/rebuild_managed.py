#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess
from pathlib import Path

from localpaths import rootpath

# this script shall be invoked by hiphub when certain files change in the EMF repository due to a commit.
# at this time, that is just EMF+SWMH/map/geographical_region.txt.  we invoke the same program that cuts
# SWMH into MiniSWMH with a special option to tell it to only generate EMF+MiniSWMH/map/geographical_region.txt
# from the aforementioned file rather than do its full set of operations.

version = 'v7.01-BETA'
version_path = rootpath / 'EMF/EMF/version.txt'

scons_bin_path = Path('/usr/bin/scons')
mapcut_bin_path_default = Path('/usr/local/bin/mapcut')
mapcut_path = rootpath / 'ck2utils/mapcut'
cut_titles = ['e_rajastan', 'e_mali', 'k_sahara', 'k_fezzan', 'k_kanem', 'k_hausaland']

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
    if sys.platform.startswith('linux') and mapcut_bin_path_default.exists():
        mapcut_bin_path = mapcut_bin_path_default
    else:
        mapcut_bin = 'mapcut' if sys.platform.startswith('linux') else 'mapcut.exe'
        mapcut_bin_path = mapcut_path / mapcut_bin

    if not mapcut_bin_path.exists():
        build_mapcut()
    if not mapcut_bin_path.exists():
        sys.stderr.write('mapcut binary not found: {}\n'.format(mapcut_bin_path))
        return 2

    print(">> executing mapcut...")

    try:
        output = subprocess.check_output([str(mapcut_bin_path), '--emf'] + cut_titles,
                                         universal_newlines=True, stderr=subprocess.STDOUT)
        if sys.stdout:
            sys.stdout.write(output)
    except subprocess.CalledProcessError as e:
        sys.stderr.write('> mapcut failed!\n> command: {}\n> exit code: {}\n\n{}'.format(e.cmd, e.returncode, e.output))
        return 3

    with version_path.open('w') as f:
        print('{} - {}'.format(version, datetime.date.today()), file=f)

    return 0


if __name__ == '__main__':
    sys.exit(main())
