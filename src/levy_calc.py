#!/usr/bin/python3

from argparse import ArgumentParser
import matplotlib.pyplot as plt

################################################################################

minLevyRaiseOpinion = -75
maxLevyRaiseOpinion = 75

def maxlevy_opinion_scale(o):
  if o < minLevyRaiseOpinion:
    return 0.0
  if o > maxLevyRaiseOpinion:
    return 1.0
  return o / 151 + 0.5 # certainly could be more general... (adjust if scale changes)

def decay_min_levy(i):
  if i < 10: return 0
  return -0.5 * ((i-10) / 100)

def decay_max_levy(i):
  if i < 20: return 0
  return -0.25 * ((i-20) / 100)

# Base values
minLBase = 0
maxLBase = 0.6

# DynLevy modifiers
minLDynLevy = -0.3
maxLDynLevy = -0.5

# Arbitrary modifiers
minLGeneric = 0
maxLGeneric = 0

# Focus law modifiers
minLFocus = 0.05 # Due to default law for feudal vassals
maxLFocus = 0.1 # Due to default law for feudal vassals

# Imperial Decay (integer percentage)
decay = 0

maxLObLaws    = [0.000, 0.075, 0.150, 0.225, 0.300]
minLObLaws    = [0.000, 0.050, 0.100, 0.150, 0.200]
minLCALaws    = [0.000, 0.050, 0.100, 0.200, 0.350]
minLAdminLaws = [0.000, 0.100, 0.150]

################################################################################

ap = ArgumentParser(description="Test out min_levy/max_levy interaction (calibration).")
# ap.add_argument('-b', '--batch', action='store_true',
#           help='Do not run in interactive mode; instead, spit out a bunch of charts.')
ap.add_argument('-o', '--ob-law', default=0,
          help='Obligations law tier in [0,4] [default: %(default)s]')
ap.add_argument('-c', '--ca-law', default=0,
          help='Crown Authority law tier in [0,4] [default: %(default)s]')
ap.add_argument('-a', '--admin-law', default=0,
          help='Administration law tier (Early = 0, Late = 1, Imperial = 2) [default: %(default)s]')
ap.add_argument('-d', '--decay', default=decay,
          help='Imperial Decay percentage (integer) [default: %(default)s]')
ap.add_argument('--dynlevy-min-levy', default=minLDynLevy,
          help='DynLevy malus to min. levy [default: %(default)s]')
ap.add_argument('--dynlevy-max-levy', default=maxLDynLevy,
          help='DynLevy malus to max. levy [default: %(default)s]')
ap.add_argument('--no-dynlevy', action='store_true',
          help='Exclude DynLevy malus to both min. and max. levies')
ap.add_argument('--min-levy-offset', default=minLGeneric,
          help='Arbitrary offset to min. levy [default: %(default)s]')
ap.add_argument('--max-levy-offset', default=maxLGeneric,
          help='Arbitrary offset to max. levy [default: %(default)s]')
ap.add_argument('--base-min-levy', default=minLBase,
          help='Arbitrary offset to min. levy [default: %(default)s]')
ap.add_argument('--base-max-levy', default=maxLBase,
          help='Arbitrary offset to max. levy [default: %(default)s]')
ap.add_argument('--focus-min-levy', default=minLFocus,
          help='Focus law modifier to min. levy [default: %(default)s]')
ap.add_argument('--focus-max-levy', default=maxLFocus,
          help='Focus law modifier to max. levy [default: %(default)s]')

################################################################################

args = ap.parse_args()

decay = int(args.decay)
assert decay >= 0 and decay <= 100
assert int(args.ob_law) in range(5)
assert int(args.ca_law) in range(5)
assert int(args.admin_law) in range(3)

minLOb = minLObLaws[int(args.ob_law)]
maxLOb = maxLObLaws[int(args.ob_law)]
minLCA = minLCALaws[int(args.ca_law)]
minLAdmin = minLAdminLaws[int(args.admin_law)]

minLDecay = decay_min_levy(decay)
maxLDecay = decay_max_levy(decay)

if args.no_dynlevy:
  minLDynLevy = 0
  maxLDynLevy = 0
else:
  minLDynLevy = float(args.dynlevy_min_levy)
  maxLDynLevy = float(args.dynlevy_max_levy)

minLGeneric = float(args.min_levy_offset)
maxLGeneric = float(args.max_levy_offset)
minLBase = float(args.base_min_levy)
maxLBase = float(args.base_max_levy)
minLFocus = float(args.focus_min_levy)
maxLFocus = float(args.focus_max_levy)

def clamp(val):
  return min(1, max(0, val))

minL = clamp(minLBase + minLDynLevy + minLFocus + minLDecay + minLGeneric + minLOb + minLCA + minLAdmin)
maxL = clamp(maxLBase + maxLDynLevy + maxLFocus + maxLDecay + maxLGeneric + maxLOb)

xVals = range(-100,101)
yVals = []
minLevyBelowOpinion = None

for o in xVals:
  if o < minLevyRaiseOpinion:
    yVals.append(0)
  else:
    maxLScaled = maxL * maxlevy_opinion_scale(o)
    if minL >= maxLScaled:
      minLevyBelowOpinion = o
      yVals.append(minL * 100.0)
    else:
      yVals.append(maxLScaled * 100.0)

print('Min. Levy: {:.2f}%'.format(minL * 100.0))
print('Max. Levy: {:.2f}%'.format(maxL * 100.0))

if minLevyBelowOpinion:
  print('Min. Levy Opinion Threshold: {}'.format(minLevyBelowOpinion))

plt.plot(xVals, yVals)
plt.xlabel('Vassal Opinion')
plt.ylabel('Liege Levy (%)')
plt.show()
