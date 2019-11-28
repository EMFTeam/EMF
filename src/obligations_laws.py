#!/usr/bin/python3

############################################################
# Copyright (C) 2019 Matthew D. Hall <zijistark@gmail.com> #
#                                                          #
# Free for personal modification. Any redistribution, even #
# without modification, of this program OR its output is   #
# expressly forbidden without the consent of the author.   #
############################################################

VERSION = '2.0.0-dev'

import sys
import argparse
import pytz
from datetime import datetime
from pathlib import Path
from tabulate import tabulate # `pip3 install tabulate`


########################################################################################################################


DEF_MOD_PATH = Path('./EMF')  # If your working directory is the EMF repository root, this refers to base EMF.
DEF_LAWS_FILE = Path('emf_obligations_laws.txt')

# Maximum possible range of combined max_levy modifiers for any given vassal type
DEF_MIN_TOTAL_MAX_LEVY = -0.075
DEF_MAX_TOTAL_MAX_LEVY = 0.3

# Mapping of vassal types to default vassal_max_levy to vassal_tax_modifier conversion ratio
DEF_TAX_PER_LEVY = {
  'feudal': 0.8,
  'iqta':   1.0,
  'temple': 1.2,
  'city':   1.4,
  'tribal': 0.6,
}

# Mapping of vassal types to default laws (zero-indexed) for Obligations and Focus, respectively
DEF_LAWS = {
  'feudal': (0, 0),
  'iqta':   (1, 2),
  'temple': (0, 2),
  'city':   (0, 3),
  'tribal': (0, 0),
}

# Mapping of vassal types to vassal opinion linear modifier function of law tier in tuple form of (slope, y-intercept)
# or (m, b), for y = mx + b (y is opinion & x is zero-indexed law tier)
DEF_OPINION = {
  'feudal': (-5, 0),
  'iqta':   (-5, 0),
  'temple': (-5, 0),
  'city':   (-5, 0),
  'tribal': (-5, 0),
}

# Same form of (m, b) for y=mx+b where y is the min_levy modifier and x is the zero-indexed law tier (we don't currently
# make any distinctions between the vassal classes when it comes to min_levy):
DEF_OBLIGATIONS_MIN_LEVY = (  0.05, -0.05)
DEF_FOCUS_MIN_LEVY       = (-0.025,  0.05)

# We know this (implicitly in most of the script), but it's nice to name it where we can:
N_LAWS = 5


########################################################################################################################


def get_args():
  parser = argparse.ArgumentParser(description="Generate EMF vassal contract (Obligations & Focus) demesne laws.")
  parser.add_argument('-n', '--dry-run', action='store_true',
                      help='print a summary of the calculated law modifiers, but don\'t modify any files')
  parser.add_argument('-m', '--mod-path', default=str(DEF_MOD_PATH),
                      help='path to root folder of mod, under which files will be generated [default: %(default)s]')
  parser.add_argument('-o', '--laws-file', default=str(DEF_LAWS_FILE),
                      help='path to root folder of mod, under which files will be generated [default: %(default)s]')
  parser.add_argument('--min-max-levy', default=DEF_MIN_TOTAL_MAX_LEVY,
                      help='minimum possible net max_levy modifier from these laws [default: %(default)s]')
  parser.add_argument('--max-max-levy', default=DEF_MAX_TOTAL_MAX_LEVY,
                      help='maximum possible net max_levy modifier from these laws [default: %(default)s]')
  parser.add_argument('--obligations-min-levy-slope', default=DEF_OBLIGATIONS_MIN_LEVY[0],
                      help='rate of change of min_levy modifier per Obligations law tier [default: %(default)s]')
  parser.add_argument('--obligations-min-levy-base', default=DEF_OBLIGATIONS_MIN_LEVY[1],
                      help='y-intercept of min_levy modifier for Focus law groups [default: %(default)s]')
  parser.add_argument('--focus-min-levy-slope', default=DEF_FOCUS_MIN_LEVY[0],
                      help='rate of change of min_levy modifier per Focus law tier [default: %(default)s]')
  parser.add_argument('--focus-min-levy-base', default=DEF_FOCUS_MIN_LEVY[1],
                      help='y-intercept of min_levy modifier for Focus law groups [default: %(default)s]')
  parser.add_argument('--feudal-tax-per-levy', default=DEF_TAX_PER_LEVY['feudal'],
                      help='rate at which max_levy can convert to tax_modifier [default: %(default)s]')
  parser.add_argument('--iqta-tax-per-levy', default=DEF_TAX_PER_LEVY['iqta'],
                      help='rate at which max_levy can convert to tax_modifier [default: %(default)s]')
  parser.add_argument('--temple-tax-per-levy', default=DEF_TAX_PER_LEVY['temple'],
                      help='rate at which max_levy can convert to tax_modifier [default: %(default)s]')
  parser.add_argument('--city-tax-per-levy', default=DEF_TAX_PER_LEVY['city'],
                      help='rate at which max_levy can convert to tax_modifier [default: %(default)s]')
  parser.add_argument('--tribal-tax-per-levy', default=DEF_TAX_PER_LEVY['tribal'],
                      help='rate at which max_levy can convert to tax_modifier [default: %(default)s]')
  parser.add_argument('--version', '-V', action='version', version='%(prog)s '+VERSION,
                      help='show program version and quit')
  return parser.parse_args()


########################################################################################################################


class VassalType:
  def __init__(self, name, tax_per_levy=None, default_ob_law=None, default_foc_law=None,
               opinion_slope=None, opinion_base=None,
               ob_min_levy_slope=None, ob_min_levy_base=None, foc_min_levy_slope=None, foc_min_levy_base=None,
               law_function=None):
    self.name = name
    self.tax_per_levy = tax_per_levy if tax_per_levy is not None else DEF_TAX_PER_LEVY[name]
    self.default_ob_law = default_ob_law if default_ob_law is not None else DEF_LAWS[name][0]
    self.default_foc_law = default_foc_law if default_foc_law is not None else DEF_LAWS[name][1]
    self.opinion_slope = opinion_slope if opinion_slope is not None else DEF_OPINION[name][0]
    self.opinion_base = opinion_base if opinion_base is not None else DEF_OPINION[name][1]
    self.ob_min_levy_slope = ob_min_levy_slope if ob_min_levy_slope is not None else DEF_OBLIGATIONS_MIN_LEVY[0]
    self.ob_min_levy_base = ob_min_levy_base if ob_min_levy_base is not None else DEF_OBLIGATIONS_MIN_LEVY[1]
    self.foc_min_levy_slope = foc_min_levy_slope if foc_min_levy_slope is not None else DEF_FOCUS_MIN_LEVY[0]
    self.foc_min_levy_base = foc_min_levy_base if foc_min_levy_base is not None else DEF_FOCUS_MIN_LEVY[1]
    self.law_function = law_function
    self.base_type = 'castle' if name == 'feudal' or name == 'iqta' else name
    self.gov_type = name
    if name == 'iqta':
      self.gov_type = 'feudal'
    elif name == 'temple':
      self.gov_type = 'theocracy'
    elif name == 'city':
      self.gov_type = 'republic'
    self.gov_trigger = 'is_' + self.gov_type
    self.opinion_type = '{}_opinion'.format(name) if self.gov_type != 'feudal' else 'feudal_opinion'


class LawFunction:
  def __init__(self, vtype, min_max_levy, max_max_levy):
    self.vtype = vtype
    self.min_max_levy = min_max_levy
    self.max_levy_range = max_max_levy - min_max_levy
    self.max_levy_tradeoff = self.max_levy_range / N_LAWS

  def focus(self, law):
    max_levy_delta = law * 2 * self.max_levy_tradeoff / (N_LAWS - 1)
    max_levy = self.max_levy_tradeoff - max_levy_delta
    return {
      'max_levy': max_levy,
      'min_levy': self.vtype.foc_min_levy_base + self.vtype.foc_min_levy_slope * law,
      'tax_modifier': max_levy_delta * self.vtype.tax_per_levy,
    }

  def obligations(self, law):
    max_levy_per_law = (self.max_levy_range - 2 * self.max_levy_tradeoff) / (N_LAWS - 1)
    max_levy = self.min_max_levy + self.max_levy_tradeoff + max_levy_per_law * law
    return {
      'max_levy': max_levy,
      'min_levy': self.vtype.ob_min_levy_base + self.vtype.ob_min_levy_slope * law,
      'tax_modifier': max_levy * self.vtype.tax_per_levy,
      'opinion': self.vtype.opinion_base + self.vtype.opinion_slope * law,
    }


########################################################################################################################


def main():
  args = get_args()
  mod_path = Path(args.mod_path)

  if not mod_path.is_dir():
    print('Fatal: Path to mod root directory is not a directory or does not exist (see: -m, --mod-path)', file=sys.stderr)
    return 1

  law_folder_path = mod_path / 'common/laws'
  law_folder_path.mkdir(parents=True, exist_ok=True)
  law_path = law_folder_path / args.laws_file

  min_levy_params = { # Since they don't vary by vassal type [currently], marshal these args into a dict for reuse:
    'ob_min_levy_slope': float(args.obligations_min_levy_slope),
    'ob_min_levy_base': float(args.obligations_min_levy_base),
    'foc_min_levy_slope': float(args.focus_min_levy_slope),
    'foc_min_levy_base': float(args.focus_min_levy_base),
  }

  vassal_types = [
    VassalType('feudal', tax_per_levy=float(args.feudal_tax_per_levy), **min_levy_params),
    VassalType('iqta',   tax_per_levy=float(args.iqta_tax_per_levy), **min_levy_params),
    VassalType('temple', tax_per_levy=float(args.temple_tax_per_levy), **min_levy_params),
    VassalType('city',   tax_per_levy=float(args.city_tax_per_levy), **min_levy_params),
    VassalType('tribal', tax_per_levy=float(args.tribal_tax_per_levy), **min_levy_params),
  ]

  for vt in vassal_types:
    vt.law_function = LawFunction(vt, float(args.min_max_levy), float(args.max_max_levy))
  
  if args.dry_run:
    print_summary(vassal_types, args, sys.stdout)
    return 0

  with law_path.open('w', encoding='cp1252', newline='\n') as of:
    print('# -*- ck2.laws -*-', file=of)
    print(file=of)
    print_summary(vassal_types, args, of)
    print_law_groups(vassal_types, of)
    print_laws(vassal_types, of)

  return 0


def print_summary(vassal_types, args, file):
  cmt = '# ' if file != sys.stdout and file != sys.stderr else ''
  if cmt:
    now = datetime.now(pytz.timezone('America/Los_Angeles'))
    print('#' * 92, file=file)
    print(cmt + 'DEMESNE LAWS: OBLIGATIONS & FOCUS', file=file)
    print(cmt, file=file)
    print(cmt + 'Generated by /EMF/src/obligations_laws.py on {} (Pacific Time).'.format(now.ctime()), file=file)
    print(cmt + 'DO NOT MANUALLY ALTER THIS FILE! YOUR CHANGES WILL BE OVERWRITTEN!', file=file)
    print('#' * 92, file=file)
    print(file=file)
  print(cmt + 'PARAMETER SUMMARY:', file=file)
  print(cmt, file=file)
  print(cmt + 'Smallest possible max_levy modifier: {}'.format(args.min_max_levy), file=file)
  print(cmt + 'Greatest possible max_levy modifier: {}'.format(args.max_max_levy), file=file)
  print(cmt, file=file)
  print(cmt + 'max_levy modifier to tax modifier conversion rate per vassal class:', file=file)
  for vt in vassal_types:
    print(cmt + '  {:8s} {}'.format(vt.name.capitalize() + ':', vt.tax_per_levy), file=file)
  print(cmt, file=file)
  print(cmt + 'min_levy modifier as function of zero-indexed Obligations law (L) per vassal class:', file=file)
  for vt in vassal_types:
    print(cmt + '  {:8s} min_levy = {} + {}*L'.format(vt.name.capitalize() + ':', vt.ob_min_levy_base, vt.ob_min_levy_slope), file=file)
  print(cmt, file=file)
  print(cmt + 'min_levy modifier as function of zero-indexed Focus law (L) per vassal class:', file=file)
  for vt in vassal_types:
    print(cmt + '  {:8s} min_levy = {} + {}*L'.format(vt.name.capitalize() + ':', vt.foc_min_levy_base, vt.foc_min_levy_slope), file=file)

  tbl_hdr = ["Modifier", "Law I", "Law II", "Law III", "Law IV", "Law V"]

  for vt in vassal_types:
    for is_focus in (True, False):
      modifier_types = ['max_levy', 'min_levy', 'tax_modifier']
      if not is_focus:
        modifier_types.append('opinion')
        # Normalize Obligations minimum tax modifier to zero at base law level; ergo, we'll need this offset:
        min_tax_offset = vt.law_function.obligations(0).get('tax_modifier', 0)

      rows = []

      for mt in modifier_types:
        row = [mt,]
        for law in range(N_LAWS):
          modifiers = vt.law_function.focus(law) if is_focus else vt.law_function.obligations(law)
          if is_focus or mt != 'tax_modifier':
            val = modifiers.get(mt, 0.0)
          else:
            val = modifiers.get(mt, 0.0) - min_tax_offset
          row.append(val if mt == 'opinion' else '{:+4.2f}%'.format(val * 100.0))
        rows.append(row)

      print('''
{}+------------------------>
{}| {} {}'''.format(cmt, cmt, vt.name.upper(), ('focus' if is_focus else 'obligations').upper()), file=file)
      print(cmt + tabulate(rows, tbl_hdr, tablefmt="psql").replace('\n', '\n' + cmt).rstrip('# '), file=file)
    print(file=file)


def print_law_groups(vtypes, f):

  print('law_groups = {', file=f)
  for vt in vtypes:
    print(tabs('''\
  {0}_slider = {{
    law_type = obligations
    left_value = LEVY
    right_value = TAX
    slider_sprite = GFX_focus_slider
    allowed_for_councillors = no
  }}
  {0}_obligations = {{
    law_type = obligations
    left_value = emf_laws_text_obligations_min
    right_value = emf_laws_text_obligations_max
    slider_sprite = GFX_oblig_{0}_slider
    allowed_for_councillors = yes
  }}''').format(vt.name), file=f)
  print('}', file=f)


def print_laws(vtypes, f):
  print('laws = {', file=f)
  at_start = True
  for vt in vtypes:
    for focus in (True, False):
      modifier_types = ['max_levy', 'min_levy', 'tax_modifier']
      min_tax_offset = 0

      if not focus:
        modifier_types.append('opinion')
        # Normalize Obligations minimum tax modifier to zero at base law level; ergo, we'll need this offset:
        min_tax_offset = vt.law_function.obligations(0).get('tax_modifier', 0)

      for law in range(N_LAWS):
        # Some law naming:
        law_group = fmt_law_group(vt, focus)
        law_name = fmt_law_name(vt, law, focus)
        next_law_name = fmt_law_name(vt, law + 1, focus) if law < N_LAWS-1 else ''
        prev_law_name = fmt_law_name(vt, law - 1, focus) if law > 0 else ''

        st = {} # Will hold some of the strings we build for interpolation later
        st['group'] = law_group
        st['law'] = law_name
        st['next_law'] = next_law_name
        st['prev_law'] = prev_law_name

        # Build modifiers string:
        modifiers = vt.law_function.focus(law) if focus else vt.law_function.obligations(law)
        st['law_modifiers'] = ''

        for mt in modifier_types:
          val = modifiers.get(mt, 0)
          if mt == 'tax_modifier':
            val -= min_tax_offset
          if val <= -1e-4 or val >= 1e-4:
            st['law_modifiers'] += '\n{}{}'.format('\t' * 2, fmt_modifier(vt, mt, val))
        
        # Is this the default law in this group? Build string:
        default_law = vt.default_foc_law if focus else vt.default_ob_law
        default = (default_law == law)
        st['default'] = ''
        if default:
          st['default'] = tabs('''
    default = yes''')

        # Should we be muslims or not for this law? Build string (potential):
        st['muslim_rule'] = ''
        if vt.name == 'iqta':
          st['muslim_rule'] = tabs('''
      owner = { religion_group = muslim }''')
        elif vt.name == 'feudal':
          st['muslim_rule'] = tabs('''
      NOT = { owner = { religion_group = muslim } }''')

        # Build tribal requirements string (potential):
        st['tribal_rule'] = ''
        if vt.name == 'tribal':
          st['tribal_rule'] = tabs('''
      OR = {
        owner = { is_tribal = no }
        has_law = tribal_organization_3
        has_law = tribal_organization_4
      }''')

        # Build special law strings:
        st['has_law_group'] = ''
        for i in range(N_LAWS):
          st['has_law_group'] += '\n{}has_law = {}'.format('\t' * 6, fmt_law_name(vt, i, focus))
        
        st['revoke_law_group'] = ''
        for i in range(N_LAWS):
          st['revoke_law_group'] += '\n{}revoke_law = {}'.format('\t' * 4, fmt_law_name(vt, i, focus))

        if next_law_name and prev_law_name:
          st['slider_rule'] = tabs('''
        OR = {{
          has_law = {}
          has_law = {}
        }}''').format(prev_law_name, next_law_name)
        else:
          st['slider_rule'] = tabs('''
        has_law = {}''').format(prev_law_name if prev_law_name else next_law_name)

        # Build ai_will_do strings:
        ai_will_do = 0 if focus and not default else 1
        st['ai_factor'] = str(ai_will_do)
        st['need_vassal_modifier'] = ''
        st['default_first_modifier'] = ''
        st['greed_modifier'] = ''
        st['rare_reduction_modifier'] = ''

        if ai_will_do:
          st['ai_factor'] += '\n'
          st['need_vassal_modifier'] = tabs('''
      modifier = {{ # Must actually have at least one {} vassal
        factor = 0
        NOT = {{ any_vassal = {{ {} = yes }} }}
      }}''').format(vt.gov_type.capitalize(), vt.gov_trigger)
        # All Obligations modifiers from here:
          if not focus:
            # If for some reason no laws in this group are passed, the AI should
            # first pass whatever law is the default:
            if not default:
              st['default_first_modifier'] = tabs('''
      modifier = {{ # Only pass the default law if none of the {} Obligations laws are passed
        factor = 0
        NOR = {{{}
        }}
      }}''').format(vt.name.capitalize(), dedent(st['has_law_group']))
            # Soft accounting for charitable vs. greedy traits (using ai_greed
            # would be better, but I need an idea of the distribution for that):
            if law <= default_law and next_law_name:
              st['greed_modifier'] = tabs('''
      modifier = {{
        factor = 0.25
        owner = {{ trait = greedy }}
        has_law = {0}
      }}
      modifier = {{
        factor = 4
        owner = {{ trait = charitable }}
        has_law = {0}
      }}''').format(next_law_name)
            elif law > default_law and prev_law_name:
              st['greed_modifier'] = tabs('''
      modifier = {{
        factor = 2
        owner = {{ trait = greedy }}
        has_law = {0}
      }}
      modifier = {{
        factor = 0.5
        owner = {{ trait = charitable }}
        has_law = {0}
      }}''').format(prev_law_name)
            # It's generally a good idea for the AI to try to keep Obligations
            # high, so this is a built-in reminder:
            if next_law_name:
              st['rare_reduction_modifier'] = tabs('''
      modifier = {{ # Slow down AI reduction of {} Obligations
        factor = {}
        has_law = {}
      }}''').format(vt.name.capitalize(), '{:.2f}'.format(0.05 * law + 0.1), next_law_name)

        if at_start:
          at_start = False
        else:
          print(file=f)

        print(tabs('''\
  {law} = {{
    group = {group}{default}

    potential = {{
      OR = {{
        higher_tier_than = BARON
        owner = {{ is_patrician = yes }}
      }}{muslim_rule}{tribal_rule}
    }}
    allow = {{
      trigger_if = {{
        limit = {{ temporary = yes }}
        temporary = no
      }}
      trigger_if = {{
        limit = {{
          OR = {{{has_law_group}
          }}
        }}{slider_rule}
      }}
    }}
    effect = {{
      hidden_effect = {{{revoke_law_group}
      }}
    }}
    ai_will_do = {{
      factor = {ai_factor}{need_vassal_modifier}{default_first_modifier}{greed_modifier}{rare_reduction_modifier}
    }}
    {law_modifiers}
  }}''').format(**st), file=f)
  print('}', file=f)


def indent(text):
  return text.replace('\n', '\n\t')


def dedent(text):
  return text.replace('\n\t', '\n')


def tabs(text):
  return text.replace(' ' * 2, '\t')


def fmt_law_group(vtype, focus):
  return '{}_{}'.format(vtype.name, 'slider' if focus else 'obligations')


def fmt_law_name(vtype, index, focus):
  return '{}_{}'.format(fmt_law_group(vtype, focus), index)


def fmt_modifier(vtype, name, value):
  if name != 'opinion':
    return '{}_vassal_{} = {:0.4f}'.format(vtype.base_type, name, value)
  else:
    return '{} = {}'.format(vtype.opinion_type, value)


########################################################################################################################


if __name__ == '__main__':
  sys.exit(main())
