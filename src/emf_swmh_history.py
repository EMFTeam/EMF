#!/usr/bin/env python3

import shutil
import sys
from ck2parser import rootpath, Comment, FullParser
from print_time import print_time

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
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((870, 6, 1), 0, '''
            effect = {
                set_title_flag = al_Mutamid
                change_variable = { which = "caliphnumber" value = 1 }
            }
            clr_global_flag = anarchy_at_samarra
            '''),
        ((892, 10, 1), 0, '''
            effect = {
                set_title_flag = al_Mutadid
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((902, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muktafi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((908, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muqtadir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((932, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Qahir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((934, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Radi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((940, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muttaqi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((944, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustakfi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((946, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muti
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((974, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Tai
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((991, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Qadir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1031, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Qaim
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1075, 1, 1), 0, '''
            effect = {
                set_title_flag = al-Muqtadi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1094, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustazhir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1118, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustarshid
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1135, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Rashid
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1136, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Muqtafi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1160, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustanjid
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1170, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustadi
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1180, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Nasir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1225, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Zahir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1226, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustansir
                change_variable = { which = "caliphnumber" value = 1 }
            }
            '''),
        ((1242, 1, 1), 0, '''
            effect = {
                set_title_flag = al_Mustasim
                change_variable = { which = "caliphnumber" value = 1 }
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
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((785, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((786, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((809, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((813, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((833, 8, 9), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((842, 1, 5), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((847, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((861, 12, 1), 1, '''
            law = infighting_0
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((862, 6, 7), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((866, 1, 1), 1, '''
            effect = {
                change_variable = { which = "imperial_dynasty_count" value = 1 }
                set_variable = { which = "imperial_decay" value = 50 }
            }
            law = law_voting_power_1
            law = war_voting_power_1
            law = titles_voting_power_1
            '''),
        ((869, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((870, 6, 1), 1, '''
            effect = {
                revoke_law = infighting_0
                change_variable = { which = "imperial_dynasty_count" value = 1 }
            }
            '''),
        ((892, 10, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((902, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((908, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((932, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((934, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((940, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((944, 1, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
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
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1143, 4, 8), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1180, 9, 24), 1, '''
            clr_global_flag = byz_empire_cracking
            set_global_flag = byz_empire_falling
            effect = {
                change_variable = { which = "imperial_dynasty_count" value = 1 }
                set_variable = { which = "imperial_decay" value = 50 }
            }
            '''),
        ((1183, 9, 24), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1185, 9, 12), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1195, 6, 1), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1203, 7, 18), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1204, 1, 28), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1282, 12, 11), 1, '''
            clr_global_flag = byz_empire_falling
            set_global_flag = byz_empire_shattered
            effect = {
                change_variable = { which = "imperial_dynasty_count" value = 1 }
                set_variable = { which = "imperial_decay" value = 70 }
            }
            '''),
        ((1328, 5, 24), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            ''')
    ],
    'e_hre': [
        ((962, 2, 2), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((973, 5, 7), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((983, 12, 7), 1, '''
            effect = {
                change_variable = { which = "imperial_dynasty_count" value = 1 }
                set_variable = { which = "imperial_decay" value = 5 }
            }
            '''),
        ((1002, 1, 24), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1024, 7, 3), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1039, 6, 4), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1056, 10, 5), 1, '''
            effect = {
                change_variable = { which = "imperial_decay" value = 5 }
                change_variable = { which = "imperial_dynasty_count" value = 1 }
            }
            '''),
        ((1106, 8, 7), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1125, 5, 23), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1152, 2, 15), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1190, 6, 10), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1197, 9, 28), 1, '''
            effect = {
                change_variable = { which = "imperial_dynasty_count" value = 1 }
                change_variable = { which = "imperial_decay" value = 10 }
            }
            '''),
        ((1208, 6, 21), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1250, 12, 13), 1, '''
            effect = { change_variable = { which = "imperial_dynasty_count" value = 1 } }
            '''),
        ((1254, 5, 21), 1, '''
            effect = { set_variable = { which = "imperial_dynasty_count" value = 0 } }
            '''),
        ((1272, 4, 2), 1, '''
            effect = {
                change_variable = { which = "imperial_decay" value = 10 }
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
    ]
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
            if path.stem == 'e_byzantium':
                for n, v in tree[3, 1, 27]:
                    if n.val == 'law' and v.val == 'imperial_administration':
                        v.val = 'administration_2'
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
            assert len(tree[580, 1, 1].contents) == 1
            item = tree[580, 1, 1].contents.pop()
            comments = item.pre_comments
            item.pre_comments = []
            comments.extend(
                [Comment(x) for x in item.inline_str(parser)[0].splitlines()])
            tree[580, 1, 1].ker.pre_comments[:0] = comments
            assert len(tree[797, 1, 1].contents) == 2
            item = tree[797, 1, 1].contents.pop()
            comments = item.pre_comments
            item.pre_comments = []
            comments.extend(
                [Comment(x) for x in item.inline_str(parser)[0].splitlines()])
            tree[797, 1, 1].ker.pre_comments[:0] = comments
            tree[907, 1, 1].contents[:0] = parser.parse('''
                set_global_flag = emf_conquest_hungary_completed
                ''').contents
            tree[1000, 12, 25].contents[:0] = parser.parse('''
                effect = { set_title_flag = ai_converted_catholic }
                ''').contents
            tree.contents[22:22] = parser.parse('''
                895.1.1 = {
                    effect = { set_title_flag = hungary_name_change }
                    set_global_flag = emf_magyar_migration_started
                }
                902.1.1 = {
                    set_global_flag = emf_magyar_migration_completed
                }
                ''').contents
            tree.contents[22].pre_comments = tree.contents[24].pre_comments
            tree.contents[24].pre_comments = []
        elif path.stem == 'k_magyar':
            changed = True
            tree[769, 1, 1].contents[:0] = parser.parse('''
                law = succ_gavelkind
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
            if len(bad) > 0:
                changed = True
                v.contents = [p2 for p2 in v.contents if p2 not in bad]
        if changed:
            tree.contents = [p for p in tree.contents
                             if p.value.contents or p.has_comments]
            targetpath = emfswmhhistory / path.relative_to(swmhhistory)
            parser.write(tree, targetpath)

if __name__ == '__main__':
    main()
