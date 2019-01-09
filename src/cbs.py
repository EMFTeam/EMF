#!/usr/bin/env python3

import sys
import ck2parser

mod_path = ck2parser.rootpath / 'EMF/EMF'


def main():
	for _, tree in ck2parser.SimpleParser().parse_files('common/cb_types/*.txt'):
		for n, v in tree:
			if isinstance(v, ck2parser.Obj):
				print(n.val)
	return 0


if __name__ == '__main__':
	sys.exit(main())
