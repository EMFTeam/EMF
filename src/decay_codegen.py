#!/usr/bin/python3

from pathlib import Path
from localpaths import rootpath

#TAB = ' ' * 4
TAB = '\t'

emf_path = rootpath / 'EMF/EMF'
effects_path = emf_path / 'common/scripted_effects/emf_decay_codegen_effects.txt'
modifiers_path = emf_path / 'common/event_modifiers/emf_decay_codegen_modifiers.txt'
i18n_path = emf_path / 'localisation/1_emf_decay_codegen.csv'

def vassal_min_levy(i):
	if i < 60: return 0
	return -0.6 * ((i-60) / 60)

def vassal_max_levy(i):
	return -0.6 * (i / 100)

def global_levy_size(i):
	if i < 20: return 0
	return -0.5 * ((i-20) / 80)

def levy_reinforce_rate(i):
	if i < 30: return 0
	return -0.7 * ((i-30) / 70)

def land_morale(i):
	return -0.5 * (i / 100)

def land_organisation(i):
	if i < 50: return 0
	return -0.2 * ((i-50) / 50)

def global_tax_modifier(i):
	return -0.5 * (i / 100)

def vassal_opinion(i):
	if i < 50: return 0
	return -20*(i-50) // 50

def defensive_plot_power_modifier(i):
	return -1.0 * (i / 100)

def retinuesize_perc(i):
	if i < 40: return 0
	return -2.0 * ((i-40) / 60)

DECIMAL = 0  # round to 3 decimal places (maximum)
INTEGER = 1  # truncate to integer

MODIFIERS = [
	('castle_vassal_min_levy',        vassal_min_levy,               DECIMAL),
	('city_vassal_min_levy',          vassal_min_levy,               DECIMAL),
	('temple_vassal_min_levy',        vassal_min_levy,               DECIMAL),
	('tribal_vassal_min_levy',        vassal_min_levy,               DECIMAL),
	('castle_vassal_max_levy',        vassal_max_levy,               DECIMAL),
	('city_vassal_max_levy',          vassal_max_levy,               DECIMAL),
	('temple_vassal_max_levy',        vassal_max_levy,               DECIMAL),
	('tribal_vassal_max_levy',        vassal_max_levy,               DECIMAL),
	('global_levy_size',              global_levy_size,              DECIMAL),
	('levy_reinforce_rate',           levy_reinforce_rate,           DECIMAL),
	('land_morale',                   land_morale,                   DECIMAL),
	('land_organisation',             land_organisation,             DECIMAL),
	('global_tax_modifier',           global_tax_modifier,           DECIMAL),
	('vassal_opinion',                vassal_opinion,                INTEGER),
	('defensive_plot_power_modifier', defensive_plot_power_modifier, DECIMAL),
	('retinuesize_perc',              retinuesize_perc,              DECIMAL),
]


def headers(files):
	note = 'NOTE: This file is code-generated and should NOT be edited manually.'
	for t, f in files:
		if t == 'i18n':
			print('#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x', file=f)
			print('#' * (len(note) + 4), file=f);
			print('# {} #'.format(note), file=f);
			print('#' * (len(note) + 4), file=f);
		else:
			print('# -*- ck2.{} -*-\n'.format(t), file=f)
			print('# {}\n'.format(note), file=f);


def define_modifiers(f):
	for i in range(101):
		print('emf_decay_modifier_{} = {{'.format(i), file=f)
		for name, func, value_type in MODIFIERS:
			val = func(i)
			if value_type == DECIMAL:
				val = round(val, 3)
			elif value_type == INTEGER:
				val = int(val)
			if val < -0.0009 or val > 0.0009:
				print('{}{} = {}'.format(TAB,name, val), file=f)
		icon = 28 if i > 0 else 10
		print('{}icon = {}'.format(TAB, icon), file=f)
		print('}', file=f)


def localisation(f):
	desc = '''\
An empire is a hard thing to hold together. The massive bureaucracy can become corrupt, and the sheer difficulty in sending messages across such a large expanse can lead to its own kind of entropy. Imperial Decay measures that entropy, and increases each time the title changes hands based on how large and centralized the empire has become.\\n\\nImperial Decay is §Rincreased§! by:\\n(§Y*§!) The title changing hands (more if it is usurped)\\n(§Y*§!) Crown authority is low\\n(§Y*§!) Having a very large realm\\n(§Y*§!) Losing crusades and holy wars\\n(§Y*§!) Losing against major invasions\\n(§Y*§!) Random events caused by a poor ruler or regent\\n\\nImperial Decay can be §Greduced§! by:\\n(§Y*§!) Becoming coronated\\n(§Y*§!) Crown authority is high\\n(§Y*§!) The realm is overthrown by an internal revolt\\n(§Y*§!) Holding a tournament/furusiyya\\n(§Y*§!) Using the 'Lower Imperial Decay' decision\\n(§Y*§!) Winning crusades and holy wars\\n(§Y*§!) Winning major invasions and rebellions\\n(§Y*§!) Enforcing imperial de jure claims\\n(§Y*§!) Random events caused by a good ruler or regent'''
	eot = ';;;;;;;;;;;;;x'
	for i in range(101):
		print('emf_decay_modifier_{0};Imperial Decay: {0}%{1}'.format(i, eot), file=f)
		print('emf_decay_modifier_{}_desc;{}{}'.format(i, desc, eot), file=f)


def remove_modifier_effect(f):
	print('\nemf_remove_decay_modifier = {', file=f)
	for i in range(101):
		print('{}remove_character_modifier = emf_decay_modifier_{}'.format(TAB, i), file=f)
	print('}', file=f)


def add_modifier_effect(f):
	print('\nemf_add_decay_modifier = {', file=f)
	print('{}if = {{'.format(TAB), file=f)
	print('{}limit = {{ primary_title = {{ NOT = {{ check_variable = {{ which = "imperial_decay" value = 1 }} }} }} }}'.format(TAB*2), file=f)
	print('{}add_character_modifier = {{ name = emf_decay_modifier_0 duration = -1 }}'.format(TAB*2), file=f)
	print(TAB*2 + '}', file=f)
	for i in range(1, 101):
		print(TAB + 'if = {', file=f)
		print('{}limit = {{ primary_title = {{ is_variable_equal = {{ which = "imperial_decay" value = {} }} }} }}'.format(TAB*2, i), file=f)
		print('{}add_character_modifier = {{ name = emf_decay_modifier_{} duration = -1 }}'.format(TAB*2, i), file=f)
		print(TAB + '}', file=f)
	print('}', file=f)


def round_effect(f, name, var, min_v, max_v):
	print('\n# THIS = empire title, effect supports rounding and clamping into range [{},{}]'.format(min_v, max_v), file=f)
	print('{} = {{'.format(name), file=f)
	for i in range(min_v, max_v+1):
		below = i - 0.5
		above = i + 0.5
		print(TAB + 'if = {', file=f)
		print(TAB*2 + 'limit = {', file=f)
		if i > min_v:
			print('{}check_variable = {{ which = "{}" value = {} }}'.format(TAB*3, var, below), file=f)
		if i < max_v:
			print('{}NOT = {{ check_variable = {{ which = "{}" value = {} }} }}'.format(TAB*3, var, above), file=f)
		print(TAB*2 + '}', file=f)
		print('{}set_variable = {{ which = "{}" value = {} }}'.format(TAB*2, var, i), file=f)
		print(TAB + '}', file=f)
	print('}', file=f)



with effects_path.open('w', encoding='cp1252', newline='\n') as ef, \
	 modifiers_path.open('w', encoding='cp1252', newline='\n') as mf, \
	 i18n_path.open('w', encoding='cp1252', newline='\n') as lf:
	headers([('scripted_effects', ef), ('event_modifiers', mf), ('i18n', lf)])
	define_modifiers(mf)
	localisation(lf)
	remove_modifier_effect(ef)
	add_modifier_effect(ef)
	round_effect(ef, 'emf_normalize_decay_change_on_new_holder', 'imperial_decay_change', 1, 25)
	round_effect(ef, 'emf_normalize_decay', 'imperial_decay', 0, 100)

