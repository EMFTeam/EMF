#!/usr/bin/env python3

import sys
import ck2parser

emf_path = ck2parser.rootpath / 'EMF/EMF'
sr_modifier_path = emf_path / 'common/event_modifiers/emf_sr_codegen_modifiers.txt'
sr_effect_path = emf_path / 'common/scripted_effects/emf_sr_codegen_effects.txt'
sr_trigger_path = emf_path / 'common/scripted_triggers/emf_sr_codegen_triggers.txt'

###


def main():
	global g_religions
	g_religions = []
	parser = ck2parser.SimpleParser(emf_path)

	for _, tree in parser.parse_files('common/religions/*.txt'):
		for n, v in tree:
			if n.val.endswith('_trigger'):
				continue
			for n2, v2 in v:
				if isinstance(v2, ck2parser.Obj) and n2.val not in ['color', 'male_names', 'female_names']:
					if v2.has_pair('secret_religion', 'no'):
						continue
					g_religions.append(n2.val)

	# create SR community event modifiers
	with sr_modifier_path.open('w', encoding='cp1252') as f:
		print('''\
# -*- ck2.event_modifiers -*-

# NOTE: This file is code-generated. Ideally, do NOT modify this file by hand.

# For available modifier icons, see: common/event_modifiers/REFERENCE_emf_modifier_icons.txt
''', file=f)

		for r in g_religions:
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
		print_trigger_has_any_religion_char_flag(f)

	# generate SR scripted effects
	with sr_effect_path.open('w', encoding='cp1252') as f:
		print('''\
# -*- ck2.scripted_effects -*-

# These are code-generated & used as implementation for vanilla scripted effects. Ideally, don't modify by hand.
''', file=f)

		print_effect_set_sr_and_clr_religion_char_flag(f)
		print_effect_add_religion_char_flag(f)
		print_effect_clr_religion_char_flag(f)
		print_effect_event_target_old_religion_from_flag(f)
		print_effect_flip_secret_religious_community_provinces(f)

	return 0

def print_trigger_has_any_religion_char_flag(f):
	print('''
emf_sr_has_any_religion_char_flag = {
	OR = {''', file=f)

	for r in g_religions:
		print('\t\thas_character_flag = character_was_' + r, file=f)

	print('\t}\n}', file=f)


def print_effect_set_sr_and_clr_religion_char_flag(f):
	print('''
emf_sr_set_sr_and_clr_religion_char_flag = {''', file=f)

	for rel in g_religions:
		print('''\
	if = {{
		limit = {{
			OR = {{
				has_character_flag = character_was_{0}
				AND = {{
					religion = {0}
					emf_sr_has_any_religion_char_flag = no
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

	for rel in g_religions:
		print('\t\t{0} = {{ set_character_flag = character_was_{0} }}'.format(rel), file=f)

	print('\t}\n}', file=f)


def print_effect_clr_religion_char_flag(f):
	print('''
emf_sr_clr_religion_char_flag = {''', file=f)

	for rel in g_religions:
		print('\tclr_character_flag = character_was_{}'.format(rel), file=f)

	print('}', file=f)


def print_effect_event_target_old_religion_from_flag(f):
	print('''
emf_sr_event_target_old_religion_from_flag = {
	trigger_switch = {
		on_trigger = has_character_flag''', file=f)

	for rel in g_religions:
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

	for rel in g_religions:
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
