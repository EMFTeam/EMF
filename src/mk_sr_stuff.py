#!/usr/bin/env python3

import sys
from pathlib import Path

from localpaths import rootpath

emf_path = rootpath / 'EMF/EMF'
sr_modifier_path = emf_path / 'common/event_modifiers/emf_sr_modifiers.txt'
sr_effect_path = emf_path / 'common/scripted_effects/emf_sr_codegen_effects.txt'
sr_trigger_path = emf_path / 'common/scripted_triggers/emf_sr_codegen_triggers.txt'

# TODO: learn escalona's python parser interface (unless I create python bindings for my C++ parser)
# and grab this information (e.g., religions) automatically.  learning that was slower than just
# writing it out for now, but in the long-term, the code should change when the religion files change
# automatically.

# NOTE: religions without secret-religion cults are not included: ((hellenic_)?pagan)|hip_religion

vanilla_religions = [
	'catholic',
	'cathar',
	'fraticelli',
	'waldensian',
	'lollard',
	'orthodox',
	'bogomilist',
	'monothelite',
	'iconoclast',
	'miaphysite',
	'monophysite',
	'paulician',
	'nestorian',
	'messalian',
	'sunni',
	'zikri',
	'ibadi',
	'kharijite',
	'shiite',
	'hurufi',
	'druze',
	'norse_pagan_reformed',
	'norse_pagan',
	'tengri_pagan_reformed',
	'tengri_pagan',
	'baltic_pagan_reformed',
	'baltic_pagan',
	'finnish_pagan_reformed',
	'finnish_pagan',
	'aztec_reformed',
	'aztec',
	'slavic_pagan_reformed',
	'slavic_pagan',
	'west_african_pagan_reformed',
	'west_african_pagan',
	'zun_pagan_reformed',
	'zun_pagan',
	'zoroastrian',
	'mazdaki',
	'manichean',
	'yazidi',
	'jewish',
	'samaritan',
	'karaite',
	'hindu',
	'buddhist',
	'jain',
]

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

all_religions = vanilla_religions + emf_religions


def main():
	# create extra event modifiers
	with sr_modifier_path.open('w', encoding='cp1252') as f:
		print('''\
# -*- ck2.event_modifiers -*-

# For available modifier icons, see: common/event_modifiers/REFERENCE_emf_modifier_icons.txt
''', file=f)

		for r in emf_religions:
			print('''\
secret_{0}_community = {{
	icon = 18
	is_visible = {{
		society_member_of = secret_religious_society_{0}
	}}
}}'''.format(r), file=f)


	# generate SR scripted triggers
	with sr_trigger_path.open('w', encoding='cp1252') as f:
		print('''\
# -*- ck2.scripted_triggers -*-

# These are code-generated & used as implementation for vanilla scripted triggers. Ideally, don't modify by hand.
''', file=f)
		print_trigger_has_any_sr_flag(f)

	# generate SR scripted effects
	with sr_effect_path.open('w', encoding='cp1252') as f:
		print('''\
# -*- ck2.scripted_effects -*-

# These are code-generated & used as implementation for vanilla scripted effects. Ideally, don't modify by hand.
''', file=f)

		print_effect_set_sr_and_clear_its_flag(f)
		print_effect_add_religion_char_flag(f)
		print_effect_clr_religion_char_flag(f)
		print_effect_event_target_old_religion_from_flag(f)
		print_effect_flip_secret_religious_community_provinces(f)

	return 0

def print_trigger_has_any_sr_flag(f):
	print('''
emf_sr_has_any_sr_flag = {
	OR = {''', file=f)

	for r in all_religions:
		print('\t\thas_character_flag = character_was_' + r, file=f)

	print('\t}\n}', file=f)


def print_effect_set_sr_and_clear_its_flag(f):
	print('''
emf_sr_set_sr_and_clear_its_flag = {''', file=f)

	for rel in all_religions:
		print('''\
	if = {{
		limit = {{
			OR = {{
				has_character_flag = character_was_{0}
				AND = {{
					religion = {0}
					emf_sr_has_any_sr_flag = no
				}}
			}}
		}}
		set_secret_religion = {0}
		clr_character_flag = character_was_{0}
		break = yes
	}}'''.format(rel), file=f)

	print('}', file=f)


def print_effect_add_religion_char_flag(f):
	print('''
emf_sr_add_religion_char_flag = {
	trigger_switch = {
		on_trigger = religion''', file=f)

	for rel in all_religions:
		print('\t\t{0} = {{ set_character_flag = character_was_{0} }}'.format(rel), file=f)

	print('\t}\n}', file=f)


def print_effect_clr_religion_char_flag(f):
	print('''
emf_sr_clr_religion_char_flag = {''', file=f)

	for rel in all_religions:
		print('\tclr_character_flag = character_was_{}'.format(rel), file=f)

	print('}', file=f)


def print_effect_event_target_old_religion_from_flag(f):
	print('''
emf_sr_event_target_old_religion_from_flag = {
	trigger_switch = {
		on_trigger = has_character_flag''', file=f)

	for rel in all_religions:
		print('''\
		character_was_{0} = {{
			random_character = {{ limit = {{ religion = {0} }} save_event_target_as = old_religion }}
		}}'''.format(rel), file=f)

	print('\t}\n}', file=f)


def print_effect_flip_secret_religious_community_provinces(f):
	print('''
emf_sr_flip_secret_religious_community_provinces = {
	trigger_switch = {
		on_trigger = society_member_of''', file=f)

	for rel in all_religions:
		print('''\
		secret_religious_society_{0} = {{
			ROOT = {{
				any_demesne_province = {{
					limit = {{ has_province_modifier = secret_{0}_community }}
					religion = {0}
					remove_province_modifier = secret_{0}_community
				}}
			}}
		}}'''.format(rel), file=f)

	print('\t}\n}', file=f)


if __name__ == '__main__':
	sys.exit(main())
