#!/usr/bin/env python3

import collections
import pathlib
import pprint
import re
import shutil
import tempfile
import ck2parser
import print_time

JUST_PRINT_STATS = False

def process_province_history(parser):
    title_id = {}
    for number, title, tree in ck2parser.get_provinces(parser):
        title_id[title] = number
    return title_id

def build_trigger(parser, counties_by_barony_count, title_id):
    trigger_outer = ck2parser.Pair('emf_can_add_holding_slot_trigger')
    trigger = ck2parser.Pair('NOR')
    trigger.value.contents.append(ck2parser.Pair('num_of_max_settlements',
                                                 ck2parser.Number(7)))
    for i in range(1, 7):
        block = ck2parser.Pair('AND')
        block.value.contents.append(ck2parser.Pair('num_of_max_settlements',
                                                   ck2parser.Number(i)))
        if i < 6:
            not_line = ck2parser.Pair('NOT')
            not_line.value.contents.append(
                ck2parser.Pair('num_of_max_settlements',
                               ck2parser.Number(i + 1)))
            block.value.contents.append(not_line)
        or_block = ck2parser.Pair('OR')
        provs = sorted(title_id[t] for t in counties_by_barony_count[i])
        prov_pairs = [ck2parser.Pair('province_id', ck2parser.Number(j))
                      for j in provs]
        or_block.value.contents.extend(prov_pairs)
        block.value.contents.append(or_block)
        trigger.value.contents.append(block)
    trigger_outer.value.contents.append(trigger)
    return trigger_outer

@print_time.print_time
def main():
    parser = ck2parser.FullParser(ck2parser.rootpath / 'SWMH-BETA/SWMH')
    outpath = ck2parser.rootpath / 'EMF/EMF+SWMH/common/scripted_triggers/emf_can_add_holding_slot_trigger.txt'
    simple_parser = ck2parser.SimpleParser(*parser.moddirs)

    title_id = process_province_history(simple_parser)
    cultures = ck2parser.get_cultures(simple_parser, groups=False)
    parser.fq_keys = cultures

    def scan_for_baronies(tree):
        for n, v in tree:
            if ck2parser.is_codename(n.val):
                if n.val.startswith('c_'):
                    baronies = sum(1 for n2, _ in v if n2.val.startswith('b_'))
                    yield n.val, baronies
                else:
                    yield from scan_for_baronies(v)

    counties_by_barony_count = collections.defaultdict(list)
    for _, tree in parser.parse_files('common/landed_titles/*'):
        for title, baronies in scan_for_baronies(tree):
            counties_by_barony_count[baronies].append(title)
    trigger = build_trigger(parser, counties_by_barony_count, title_id)
    with outpath.open('w', encoding='cp1252', newline='\r\n') as f:
        f.write(trigger.str(parser))

if __name__ == '__main__':
    main()
