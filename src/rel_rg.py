#!/usr/bin/env python3

import sys
import ck2parser

from collections import defaultdict

emf_path = ck2parser.rootpath / 'EMF/EMF'

###

TAB = '\t'


def main():
	opt_rel = True

	if 'groups' in sys.argv[1:]:
		opt_rel = False

	religions = []
	rg_map = defaultdict(list)

	for _, tree in ck2parser.SimpleParser(emf_path).parse_files('common/religions/*.txt'):
		for n, v in tree:
			if n.val.endswith('_trigger'):
				continue
			for n2, v2 in v:
				if isinstance(v2, ck2parser.Obj) and n2.val not in ['interface_skin', 'color', 'male_names', 'female_names']:
					# if v2.has_pair('secret_religion', 'no'):
					# 	continue
					religions.append(n2.val)
					rg_map[n.val].append(n2.val)

#	rg_map['pagan_group'].append('bon_reformed')
#	rg_map['pagan_group'].append('hellenic_pagan_reformed')

	if opt_rel:
		for r in sorted(religions):
			print(r)
	else:
		for rg in sorted(rg_map.keys()):
			print(rg)

	# for rg in sorted(rg_map.keys()):
	# 	print("{}:".format(rg))
	# 	for r in sorted(rg_map[rg]):
	# 		print("{}{}".format(TAB, r))

	return 0


if __name__ == '__main__':
	sys.exit(main())
