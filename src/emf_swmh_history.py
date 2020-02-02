#!/usr/bin/env python3

import shutil
import sys
from ck2parser import rootpath, Comment, FullParser
from print_time import print_time
from collections import OrderedDict

changeset = {
    'd_sunni': [
        ((775, 1, 1), 0, '''
            effect = { set_title_flag = al_Mahdi }
            '''),
        ((785, 1, 1), 0, '''
            effect = { set_title_flag = al_Hadi }
            '''),
        ((861, 12, 1), 1, '''
            effect = { set_title_flag = anarchy_at_samarra_happened }
            set_global_flag = anarchy_at_samarra
            '''),
        ((869, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muhtadi
                set_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((870, 6, 1), 0, '''
            effect = {
                set_title_flag = al_Mutamid
                set_variable = { which = "caliphnumber" value = 2 }
            }
            clr_global_flag = anarchy_at_samarra
            '''),
        ((892, 10, 1), 0, '''
            effect = {
                set_title_flag = al_Mutadid
                set_variable = { which = "caliphnumber" value = 3 }
            }
            '''),
        ((902, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muktafi
                set_variable = { which = "caliphnumber" value = 4 }
            }
            '''),
        ((908, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muqtadir
                set_variable = { which = "caliphnumber" value = 5 }
            }
            '''),
        ((932, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Qahir
                set_variable = { which = "caliphnumber" value = 6 }
            }
            '''),
        ((934, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Radi
                set_variable = { which = "caliphnumber" value = 7 }
            }
            '''),
        ((940, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muttaqi
                set_variable = { which = "caliphnumber" value = 8 }
            }
            '''),
        ((944, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustakfi
                set_variable = { which = "caliphnumber" value = 9 }
            }
            '''),
        ((946, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muti
                set_variable = { which = "caliphnumber" value = 10 }
            }
            '''),
        ((974, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Tai
                set_variable = { which = "caliphnumber" value = 11 }
            }
            '''),
        ((991, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Qadir
                set_variable = { which = "caliphnumber" value = 12 }
            }
            '''),
        ((1031, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Qaim
                set_variable = { which = "caliphnumber" value = 13 }
            }
            '''),
        ((1075, 1, 1), 0, '''
            effect = {
                set_title_flag = al-Muqtadi
                set_variable = { which = "caliphnumber" value = 14 }
            }
            '''),
        ((1094, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustazhir
                set_variable = { which = "caliphnumber" value = 15 }
            }
            '''),
        ((1118, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustarshid
                set_variable = { which = "caliphnumber" value = 16 }
            }
            '''),
        ((1135, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Rashid
                set_variable = { which = "caliphnumber" value = 17 }
            }
            '''),
        ((1136, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muqtafi
                set_variable = { which = "caliphnumber" value = 18 }
            }
            '''),
        ((1160, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustanjid
                set_variable = { which = "caliphnumber" value = 19 }
            }
            '''),
        ((1170, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustadi
                set_variable = { which = "caliphnumber" value = 20 }
            }
            '''),
        ((1180, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Nasir
                set_variable = { which = "caliphnumber" value = 21 }
            }
            '''),
        ((1225, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Zahir
                set_variable = { which = "caliphnumber" value = 22 }
            }
            '''),
        ((1226, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustansir
                set_variable = { which = "caliphnumber" value = 23 }
            }
            '''),
        ((1242, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustasim
                set_variable = { which = "caliphnumber" value = 24 }
            }
            ''')
    ],
    'e_arabia': [
        ((754, 1, 1), 1, '''
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 1 }
                set_variable = { which = "imperial_decay" value = 25 }
            }
            '''),
        ((775, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 2 } }
            '''),
        ((785, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 3 } }
            '''),
        ((786, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 4 } }
            '''),
        ((809, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 5 } }
            '''),
        ((813, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 6 } }
            '''),
        ((833, 8, 9), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 7 } }
            '''),
        ((842, 1, 5), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 8 } }
            '''),
        ((847, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 9 } }
            '''),
        ((861, 12, 1), 1, '''
            law = infighting_0
            effect = { set_variable = { which = "imperial_dynasty_count" value = 10 } }
            '''),
        ((862, 6, 7), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 11 } }
            '''),
        ((866, 1, 1), 1, '''
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 12 }
                set_variable = { which = "imperial_decay" value = 50 }
            }
            '''),
        ((869, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 13 } }
            '''),
        ((870, 6, 1), 1, '''
            effect = {
                revoke_law = infighting_0
                set_variable = { which = "imperial_dynasty_count" value = 14 }
            }
            '''),
        ((892, 10, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 15 } }
            '''),
        ((902, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 16 } }
            '''),
        ((908, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 17 } }
            '''),
        ((932, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 18 } }
            '''),
        ((934, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 19 } }
            '''),
        ((940, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 20 } }
            '''),
        ((944, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 21 } }
            '''),
        ((945, 1, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            ''')
    ],
    'e_byzantium': [
        ((743, 11, 2), 1, '''
            set_global_flag = byz_empire_flourishes
            effect = {
                set_variable = { which = "imperial_decay" value = 10 }
            }
            '''),
        ((1055, 1, 11), 1, '''
            clr_global_flag = byz_empire_flourishes
            set_global_flag = byz_empire_cracking
            effect = {
                set_variable = { which = "imperial_decay" value = 30 }
            }
            '''),
        ((1071, 8, 26), 1, '''
            clr_global_flag = byz_empire_cracking
            set_global_flag = byz_empire_falling
            effect = {
                set_variable = { which = "imperial_decay" value = 50 }
            }
            '''),
        ((1081, 4, 1), 1, '''
            clr_global_flag = byz_empire_falling
            set_global_flag = byz_empire_cracking
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 0 }
                set_variable = { which = "imperial_decay" value = 30 }
            }
            '''),
        ((1118, 8, 15), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1143, 4, 8), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 2 } }
            '''),
        ((1180, 9, 24), 1, '''
            clr_global_flag = byz_empire_cracking
            set_global_flag = byz_empire_falling
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 3 }
                set_variable = { which = "imperial_decay" value = 50 }
            }
            '''),
        ((1183, 9, 24), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 4 } }
            '''),
        ((1185, 9, 12), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1195, 6, 1), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1203, 7, 18), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 2 } }
            '''),
        ((1204, 1, 28), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1282, 12, 11), 1, '''
            clr_global_flag = byz_empire_falling
            set_global_flag = byz_empire_shattered
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 1 }
                set_variable = { which = "imperial_decay" value = 70 }
            }
            '''),
        ((1328, 5, 24), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 2 } }
            ''')
    ],
    'e_hre': [
        ((962, 2, 2), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((973, 5, 7), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((983, 12, 7), 1, '''
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 2 }
                set_variable = { which = "imperial_decay" value = 5 }
            }
            '''),
        ((1002, 1, 24), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 3 } }
            '''),
        ((1024, 7, 3), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1039, 6, 4), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1056, 10, 5), 1, '''
            effect = {
                set_variable = { which = "imperial_decay" value = 10 }
                set_variable = { which = "imperial_dynasty_count" value = 2 }
            }
            '''),
        ((1106, 8, 7), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 3 } }
            '''),
        ((1125, 5, 23), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1152, 2, 15), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1190, 6, 10), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 2 } }
            '''),
        ((1197, 9, 28), 1, '''
            effect = {
                set_variable = { which = "imperial_dynasty_count" value = 3 }
                set_variable = { which = "imperial_decay" value = 20 }
            }
            '''),
        ((1208, 6, 21), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1250, 12, 13), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1254, 5, 21), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1272, 4, 2), 1, '''
            effect = {
                set_variable = { which = "imperial_decay" value = 30 }
            }
            ''')
    ],
    'd_hashshashin': [
        ((20, 1, 1), 1, '''
            law = crown_authority_2
            law = revokation_2
            law = ze_revokation_2
            law = administration_1
            law = law_voting_power_0
            law = war_voting_power_0
            law = titles_voting_power_0
            law = justice_voting_power_0
            law = centralization_3
            ''')
    ],
    'k_magyar': [
        ((769, 1, 1), 0, '''
            law = succ_gavelkind
            ''')
    ]
}

# Dictionary of non-EMF laws, each paired with the EMF law with which it should be replaced
# If a single law is to be replaced with multiple laws, use a tuple containing the laws as the value
replace_law_dict = {
    "feudal_administration": "administration_0",
    "imperial_administration": "administration_2",
    "revoke_title_voting_power_0": "titles_voting_power_0",
    "revoke_title_voting_power_1": "titles_voting_power_1",
    "imprison_voting_power_0": "justice_voting_power_0",
    "imprison_voting_power_1": "justice_voting_power_1",
    "grant_title_voting_power_0": "titles_voting_power_0",
    "grant_title_voting_power_1": "titles_voting_power_1",
    "banish_voting_power_0": "justice_voting_power_0",
    "banish_voting_power_1": "justice_voting_power_1",
    "execution_voting_power_0": "justice_voting_power_0",
    "execution_voting_power_1": "justice_voting_power_1",
    "vassal_wars_law_0": "king_peace_0",
    "vassal_wars_law_1": "king_peace_1",
    "vassal_wars_law_2": "king_peace_2",
    "out_of_realm_inheritance_law_0": "inheritance_0",
    "out_of_realm_inheritance_law_1": "inheritance_1",
    "revoke_title_law_0": "ze_revokation_0",
    "revoke_title_law_1": "ze_revokation_1",
    "revoke_title_law_2": "ze_revokation_2",
    "ze_administration_laws_0": "administration_0",
    "ze_administration_laws_1": "administration_1",
    "ze_administration_laws_2": "administration_2"
}

@print_time
def main():
    swmhpath = rootpath / 'SWMH-BETA/SWMH'
    emfpath = rootpath / 'EMF/EMF'
    emfswmhpath = rootpath / 'EMF/EMF+SWMH'
    swmhhistory = swmhpath / 'history'
    emfswmhhistory = emfswmhpath / 'history'
    parser = FullParser()
    parser.fq_keys = ['name']
    parser.crlf = False
    parser.tab_indents = True
    parser.indent_width = 8
    # parser.no_fold_keys.extend(['factor', 'value'])

    # shutil.rmtree(str(emfswmhhistory), ignore_errors=True)
    # emfswmhhistory.mkdir(parents=True)

    valid_laws = set()
    for path, tree in parser.parse_files('common/laws/*.txt',
                                         basedir=emfpath):
        for n, v in tree:
            if n.val != 'laws_groups':
                valid_laws.update(n2.val for n2, v2 in v)

    assert valid_laws.isdisjoint(replace_law_dict), "A valid law is also in the list of laws that are to be replaced!"

    shutil.rmtree(str(emfswmhhistory / 'characters'), ignore_errors=True)

    parser.newlines_to_depth = 0
    parser.no_fold_to_depth = 1
    (emfswmhhistory / 'characters').mkdir()
    path = swmhhistory / 'characters/hungarian.txt'
    tree = parser.parse_file(path)
    effect = tree[159137][867, 1, 1]['effect']
    effect.contents = [p for p in effect.contents
                       if p.key.val == 'create_character']
    effect.contents[:0] = parser.parse('''
        # Truce with Bulgaria until 887
        random_independent_ruler = {
            limit = { has_landed_title = k_bulgaria }
            opinion = { who = ROOT modifier = in_non_aggression_pact years = 20 }
        }
        if = {
            limit = { is_nomadic = yes }
            spawn_unit = {
                province = 1147 # Bacau
                owner = ROOT
                troops = {
                    light_cavalry = { 465 465 }
                    horse_archers = { 235 235 }
                }
                attrition = 0.25
                reinforces = yes
                earmark = start_troops
            }
            spawn_unit = {
                province = 1147 # Bacau
                owner = ROOT
                troops = {
                    light_cavalry = { 465 465 }
                    horse_archers = { 235 235 }
                }
                attrition = 0.25
                reinforces = yes
                earmark = start_troops
            }
        }
        ''').contents
    targetpath = emfswmhhistory / path.relative_to(swmhhistory)
    parser.write(tree, targetpath)

    shutil.rmtree(str(emfswmhhistory / 'titles'), ignore_errors=True)

    parser.newlines_to_depth = -1
    parser.no_fold_to_depth = 0
    parser.fq_keys = ['which']
    (emfswmhhistory / 'titles').mkdir()
    for path, tree in parser.parse_files('history/titles/*.txt',
                                         basedir=swmhpath):
        changed = False
        if path.stem in changeset:
            changed = True
            for date, where, text in changeset[path.stem]:
                try:
                    tree[date].contents[where:where] = parser.parse(text).contents
                except:
                    print(path)
                    raise
        elif path.stem == 'd_apostolic':
            for p in reversed(tree):
                for p2 in reversed(p.value):
                    if p2.key.val != 'holder':
                        p.value.contents.remove(p2)
                if len(p.value.contents) == 0:
                    tree.contents.remove(p)
            later_history = []
            for p in reversed(tree):
                if p.key.val >= (1058, 1, 1):
                    tree.contents.remove(p)
                    later_history.insert(0, p)
            tree.contents.extend(parser.parse('''
                1058.1.1 = {
                    holder = 0
                }
                ''').contents)
            parser.write(tree, emfswmhhistory / 'titles/b_etchmiadzin.txt')
            tree.contents = later_history
            parser.write(tree, emfswmhhistory / 'titles/b_trazak.txt')
        elif path.stem == 'k_hungary':
            changed = True
            assert len(tree.contents) == 57
            # comment out the last (and only) item in the 580 block (set_coa)
            assert len(tree[580, 1, 1].contents) == 1
            item = tree[580, 1, 1].contents.pop()
            comments = item.pre_comments
            item.pre_comments = []
            comments.extend(
                [Comment(x) for x in item.inline_str(parser)[0].splitlines()])
            tree[580, 1, 1].ker.pre_comments[:0] = comments
            # comment out the last pair in the 797 obj (reset_coa)
            assert len(tree[797, 1, 1].contents) == 2
            item = tree[797, 1, 1].contents.pop()
            comments = item.pre_comments
            item.pre_comments = []
            comments.extend(
                [Comment(x) for x in item.inline_str(parser)[0].splitlines()])
            tree[797, 1, 1].ker.pre_comments[:0] = comments
            # insert two pairs between the 22nd (835) and the 23rd (907)...
            tree.contents[22:22] = parser.parse('''
                895.1.1 = {
                    effect = { set_title_flag = hungary_name_change }
                    set_global_flag = emf_magyar_migration_started
                }
                902.1.1 = {
                    set_global_flag = emf_magyar_migration_completed
                }
                ''').contents
            # ...and move the commented-out 895 to a reasonable place
            tree.contents[22].pre_comments = tree.contents[24].pre_comments
            tree.contents[24].pre_comments = []
            # prepend a pair to the 907 obj
            tree[907, 7, 4].contents[:0] = parser.parse('''
                set_global_flag = emf_conquest_hungary_completed
                ''').contents
            # prepend a pair to the 1000 obj
            tree[1000, 12, 25].contents[:0] = parser.parse('''
                effect = { set_title_flag = ai_converted_catholic }
                ''').contents
        elif path.stem == 'e_china_west_governor':
            changed = True
            assert len(tree.contents) == 43
            tree[1264, 8, 21].contents.extend(parser.parse('''
                effect = { set_coa = e_china_yuan }
                ''').contents)
            tree[1234, 2, 10].contents.extend(parser.parse('''
                effect = { set_coa = e_mongol_empire }
                ''').contents)
            tree[1125, 3, 26].contents.extend(parser.parse('''
                effect = { set_coa = e_china_jin }
                ''').contents)
            tree[1005, 1, 1].contents.extend(parser.parse('''
                effect = { set_coa = e_china_liao }
                ''').contents)
            tree.contents[11:11] = parser.parse('''
                960.2.1 = {
                    effect = { set_coa = e_china_song }
                }
                ''').contents
            tree.contents[6:6] = parser.parse('''
                907.5.12 = {
                    effect = { reset_coa = THIS }
                }
                ''').contents
            tree.contents[:0] = parser.parse('''
                618.6.18 = {
                    effect = { set_coa = e_china_tang }
                }
                690.10.16 = {
                    effect = { set_coa = e_china_zhou }
                }
                705.12.16 = {
                    effect = { set_coa = e_china_tang }
                }
                ''').contents
            tree.contents[0].pre_comments = tree.contents[3].pre_comments
            tree.contents[3].pre_comments = []
        for n, v in tree:
            # removes attached comments, eh, whatever
            bad = {p2 for p2 in v.contents
                if p2.key.val == 'vice_royalty' or
                    p2.key.val == 'law' and p2.value.val not in valid_laws}
            # working this way (create set + insert set) avoids duplicate law entries
            # (compared to just replacing values in v.contents)
            replaced_law_entries = OrderedDict() # OrderedDict with bogus values as a hacky ordered set (makes sure new laws are inserted in a deterministic order)
            for p2 in v.contents:
                if p2.key.val == 'law' and p2.value.val in replace_law_dict:
                    if isinstance(replace_law_dict[p2.value.val], tuple):
                        for new_law in replace_law_dict[p2.value.val]:
                            replaced_law_entries[new_law] = None
                    else:
                        replaced_law_entries[replace_law_dict[p2.value.val]] = None
            if len(bad) > 0:
                changed = True
                v.contents = [p2 for p2 in v.contents if p2 not in bad]
            if len(replaced_law_entries) > 0:
                changed = True
                v.contents += parser.parse(
                    '\n'.join('law = ' + new_law for new_law in replaced_law_entries.keys())
                    ).contents
        if changed:
            tree.contents = [p for p in tree.contents
                             if p.value.contents or p.has_comments]
            targetpath = emfswmhhistory / path.relative_to(swmhhistory)
            parser.write(tree, targetpath)

if __name__ == '__main__':
    main()
