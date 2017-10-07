#!/usr/bin/python3

from pathlib import Path
from localpaths import rootpath

emf_path = rootpath / 'EMF/EMF'
effects_path = emf_path / 'common/scripted_effects/emf_relsub_codegen_effects.txt'
modifiers_path = emf_path / 'common/event_modifiers/emf_relsub_codegen_modifiers.txt'
i18n_path = emf_path / 'localisation/1_emf_relsub_codegen.csv'

N = 20  # number of relsub unrest modifier steps

class Modifier:
	def __init__(self, name, slope, offset=0, min=-1000, max=1000, integer_valued=False):
		self._name = name
		self._m = slope
		self._b = offset
		self._min = min_value
		self._max = max_value
		self._int_mode = integer_valued

	def name():
		return self._name

	def slope():
		return self._m

	def offset():
		return self._b

	def is_integer_valued():
		return self._int_mode

	def __call__(self, i):
		val = i * self._m + self._b
		val = min(
		return int(val) if self._int_mode else round(val, 3)



DECIMAL = 0  # round to 3 decimal places (maximum)
INTEGER = 1  # truncate to integer

MODIFIERS = {
	'light': [
		Modifier('local_revolt_risk', 0.04, 0.1),
		Modifier('levy_size', -0.2, -0.2, min=-2),
		Modifier('levy_reinforce_rate', -0.2, min=-2),
		Modifier('local_tax_modifier', -0.2, -0.2, min=-2),
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
	('retinue_size_perc',             retinue_size_perc,             DECIMAL),
}


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
				print('\t{} = {}'.format(name, val), file=f)
		icon = 28 if i > 0 else 10
		print('\ticon = {}'.format(icon), file=f)
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
		print('\tremove_character_modifier = emf_decay_modifier_{}'.format(i), file=f)
	print('}', file=f)


def add_modifier_effect(f):
	print('\nemf_add_decay_modifier = {', file=f)
	print('\tif = {', file=f)
	print('\t\tlimit = { primary_title = { NOT = { check_variable = { which = "imperial_decay" value = 1 } } } }', file=f)
	print('\t\tadd_character_modifier = { name = emf_decay_modifier_0 duration = -1 }', file=f)
	print('\t}', file=f)
	for i in range(1, 101):
		print('\tif = {', file=f)
		print('\t\tlimit = {{ primary_title = {{ is_variable_equal = {{ which = "imperial_decay" value = {} }} }} }}'.format(i), file=f)
		print('\t\tadd_character_modifier = {{ name = emf_decay_modifier_{} duration = -1 }}'.format(i), file=f)
		print('\t}', file=f)
	print('}', file=f)


def round_effect(f, name, var, min_v, max_v):
	print('\n# THIS = empire title, effect supports rounding and clamping into range [{},{}]'.format(min_v, max_v), file=f)
	print('{} = {{'.format(name), file=f)
	for i in range(min_v, max_v+1):
		below = i - 0.5
		above = i + 0.5
		print('\tif = {', file=f)
		print('\t\tlimit = {', file=f)
		if i > min_v:
			print('\t\t\tcheck_variable = {{ which = "{}" value = {} }}'.format(var, below), file=f)
		if i < max_v:
			print('\t\t\tNOT = {{ check_variable = {{ which = "{}" value = {} }} }}'.format(var, above), file=f)
		print('\t\t}', file=f)
		print('\t\tset_variable = {{ which = "{}" value = {} }}'.format(var, i), file=f)
		print('\t}', file=f)
	print('}', file=f)



with effects_path.open('w', encoding='cp1252') as ef, \
	 modifiers_path.open('w', encoding='cp1252') as mf, \
	 i18n_path.open('w', encoding='cp1252') as lf:
	headers([('scripted_effects', ef), ('event_modifiers', mf), ('i18n', lf)])
	define_modifiers(mf)
	localisation(lf)
	remove_modifier_effect(ef)
	add_modifier_effect(ef)
	round_effect(ef, 'emf_normalize_decay_change_on_new_holder', 'imperial_decay_change', 1, 25)
	round_effect(ef, 'emf_normalize_decay', 'imperial_decay', 0, 100)

