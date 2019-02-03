#!/usr/bin/python3

import sys
import ck2parser

g_emf_path = ck2parser.rootpath / 'EMF/EMF'

###


def main():
	moddirs = (g_emf_path,)
	parser = ck2parser.SimpleParser(*moddirs)
	loc = ck2parser.get_localisation(moddirs=moddirs)
	for _, tree in parser.parse_files('common/traits/*.txt'):
		for n, v in tree:
			for n2, v2 in v:
				try:
					if n2.val == 'inherit_chance':
						loc_val = loc.get(n.val)
						loc_val = ' # ' + loc_val if loc_val else ''
						print('''\
if = {{
	limit = {{ trait = {0} }}{2}
	random = {{ chance = {1} PREV = {{ add_trait = {0} }} }}
}}'''.format(n.val, v2.val, loc_val))
				except:
					pass
	return 0


###


if __name__ == '__main__':
	sys.exit(main())
