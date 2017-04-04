#!/usr/bin/env python3

import sys
from pathlib import Path

from localpaths import rootpath

sr_modifier_path = rootpath / 'EMF/EMF/common/event_modifiers/emf_sr_modifiers.txt'

emf_religions = [
	'adoptionist',
	'arian',
	'syriac',
	'maronite',
	'apostolic',
	'tondrakian',
	'mahdiyya',
	'nabawiyya',
	'haruri',
	'waqifi',
	'zaydi',
	'ismaili',
	'qarmatian',
	'east_african_pagan',
	'east_african_pagan_reformed',
	'zurvanist',
	'mandaean',
]

modifier_file_hdr = '''\
# -*- ck2.event_modifiers -*-

# For available modifier icons, see: common/event_modifiers/REFERENCE_emf_modifier_icons.txt
'''

def main():
	with sr_modifier_path.open('w', encoding='cp1252') as f:
		print(modifier_file_hdr, file=f)

		for r in emf_religions:
			print('''\
secret_{0}_community = {{
	icon = 18
	is_visible = {{
		society_member_of = secret_religious_society_{0}
	}}
}}'''.format(r), file=f)

	return 0


if __name__ == '__main__':
	sys.exit(main())
