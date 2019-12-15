#!/usr/bin/python3

from pathlib import Path
from localpaths import rootpath

emf_path = rootpath / 'EMF/EMF'
cloc_path = emf_path / 'localisation/customizable_localisation/emf_opinion_codegen_custom_loc.txt'
i18n_path = emf_path / 'localisation/1_emf_opinion_codegen.csv'

# Map code scope (which can be prefixed w/ persistent_event_target: or
# event_target: -- it'll be handled) to custom loc name of scope. I.e., for a
# key of 'event_target:emf_global_ai_conqueror', we might want a value of
# 'GlobalAIConqueror' and for a built-in scope like FROMFROM, we'd want [for
# consistency] to give a value of FromFrom.
opinion_of_scopes = {
	'ROOT':      'Root',
	'ROOT_FROM': 'RootFrom',
	'PREV':      'Prev',
	'PREVPREV':  'PrevPrev',
}

########################################################################################################################


def headers(files):
	note = 'NOTE: This file is code-generated and should NOT be edited directly: manual changes will be overwritten!'
	for t, f in files:
		if t == 'i18n':
			print('#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x', file=f)
			print('#' * (len(note) + 4), file=f);
			print('# {} #'.format(note), file=f);
			print('#' * (len(note) + 4), file=f);
		else:
			print('# -*- ck2.{} -*-\n'.format(t), file=f)
			print('# {}\n'.format(note), file=f);


def print_cloc(file, scope, named_scope, loc):
	loc['EMF_String_NA'] = '§YN/A§!'
	print('''
defined_text = {{
	name = EMF_GetOpinionOf{}
	text = {{
		localisation_key = EMF_String_NA
		trigger = {{
			character = {}
		}}
	}}'''.format(named_scope, scope), file=file)
	loc['EMF_String_Neg100'] = '§R-100§!'
	print('''\
	text = {{
		localisation_key = EMF_String_Neg100
		trigger = {{
			NOT = {{ opinion = {{ who = {} value = -99 }} }}
		}}
	}}'''.format(scope), file=file)

	for o in range(-99, 100):
		if o < 0:
			o_color = 'R'
			o_name = 'Neg{}'.format(-o)
		elif o == 0:
			o_color = 'Y'
			o_name = 'Zero'
		else:
			o_color = 'G'
			o_name = 'Pos{}'.format(o)

		key = 'EMF_String_{}'.format(o_name)
		loc[key] = '§{}{}§!'.format(o_color, o)
		print('''\
	text = {{
		localisation_key = {0}
		trigger = {{
			opinion = {{ who = {1} value = {2} }}
			NOT = {{ opinion = {{ who = {1} value = {3} }} }}
		}}
	}}'''.format(key, scope, o, o + 1), file=file)

	loc['EMF_String_Pos100'] = '§G100§!'
	print('''\
	text = {{
		localisation_key = EMF_String_Pos100
		trigger = {{
			opinion = {{ who = {} value = 100 }}
		}}
	}}
	fallback_text = {{
		localisation_key = EMF_String_NA
	}}
}}'''.format(scope), file=file)


####


with cloc_path.open('w', encoding='cp1252', newline='\n') as cf, \
	 i18n_path.open('w', encoding='cp1252', newline='\n') as lf:

	headers([('custom_loc', cf), ('i18n', lf)])

	loc = {}
	for s in opinion_of_scopes:
		print_cloc(cf, s, opinion_of_scopes[s], loc)

	for k in sorted(loc):
		print('{};{};;;;;;;;;;;;;x'.format(k, loc[k]), file=lf)
