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
from pathlib import Path
from tabulate import tabulate # `pip3 install tabulate`


########################################################################################################################


DEF_MOD_PATH = Path('../EMF')  # If you were in the /EMF/src folder, this would be base EMF...

# Maximum possible range of combined max_levy modifiers for any given vassal type
DEF_MIN_TOTAL_MAX_LEVY = -0.2
DEF_MAX_TOTAL_MAX_LEVY = 0.3

# Mapping of vassal types to default vassal_max_levy modifier to vassal_tax_modifier conversion ratio
DEF_TAX_PER_LEVY = {
  'feudal': 1.0,
  'iqta':   1.2,
  'temple': 1.6,
  'city':   2.0,
  'tribal': 0.8,
}

# Mapping of vassal types to default laws (zero-indexed) for Obligations and Focus, respectively
DEF_LAWS = {
  'feudal': (0,0),
  'iqta':   (1,2),
  'temple': (0,2),
  'city':   (0,3),
  'tribal': (0,0),
}

# Mapping of vassal types to vassal opinion linear modifier function of law tier in tuple form of (slope, y-intercept)
# or (m, b), for y = mx + b (y is opinion & x is zero-indexed law tier)
DEF_OPINION = {
  'feudal': (-5,0),
  'iqta':   (-5,0),
  'temple': (-5,0),
  'city':   (-5,0),
  'tribal': (-6,0),
}

N_LAWS = 5


########################################################################################################################


class VassalType:
  def __init__(self, name, tax_per_levy=None, obligation_law=None, focus_law=None, opinion_slope=None, opinion_base=None, law_function=None):
    self.name = name
    self.tax_per_levy = tax_per_levy if tax_per_levy is not None else DEF_TAX_PER_LEVY[name]
    self.obligation_law = obligation_law if obligation_law is not None else DEF_LAWS[name][0]
    self.focus_law = focus_law if focus_law is not None else DEF_LAWS[name][1]
    self.opinion_slope = opinion_slope if opinion_slope is not None else DEF_OPINION[name][0]
    self.opinion_base = opinion_base if opinion_base is not None else DEF_OPINION[name][1]
    self.law_function = law_function
    self.base_type = 'castle' if name == 'feudal' or name == 'iqta' else name
    self.gov_group = name
    if name == 'iqta':
      self.gov_group = 'feudal'
    elif name == 'temple':
      self.gov_group = 'theocracy'
    elif name == 'city':
      self.gov_group = 'republic'


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
      'tax_modifier': max_levy_delta * self.vtype.tax_per_levy,
    }

  def obligations(self, law):
    max_levy_per_law = (self.max_levy_range - 2 * self.max_levy_tradeoff) / (N_LAWS - 1)
    max_levy = self.min_max_levy + self.max_levy_tradeoff + max_levy_per_law * law
    return {
      'max_levy': max_levy,
      'tax_modifier': max_levy * self.vtype.tax_per_levy,
      'opinion': self.vtype.opinion_base + self.vtype.opinion_slope * law,
    }


########################################################################################################################


def get_args():
  parser = argparse.ArgumentParser(description="Generate EMF vassal contract (Obligations & Focus) demesne laws.")
  parser.add_argument('-n', '--dry-run', action='store_true',
                      help='print a summary of the calculated law modifiers, but don\'t modify any files')
  parser.add_argument('-m', '--mod-path', default=DEF_MOD_PATH,
                      help='path to root folder of mod, under which files will be generated [default: %(default)s]')
  parser.add_argument('--min-max-levy', default=DEF_MIN_TOTAL_MAX_LEVY,
                      help='minimum possible net max_levy modifier from these laws [default: %(default)s]')
  parser.add_argument('--max-max-levy', default=DEF_MAX_TOTAL_MAX_LEVY,
                      help='maximum possible net max_levy modifier from these laws [default: %(default)s]')
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


def main():
  args = get_args()

  if not args.dry_run:
    print("Fatal: Must use this program with the -n, --dry-run option, for now", file=sys.stderr)
    return 1

  vassal_types = [
    VassalType('feudal', tax_per_levy=float(args.feudal_tax_per_levy)),
    VassalType('iqta',   tax_per_levy=float(args.iqta_tax_per_levy)),
    VassalType('temple', tax_per_levy=float(args.temple_tax_per_levy)),
    VassalType('city',   tax_per_levy=float(args.city_tax_per_levy)),
    VassalType('tribal', tax_per_levy=float(args.tribal_tax_per_levy)),
  ]

  for vt in vassal_types:
    vt.law_function = LawFunction(vt, float(args.min_max_levy), float(args.max_max_levy))

  # Always print a law summary to stdout (if not a dry run, also print it to the actual laws file)
  print_summary(vassal_types, args, sys.stdout)

  if args.dry_run:
    return 0

  return 0


def print_summary(vassal_types, args, file):
  cmt = '# ' if file != sys.stdout and file != sys.stderr else ''
  print(cmt + 'PARAMETER SUMMARY:', file=file)
  print(cmt, file=file)
  print(cmt + 'Smallest possible max_levy modifier: {}'.format(args.min_max_levy), file=file)
  print(cmt + 'Greatest possible max_levy modifier: {}'.format(args.max_max_levy), file=file)
  print(cmt + 'Levy to tax conversion efficiency per vassal class:', file=file)
  for vt in vassal_types:
    print(cmt + '  {:8s} {}'.format(vt.name.capitalize() + ':', vt.tax_per_levy), file=file)

  tbl_hdr = ["Modifier", "Law I", "Law II", "Law III", "Law IV", "Law V"]

  for vt in vassal_types:
    for is_focus in (True, False):
      modifier_types = ['max_levy', 'tax_modifier']
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
          row.append(val)
        rows.append(row)

      print('''
{}+------------------------>
{}| {} {}'''.format(cmt, cmt, vt.name.upper(), ('focus' if is_focus else 'obligations').upper()), file=file)
      print(cmt + tabulate(rows, tbl_hdr, tablefmt="psql").replace('\n', '\n' + cmt).rstrip('# '), file=file)


########################################################################################################################


if __name__ == '__main__':
  sys.exit(main())
