import sys
import os

f = open('./combat_tactics.csv')
array = [line.strip().split(',') for line in f]
f.close()

f = open('./cultural_tactics.csv')
array2 = [line.strip().split(',') for line in f]
f.close()

normal_weight = 3
cultural_weight = 6

cultural_tactics = {
            "finnish":          ("raid_tactic", "quick_attack_tactic"),
            "lappish":          ("raid_tactic", "quick_attack_tactic"),
            "komi":             ("raid_tactic", "quick_attack_tactic"),
            "mordvin":          ("raid_tactic", "quick_attack_tactic"),
            "samoyed":          ("raid_tactic", "quick_attack_tactic"),
            "english":          ("volley_tactic", "longbow_volley_tactic"),
            "welsh":            ("volley_tactic", "longbow_volley_tactic"),
            "ligurian":         ("volley_tactic", "ambush_volley_tactic"),
            "g_iranian":        ("swarm_tactic", "retreat_and_ambush_tactic"),
            "cuman":            ("swarm_tactic", "retreat_and_ambush_tactic"),
            "khazar":           ("swarm_tactic", "retreat_and_ambush_tactic"),
            "pecheneg":         ("swarm_tactic", "retreat_and_ambush_tactic"),
            "mongol":           ("swarm_tactic", "retreat_and_ambush_tactic"),
            "turkish":          ("swarm_tactic", "retreat_and_ambush_tactic"),
            "hungarian":        ("swarm_tactic", "retreat_and_ambush_tactic"),
            "g_west_african":   ("harass_tactic", "missile_harass_tactic"),
            "g_east_african":   ("harass_tactic", "missile_harass_tactic"),
            "italian":          ("melee_charge_tactic", "awesome_charge_tactic"),
            "sicilian":         ("melee_charge_tactic", "awesome_charge_tactic"),
            "bohemian":         ("melee_charge_tactic", "heavy_charge_tactic"),
            "polish":           ("melee_charge_tactic", "combined_charge_tactic"),
            "serbian":          ("melee_charge_tactic", "heavy_charge_tactic"),
            "bulgarian":        ("melee_charge_tactic", "heavy_charge_tactic"),            "russian":          ("melee_charge_tactic", "embolon_charge_tactic"),
            "frankish":         ("melee_charge_tactic", "shock_charge_tactic"),
            "norman":           ("melee_charge_tactic", "heavy_charge_tactic"),
            "breton":           ("melee_charge_tactic", "heavy_charge_tactic"),
            "german":           ("melee_charge_tactic", "heavy_charge_tactic"),
            "alan":             ("melee_charge_tactic", "embolon_charge_tactic"),
            "armenian":         ("melee_charge_tactic", "embolon_charge_tactic"),
            "georgian":         ("melee_charge_tactic", "heavy_charge_tactic"),
            "sardinian":        ("melee_charge_tactic", "awesome_charge_tactic"),
            "corsican":         ("melee_charge_tactic", "awesome_charge_tactic"),
            "central_italian":  ("melee_charge_tactic", "awesome_charge_tactic"),
            "southern_italian": ("melee_charge_tactic", "awesome_charge_tactic"),
            "neapolitan":       ("melee_charge_tactic", "awesome_charge_tactic"),
            "tuscan":           ("melee_charge_tactic", "awesome_charge_tactic"),
            "karantanci":       ("melee_charge_tactic", "combined_charge_tactic"),
            "moravian":         ("melee_charge_tactic", "heavy_charge_tactic"),
            "bosnian":          ("melee_charge_tactic", "combined_charge_tactic"),
            "cornish":          ("melee_charge_tactic", "heavy_charge_tactic"),
            "arpitan":          ("melee_charge_tactic", "shock_charge_tactic"),
            "romanian":         ("raid_tactic", "horseback_raid_tactic"),
            "portuguese":       ("raid_tactic", "horseback_raid_tactic"),
            "castillian":       ("raid_tactic", "horseback_raid_tactic"),
            "catalan":          ("raid_tactic", "quick_attack_tactic"),
            "andalusian_arabic":("raid_tactic", "horseback_raid_tactic"),
            "g_arabic":         ("melee_charge_tactic", "mameluke_raid_tactic"),
            "aragonese":        ("raid_tactic", "horseback_raid_tactic"),
            "galician":         ("raid_tactic", "horseback_raid_tactic"),
            "leonese":          ("raid_tactic", "horseback_raid_tactic"),
            "albanian":         ("raid_tactic", "horseback_raid_tactic"),
            "g_north_african":  ("raid_tactic", "horseback_raid_tactic"),
            "roman":            ("advance_tactic", "roman_triple_line_tactic"),
            "pommeranian":      ("advance_tactic", "infantry_rush_tactic"),
            "croatian":         ("advance_tactic", "infantry_rush_tactic"),
            "irish":            ("advance_tactic", "shield_rush_tactic"),
            "basque":           ("advance_tactic", "intimidating_advance_tactic"),
            "norse":            ("advance_tactic", "infantry_rush_tactic"),
            "norwegian":        ("advance_tactic", "infantry_rush_tactic"),
            "saxon":            ("advance_tactic", "shield_rush_tactic"),
            "lettigallish":     ("advance_tactic", "infantry_rush_tactic"),
            "lithuanian":       ("advance_tactic", "infantry_rush_tactic"),
            "nahuatl":          ("advance_tactic", "aztec_combined_tactic"),
            "jewish":           ("advance_tactic", "shield_rush_tactic"),
            "venetian":         ("advance_tactic", "infantry_rush_tactic"),
            "langobardisch":    ("advance_tactic", "infantry_rush_tactic"),
            "estonian":         ("advance_tactic", "intimidating_advance_tactic"),
            "norsegaelic":      ("advance_tactic", "infantry_rush_tactic"),
            "gothic":           ("advance_tactic", "infantry_rush_tactic"),
            "anglonorse":       ("advance_tactic", "infantry_rush_tactic"),
            "cumbric":          ("advance_tactic", "infantry_rush_tactic"),
            "scottish":         ("stand_fast_tactic", "schiltron_tactic"),
            "dutch":            ("stand_fast_tactic", "pike_assault_tactic"),
            "frisian":          ("stand_fast_tactic", "pike_assault_tactic"),
            "g_indo_aryan_group":("stand_fast_tactic", "gray_wall_tactic"),
            "g_dravidian_group":("stand_fast_tactic", "gray_wall_tactic")
            }

exempt_cultures = {
            "stand_fast_tactic": [],
            "harass_tactic": [],
            "swarm_tactic": [],
            "advance_tactic": [],
            "volley_tactic": [],
            "shieldwall_tactic": [],
            "raid_tactic": [],
            "melee_charge_tactic": []
            }
cultural_tactics_list = {}
matching_tactics_list = {}
for i in cultural_tactics.keys():
    exempt_cultures[cultural_tactics[i][0]] += [i]
    if cultural_tactics[i][1] not in cultural_tactics_list:
        cultural_tactics_list[cultural_tactics[i][1]] = []
        matching_tactics_list[cultural_tactics[i][1]] = cultural_tactics[i][0]
    cultural_tactics_list[cultural_tactics[i][1]] += [i]

base_tactics = """### At the moment we have a pretty basic icon system for combat tactics showing
### the uniticon which has the biggest bonus value in the tactic.
### This is the sprite number for each unit:
### GOOD 1=LI 2=HI 3=PIKE 4=LC 5=KNIGHTS 6=ARCHERS 7=HORSE ARCH.
### Neutral 8=LI 9=HI 10=PIKE 11=LC 12=KNIGHTS 13=ARCHERS 14=HORSE ARCH.
### Bad 15=LI 16=HI 17=PIKE 18=LC 19=KNIGHTS 20=ARCHERS 21=HORSE ARCH.

# Must be first in file. This tactic will be set if anything goes wrong
no_tactic = {
	days = 3 # tactic lasts one day
	sprite = 1 # index of icon

	trigger = {
		always = no # never use unless set explicitly by code
	}
	
	light_infantry_offensive = -0.25
	heavy_infantry_offensive = -0.25
	pikemen_offensive = -0.25
	light_cavalry_offensive = -0.25
	camel_cavalry_offensive = -0.25
	knights_offensive = -0.25
	archers_offensive = -0.25
	horse_archers_offensive = -0.25
	
	light_infantry_defensive = -0.25
	heavy_infantry_defensive = -0.25
	pikemen_defensive = -0.25
	light_cavalry_defensive = -0.25
	camel_cavalry_defensive = -0.25
	knights_defensive = -0.25
	archers_defensive = -0.25
	horse_archers_defensive = -0.25
}

generic_skirmish_tactic = {
	days = 5 # tactic lasts one day
	sprite = 1 # index of icon
	group = skirmish

	trigger = {
		phase = skirmish
			flank_has_leader = no
	}

	mean_time_to_happen = {
		days = 0
	}
}

#### Charge Tactics ####
good_charge_tactic = {
	days = 5
	sprite = 5 # index of icon
	group = charge
	
	trigger = {
		phase = skirmish
		is_flanking = no
		flank_has_leader = yes
		days = 11 # duration of combat >= 10 days
	}

	mean_time_to_happen = {
		days = 6 # this has nothing to do with days, it just represents relative chance of selecting this tactic, higher is better
		modifier = {
			factor = 0.6
			leader = {
				NOT = { martial = 0 }
			}
		}
		modifier = {
			factor = 0.7
			leader = {
				NOT = { martial = 2 }
			}
		}
		modifier = {
			factor = 0.7
			leader = {
				NOT = { martial = 4 }
			}
		}
		modifier = {
			factor = 0.65
			leader = {
				NOT = { martial = 6 }
			}
		}
		modifier = {
			factor = 0.75
			leader = {
				NOT = { martial = 8 }
			}
		}
		modifier = {
			factor = 0.75
			leader = {
				NOT = { martial = 10 }
			}
		}
		modifier = {
			factor = 1.1
			leader = {
				martial = 12
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				martial = 14
			}
		}
		modifier = {
			factor = 1.3
			leader = {
				martial = 16
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 18
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 20
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 22
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 24
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 26
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = knight
				value = 0.3
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = heavy_infantry
				value = 0.3
			}
		}
	}

	change_phase_to = melee
	
	light_infantry_offensive = 0.5
	heavy_infantry_offensive = 0.75
	pikemen_offensive = 1.0
	light_cavalry_offensive = 0.5
	camel_cavalry_offensive = 1.5
	knights_offensive = 1.50
	archers_offensive = 0.25
	horse_archers_offensive = 0.25
	
	light_infantry_defensive = 0
	heavy_infantry_defensive = 0
	pikemen_defensive = 0
	light_cavalry_defensive = 0
	camel_cavalry_defensive = 0
	knights_defensive = 0
	archers_defensive = 0
	horse_archers_defensive = 0
}

charge_tactic = {
	days = 5
	sprite = 5 # index of icon
	group = charge
	
	trigger = {
		phase = skirmish
		is_flanking = no
		flank_has_leader = yes
		days = 11 # duration of combat >= 10 days
	}

	mean_time_to_happen = {
		days = 6 # this has nothing to do with days, it just represents relative chance of selecting this tactic, higher is better
		modifier = {
			factor = 0.8
			leader = {
				NOT = { martial = 0 }
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				NOT = { martial = 2 }
			}
		}
		modifier = {
			factor = 0.9
			leader = {
				NOT = { martial = 4 }
			}
		}
		modifier = {
			factor = 0.9
			leader = {
				NOT = { martial = 6 }
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				NOT = { martial = 8 }
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				NOT = { martial = 10 }
			}
		}
		modifier = {
			factor = 1.1
			leader = {
				martial = 12
			}
		}
		modifier = {
			factor = 1.1
			leader = {
				martial = 14
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 16
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 18
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 20
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 22
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 24
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 26
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = knight
				value = 0.3
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = heavy_infantry
				value = 0.3
			}
		}
	}

	change_phase_to = melee
	
	light_infantry_offensive = 0.25
	heavy_infantry_offensive = 0.5
	pikemen_offensive = 0.75
	light_cavalry_offensive = 0.25
	camel_cavalry_offensive = 1.25
	knights_offensive = 1.25
	archers_offensive = 0
	horse_archers_offensive = 0
	
	light_infantry_defensive = 0
	heavy_infantry_defensive = 0
	pikemen_defensive = 0
	light_cavalry_defensive = 0
	camel_cavalry_defensive = 0
	knights_defensive = 0
	archers_defensive = 0
	horse_archers_defensive = 0
}

bad_charge_tactic = {
	days = 5
	sprite = 5 # index of icon
	group = charge
	
	trigger = {
		phase = skirmish
		is_flanking = no
		flank_has_leader = yes
		days = 11 # duration of combat >= 10 days
	}

	mean_time_to_happen = {
		days = 6 # this has nothing to do with days, it just represents relative chance of selecting this tactic, higher is better
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 0 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 2 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 4 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 6 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 8 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 10 }
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 12
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 14
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 16
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 18
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 20
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 22
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 24
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 26
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = knight
				value = 0.3
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = heavy_infantry
				value = 0.3
			}
		}
	}

	change_phase_to = melee
	
	light_infantry_offensive = 0.25
	heavy_infantry_offensive = 0
	pikemen_offensive = 0.25
	light_cavalry_offensive = 0.25
	camel_cavalry_offensive = 0.75
	knights_offensive = 0.75
	archers_offensive = 0
	horse_archers_offensive = 0
	
	light_infantry_defensive = -0.25
	heavy_infantry_defensive = -0.25
	pikemen_defensive = -0.25
	light_cavalry_defensive = -0.25
	camel_cavalry_defensive = -0.25
	knights_defensive = -0.25
	archers_defensive = -0.25
	horse_archers_defensive = -0.25
}

charge_on_undefended_tactic = {
	days = 5
	sprite = 5
	group = charge
	
	trigger = {
		phase = skirmish
		is_flanking = no
		days = 3 # duration of combat >= 3 days
	}
	
	mean_time_to_happen = {
		days = 100
		modifier = {
			factor = 0
			NOT = { 
				enemy = {
					troops = {
					who = archers
						value = 0.6
					}
				}
			}
		}
	}

	light_infantry_offensive = 0.5
	heavy_infantry_offensive = 0.75
	pikemen_offensive = 1.0
	light_cavalry_offensive = 0.5
	camel_cavalry_offensive = 1.5
	knights_offensive = 1.50
	archers_offensive = 0.25
	horse_archers_offensive = 0.25

	light_infantry_defensive = 0
	heavy_infantry_defensive = 0
	pikemen_defensive = 0
	light_cavalry_defensive = 0
	camel_cavalry_defensive = 0
	knights_defensive = 0
	archers_defensive = 0
	horse_archers_defensive = 0
	
	change_phase_to = melee
}

##########################################################################
# Siege offensive tactics
##########################################################################
# Must be first "siege = attacker"
no_siege_offense_tactic = {
	days = 3 # tactic lasts one day
	sprite = 1 # index of icon
	
	siege = attacker	
	
	trigger = {
		always = no # never use unless set explicitly by code
	}
}

default_siege_offense_tactic = {
	days = 5
	sprite = 1

	siege = attacker	

	trigger = {
		always = yes
	}

	mean_time_to_happen = {
		days = 3
	}
}

##########################################################################
# Siege defensive tactics
##########################################################################

# Must be first "siege = defender"
no_siege_defense_tactic = {
	days = 3 # tactic lasts one day
	sprite = 1 # index of icon
	siege = defender	
	trigger = {
		always = no # never use unless set explicitly by code
	}
}

default_siege_defense_tactic = {
	days = 5
	sprite = 1

	siege = defender
	
	trigger = {
		always = yes
	}

	mean_time_to_happen = {
		days = 3
	}
}

pursue_tactic = {
	days = 15
	sprite = 4
	group = charge
	
	trigger = {
		phase = pursue
	}

	mean_time_to_happen = {
		days = 10
	}
}


##########################################################################
# Combat MTTH definitions(do not remove)
##########################################################################

flank_retreat_odds =
{
	# MTTH range is 0-100, if flank morale is below MTTH, flank will retreat
	mean_time_to_happen = {
		days = 25
	}
}

flank_pursue_odds =
{
	# MTTH range is 0-100, chance (in %) of pursuing a fleeing flank
	mean_time_to_happen = {
		days = 25
	}
}\n"""

big_ol_block_of_conditionals = {
            "melee_charge_tactic": """		OR = {
			knights = 0.01
			OR = {
				light_cavalry = 0.01
				camel_cavalry = 0.01
			}
			horse_archers = 0.01
		}
		NOT = { AND = {
			OR = {
				light_infantry = 0.60
				heavy_infantry = 0.30
				pikemen = 0.30
				war_elephants = 0.03
				archers = 0.30
			}
			NOT = {
				OR = {
					knights = 0.16
					AND = { 
						horse_archers = 0.30
						OR = {
							knights = 0.10
							NOT = { light_cavalry = 0.10 }
							NOT = { camel_cavalry = 0.10 }
						}
					}
					AND = {
						light_cavalry = 0.30
						OR = {
							knights = 0.10
							NOT = { camel_cavalry = 0.10 }
							NOT = { horse_archers = 0.10 }
						}
					}
					camel_cavalry = 0.30
				}
			}
		} }""",
            "raid_tactic": """		OR = {
			light_infantry = 0.01
			OR = {
				light_cavalry = 0.01
				camel_cavalry = 0.01
			}
			horse_archers = 0.01
		}
		NOT = { AND = {
			OR = {
				knights = 0.16
				heavy_infantry = 0.30
				pikemen = 0.30
				war_elephants = 0.03
				archers = 0.30
			}
			NOT = {
				OR = {
					AND = {
						light_infantry = 0.60
						OR = {
							NOT = { heavy_infantry = 0.10 }
							horse_archers = 0.10
							light_cavalry = 0.10
							camel_cavalry = 0.10
						}
					}
					AND = { 
						horse_archers = 0.30
						OR = {
							NOT = { knights = 0.10 }
							light_cavalry = 0.10
							camel_cavalry = 0.10
						}
					}
					AND = {
						light_cavalry = 0.30
						OR = {
							NOT = { knights = 0.10 }
							NOT = { camel_cavalry = 0.10 }
							horse_archers = 0.10
						}
					}
				}
			}
		} }""",
            "advance_tactic": """		OR = {
			light_infantry = 0.01
			heavy_infantry = 0.01
			pikemen = 0.01
			war_elephants = 0.01
		}
		NOT = { AND = {
			OR = {
				knights = 0.16
				light_cavalry = 0.30
				camel_cavalry = 0.30
				horse_archers = 0.30
				archers = 0.30
			}
			NOT = {
				OR = {
					heavy_infantry = 0.30
					AND = { 
						light_infantry = 0.60
						OR = {
							heavy_infantry = 0.10
							NOT = {
								horse_archers = 0.10
								light_cavalry = 0.10
								camel_cavalry = 0.10
							}
						}
					}
					AND = {
						OR = {
                                                    pikemen = 0.30
                                                    war_elephants = 0.03
                                                }
						OR = {
							NOT = { archers = 0.10 }
							heavy_infantry = 0.10
						}
					}
				}
			}
		} }""",
            "stand_fast_tactic": """		OR = {
			archers = 0.01
			heavy_infantry = 0.01
			war_elephants = 0.01
			pikemen = 0.01
		}
		NOT = { AND = {
			OR = {
				knights = 0.16
				light_cavalry = 0.30
				camel_cavalry = 0.30
				horse_archers = 0.30
				light_infantry = 0.60
			}
			NOT = {
				OR = {
					pikemen = 0.30
					archers = 0.30
					war_elephants = 0.30
					AND = {
						heavy_infantry = 0.30
						OR = {
							pikemen = 0.10
							archers = 0.10
						}
					}
				}
			}
		} }""",
            "harass_tactic": """		OR = {
			light_cavalry = 0.01
			camel_cavalry = 0.01
			light_infantry = 0.01
		}""",
            "volley_tactic": """		archers = 0.01""",
            "swarm_tactic": """		horse_archers = 0.01""",
            "shieldwall_tactic": """""",
            "good": """\t\tmodifier = {
			factor = 0.6
			leader = {
				NOT = { martial = 0 }
			}
		}
		modifier = {
			factor = 0.7
			leader = {
				NOT = { martial = 2 }
			}
		}
		modifier = {
			factor = 0.7
			leader = {
				NOT = { martial = 4 }
			}
		}
		modifier = {
			factor = 0.65
			leader = {
				NOT = { martial = 6 }
			}
		}
		modifier = {
			factor = 0.75
			leader = {
				NOT = { martial = 8 }
			}
		}
		modifier = {
			factor = 0.75
			leader = {
				NOT = { martial = 10 }
			}
		}
		modifier = {
			factor = 1.1
			leader = {
				martial = 12
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				martial = 14
			}
		}
		modifier = {
			factor = 1.3
			leader = {
				martial = 16
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 18
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 20
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 22
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 24
			}
		}
		modifier = {
			factor = 1.35
			leader = {
				martial = 26
			}
		}""",
            "normal": """\t\tmodifier = {
			factor = 0.8
			leader = {
				NOT = { martial = 0 }
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				NOT = { martial = 2 }
			}
		}
		modifier = {
			factor = 0.9
			leader = {
				NOT = { martial = 4 }
			}
		}
		modifier = {
			factor = 0.9
			leader = {
				NOT = { martial = 6 }
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				NOT = { martial = 8 }
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				NOT = { martial = 10 }
			}
		}
		modifier = {
			factor = 1.1
			leader = {
				martial = 12
			}
		}
		modifier = {
			factor = 1.1
			leader = {
				martial = 14
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 16
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 18
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 20
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 22
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 24
			}
		}
		modifier = {
			factor = 1.05
			leader = {
				martial = 26
			}
		}""",
            "bad": """\t\tmodifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 0 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 2 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 4 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 6 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 8 }
			}
		}
		modifier = {
			factor = 1.2
			leader = {
				NOT = { martial = 10 }
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 12
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 14
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 16
			}
		}
		modifier = {
			factor = 0.95
			leader = {
				martial = 18
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 20
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 22
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 24
			}
		}
		modifier = {
			factor = 0.8
			leader = {
				martial = 26
			}
		}"""
            }

combat_tactics = ""
localization = "#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x\n"
localization += "good_charge_tactic;Devestating Charge Tactic;;;;;;;;;;;;;x\n"
localization += "bad_charge_tactic;Failed Charge Tactic;;;;;;;;;;;;;x\n"

for i in xrange(1,len(array[0])):
    tactic_name = array[0][i]
    tactic_values = {}
    for j in xrange(1,len(array)):
        tactic_values[array[j][0]] = array[j][i]
    combat_tactics += "good_"+tactic_name+" = {\n";
    localization += "good_"+tactic_name+";Devastating "+tactic_values["name"]+" Tactic;;;;;;;;;;;;;x\n"
    combat_tactics += "\tdays = "+tactic_values["days"]+"\n"
    combat_tactics += "\tsprite = "+str(int(tactic_values["sprite"])-7)+"\n"
    combat_tactics += "\tgroup = "+tactic_values["group"]+"\n"
    combat_tactics += "\ttrigger = {\n"
    combat_tactics += "\t\tphase = "+tactic_values["phase"]+"\n"
    combat_tactics += big_ol_block_of_conditionals[tactic_name] + "\n"
    combat_tactics += "\t\tflank_has_leader = yes\n"
    if exempt_cultures[tactic_name] != []:
        combat_tactics += "\t\tNOT = {\n"
        combat_tactics += "\t\t\tleader = {\n"
        combat_tactics += "\t\t\t\tOR = {\n"
        for k in exempt_cultures[tactic_name]:
            if k[0:2] == "g_":
                combat_tactics += "\t\t\t\t\tculture_group = "+k[2:]+"\n"
            else:
                combat_tactics += "\t\t\t\t\tculture = "+k+"\n"
        combat_tactics += "\t\t\t\t}\n"
        combat_tactics += "\t\t\t}\n"
        combat_tactics += "\t\t}\n" # now the not is closed
    combat_tactics += "\t}\n"
    combat_tactics += "\n"
    combat_tactics += "\tmean_time_to_happen = {\n"
    combat_tactics += "\t\tdays = "+str(normal_weight)+"\n"
    combat_tactics += big_ol_block_of_conditionals['good']+"\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\tlight_infantry_offensive = "+str(float(tactic_values["light_infantry_offensive"])+0.25)+"\n"
    combat_tactics += "\theavy_infantry_offensive = "+str(float(tactic_values["heavy_infantry_offensive"])+0.25)+"\n"
    combat_tactics += "\tpikemen_offensive = "+str(float(tactic_values["pikemen_offensive"])+0.25)+"\n"
    combat_tactics += "\tlight_cavalry_offensive = "+str(float(tactic_values["light_cavalry_offensive"])+0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_offensive = "+str(float(tactic_values["camel_cavalry_offensive"])+0.25)+"\n"
    combat_tactics += "\tknights_offensive = "+str(float(tactic_values["knights_offensive"])+0.25)+"\n"
    combat_tactics += "\tarchers_offensive = "+str(float(tactic_values["archers_offensive"])+0.25)+"\n"
    combat_tactics += "\thorse_archers_offensive = "+str(float(tactic_values["horse_archers_offensive"])+0.25)+"\n"
    combat_tactics += "\twar_elephants_offensive = "+str(float(tactic_values["war_elephants_offensive"])+0.25)+"\n"
    combat_tactics += "\n"
    combat_tactics += "\tlight_infantry_defensive = "+str(float(tactic_values["light_infantry_defensive"])+0.25)+"\n"
    combat_tactics += "\theavy_infantry_defensive = "+str(float(tactic_values["heavy_infantry_defensive"])+0.25)+"\n"
    combat_tactics += "\tpikemen_defensive = "+str(float(tactic_values["pikemen_defensive"])+0.25)+"\n"
    combat_tactics += "\tlight_cavalry_defensive = "+str(float(tactic_values["light_cavalry_defensive"])+0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_defensive = "+str(float(tactic_values["camel_cavalry_defensive"])+0.25)+"\n"
    combat_tactics += "\tknights_defensive = "+str(float(tactic_values["knights_defensive"])+0.25)+"\n"
    combat_tactics += "\tarchers_defensive = "+str(float(tactic_values["archers_defensive"])+0.25)+"\n"
    combat_tactics += "\thorse_archers_defensive = "+str(float(tactic_values["horse_archers_defensive"])+0.25)+"\n"
    combat_tactics += "\twar_elephants_defensive = "+str(float(tactic_values["war_elephants_defensive"])+0.25)+"\n"
    combat_tactics += "\tenemy = {\n"
    combat_tactics += "\t\tgroup = "+tactic_values["enemy"]+"\n"
    combat_tactics += "\t\tfactor = 1\n"
    combat_tactics += "\t}\n"
    combat_tactics += "}\n"

    combat_tactics += tactic_name+" = {\n";
    localization += tactic_name+";"+tactic_values["name"]+" Tactic;;;;;;;;;;;;;x\n"
    combat_tactics += "\tdays = "+tactic_values["days"]+"\n"
    combat_tactics += "\tsprite = "+str(int(tactic_values["sprite"])-7)+"\n"
    combat_tactics += "\tgroup = "+tactic_values["group"]+"\n"
    combat_tactics += "\ttrigger = {\n"
    combat_tactics += "\t\tphase = "+tactic_values["phase"]+"\n"
    combat_tactics += big_ol_block_of_conditionals[tactic_name] + "\n"
    combat_tactics += "\t\tflank_has_leader = yes\n"
    if exempt_cultures[tactic_name] != []:
        combat_tactics += "\t\tNOT = {\n"
        combat_tactics += "\t\t\tleader = {\n"
        combat_tactics += "\t\t\t\tOR = {\n"
        for k in exempt_cultures[tactic_name]:
            if k[0:2] == "g_":
                combat_tactics += "\t\t\t\t\tculture_group = "+k[2:]+"\n"
            else:
                combat_tactics += "\t\t\t\t\tculture = "+k+"\n"
        combat_tactics += "\t\t\t\t}\n"
        combat_tactics += "\t\t\t}\n"
        combat_tactics += "\t\t}\n" # now the not is closed
    combat_tactics += "\t}\n"
    combat_tactics += "\n"
    combat_tactics += "\tmean_time_to_happen = {\n"
    combat_tactics += "\t\tdays = "+str(normal_weight)+"\n"
    combat_tactics += big_ol_block_of_conditionals['normal']+"\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\tlight_infantry_offensive = "+str(float(tactic_values["light_infantry_offensive"])+0)+"\n"
    combat_tactics += "\theavy_infantry_offensive = "+str(float(tactic_values["heavy_infantry_offensive"])+0)+"\n"
    combat_tactics += "\tpikemen_offensive = "+str(float(tactic_values["pikemen_offensive"])+0)+"\n"
    combat_tactics += "\tlight_cavalry_offensive = "+str(float(tactic_values["light_cavalry_offensive"])+0)+"\n"
    combat_tactics += "\tcamel_cavalry_offensive = "+str(float(tactic_values["camel_cavalry_offensive"])+0)+"\n"
    combat_tactics += "\tknights_offensive = "+str(float(tactic_values["knights_offensive"])+0)+"\n"
    combat_tactics += "\tarchers_offensive = "+str(float(tactic_values["archers_offensive"])+0)+"\n"
    combat_tactics += "\thorse_archers_offensive = "+str(float(tactic_values["horse_archers_offensive"])+0)+"\n"
    combat_tactics += "\twar_elephants_offensive = "+str(float(tactic_values["war_elephants_offensive"])+0)+"\n"
    combat_tactics += "\n"
    combat_tactics += "\tlight_infantry_defensive = "+str(float(tactic_values["light_infantry_defensive"])+0)+"\n"
    combat_tactics += "\theavy_infantry_defensive = "+str(float(tactic_values["heavy_infantry_defensive"])+0)+"\n"
    combat_tactics += "\tpikemen_defensive = "+str(float(tactic_values["pikemen_defensive"])+0)+"\n"
    combat_tactics += "\tlight_cavalry_defensive = "+str(float(tactic_values["light_cavalry_defensive"])+0)+"\n"
    combat_tactics += "\tcamel_cavalry_defensive = "+str(float(tactic_values["camel_cavalry_defensive"])+0)+"\n"
    combat_tactics += "\tknights_defensive = "+str(float(tactic_values["knights_defensive"])+0)+"\n"
    combat_tactics += "\tarchers_defensive = "+str(float(tactic_values["archers_defensive"])+0)+"\n"
    combat_tactics += "\thorse_archers_defensive = "+str(float(tactic_values["horse_archers_defensive"])+0)+"\n"
    combat_tactics += "\twar_elephants_defensive = "+str(float(tactic_values["war_elephants_defensive"])+0)+"\n"
    combat_tactics += "\tenemy = {\n"
    combat_tactics += "\t\tgroup = "+tactic_values["enemy"]+"\n"
    combat_tactics += "\t\tfactor = 1\n"
    combat_tactics += "\t}\n"
    combat_tactics += "}\n"

    combat_tactics += "bad_"+tactic_name+" = {\n";
    localization += "bad_"+tactic_name+";Failed "+tactic_values["name"]+" Tactic;;;;;;;;;;;;;x\n"
    combat_tactics += "\tdays = "+tactic_values["days"]+"\n"
    combat_tactics += "\tsprite = "+str(int(tactic_values["sprite"])-7)+"\n"
    combat_tactics += "\tgroup = "+tactic_values["group"]+"\n"
    combat_tactics += "\ttrigger = {\n"
    combat_tactics += "\t\tphase = "+tactic_values["phase"]+"\n"
    combat_tactics += big_ol_block_of_conditionals[tactic_name] + "\n"
    combat_tactics += "\t\tflank_has_leader = yes\n"
    if exempt_cultures[tactic_name] != []:
        combat_tactics += "\t\tNOT = {\n"
        combat_tactics += "\t\t\tleader = {\n"
        combat_tactics += "\t\t\t\tOR = {\n"
        for k in exempt_cultures[tactic_name]:
            if k[0:2] == "g_":
                combat_tactics += "\t\t\t\t\tculture_group = "+k[2:]+"\n"
            else:
                combat_tactics += "\t\t\t\t\tculture = "+k+"\n"
        combat_tactics += "\t\t\t\t}\n"
        combat_tactics += "\t\t\t}\n"
        combat_tactics += "\t\t}\n" # now the not is closed
    combat_tactics += "\t}\n"
    combat_tactics += "\n"
    combat_tactics += "\tmean_time_to_happen = {\n"
    combat_tactics += "\t\tdays = "+str(normal_weight)+"\n"
    combat_tactics += big_ol_block_of_conditionals['bad']+"\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\tlight_infantry_offensive = "+str(float(tactic_values["light_infantry_offensive"])-0.25)+"\n"
    combat_tactics += "\theavy_infantry_offensive = "+str(float(tactic_values["heavy_infantry_offensive"])-0.25)+"\n"
    combat_tactics += "\tpikemen_offensive = "+str(float(tactic_values["pikemen_offensive"])-0.25)+"\n"
    combat_tactics += "\tlight_cavalry_offensive = "+str(float(tactic_values["light_cavalry_offensive"])-0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_offensive = "+str(float(tactic_values["camel_cavalry_offensive"])-0.25)+"\n"
    combat_tactics += "\tknights_offensive = "+str(float(tactic_values["knights_offensive"])-0.25)+"\n"
    combat_tactics += "\tarchers_offensive = "+str(float(tactic_values["archers_offensive"])-0.25)+"\n"
    combat_tactics += "\thorse_archers_offensive = "+str(float(tactic_values["horse_archers_offensive"])-0.25)+"\n"
    combat_tactics += "\twar_elephants_offensive = "+str(float(tactic_values["war_elephants_offensive"])-0.25)+"\n"
    combat_tactics += "\n"
    combat_tactics += "\tlight_infantry_defensive = "+str(float(tactic_values["light_infantry_defensive"])-0.25)+"\n"
    combat_tactics += "\theavy_infantry_defensive = "+str(float(tactic_values["heavy_infantry_defensive"])-0.25)+"\n"
    combat_tactics += "\tpikemen_defensive = "+str(float(tactic_values["pikemen_defensive"])-0.25)+"\n"
    combat_tactics += "\tlight_cavalry_defensive = "+str(float(tactic_values["light_cavalry_defensive"])-0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_defensive = "+str(float(tactic_values["camel_cavalry_defensive"])-0.25)+"\n"
    combat_tactics += "\tknights_defensive = "+str(float(tactic_values["knights_defensive"])-0.25)+"\n"
    combat_tactics += "\tarchers_defensive = "+str(float(tactic_values["archers_defensive"])-0.25)+"\n"
    combat_tactics += "\thorse_archers_defensive = "+str(float(tactic_values["horse_archers_defensive"])-0.25)+"\n"
    combat_tactics += "\twar_elephants_defensive = "+str(float(tactic_values["war_elephants_defensive"])-0.25)+"\n"
    combat_tactics += "\tenemy = {\n"
    combat_tactics += "\t\tgroup = "+tactic_values["enemy"]+"\n"
    combat_tactics += "\t\tfactor = 1\n"
    combat_tactics += "\t}\n"
    combat_tactics += "}\n"

for i in xrange(1,len(array2[0])):
    tactic_name = array2[0][i]
    tactic_values = {}
    for j in xrange(1,len(array2)):
        tactic_values[array2[j][0]] = array2[j][i]
    combat_tactics += "good_"+tactic_name+" = {\n";
    localization += "good_"+tactic_name+";Devastating "+tactic_values["name"]+" Tactic;;;;;;;;;;;;;x\n"
    combat_tactics += "\tdays = "+tactic_values["days"]+"\n"
    combat_tactics += "\tsprite = "+str(int(tactic_values["sprite"])-7)+"\n"
    combat_tactics += "\tgroup = "+tactic_values["group"]+"\n"
    combat_tactics += "\ttrigger = {\n"
    combat_tactics += "\t\tphase = "+tactic_values["phase"]+"\n"
    combat_tactics += big_ol_block_of_conditionals[matching_tactics_list[tactic_name]] + "\n"
    combat_tactics += "\t\tflank_has_leader = yes\n"
    if cultural_tactics_list[tactic_name] != []:
        combat_tactics += "\t\tleader = {\n"
        combat_tactics += "\t\t\tOR = {\n"
        for k in cultural_tactics_list[tactic_name]:
            if k[0:2] == "g_":
                combat_tactics += "\t\t\t\tculture_group = "+k[2:]+"\n"
            else:
                combat_tactics += "\t\t\t\tculture = "+k+"\n"
        combat_tactics += "\t\t\t}\n"
        combat_tactics += "\t\t}\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\n"
    combat_tactics += "\tmean_time_to_happen = {\n"
    combat_tactics += "\t\tdays = "+str(normal_weight)+"\n"
    combat_tactics += big_ol_block_of_conditionals['good']+"\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\tlight_infantry_offensive = "+str(float(tactic_values["light_infantry_offensive"])+0.25)+"\n"
    combat_tactics += "\theavy_infantry_offensive = "+str(float(tactic_values["heavy_infantry_offensive"])+0.25)+"\n"
    combat_tactics += "\tpikemen_offensive = "+str(float(tactic_values["pikemen_offensive"])+0.25)+"\n"
    combat_tactics += "\tlight_cavalry_offensive = "+str(float(tactic_values["light_cavalry_offensive"])+0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_offensive = "+str(float(tactic_values["camel_cavalry_offensive"])+0.25)+"\n"
    combat_tactics += "\tknights_offensive = "+str(float(tactic_values["knights_offensive"])+0.25)+"\n"
    combat_tactics += "\tarchers_offensive = "+str(float(tactic_values["archers_offensive"])+0.25)+"\n"
    combat_tactics += "\thorse_archers_offensive = "+str(float(tactic_values["horse_archers_offensive"])+0.25)+"\n"
    combat_tactics += "\twar_elephants_offensive = "+str(float(tactic_values["war_elephants_offensive"])+0.25)+"\n"
    combat_tactics += "\n"
    combat_tactics += "\tlight_infantry_defensive = "+str(float(tactic_values["light_infantry_defensive"])+0.25)+"\n"
    combat_tactics += "\theavy_infantry_defensive = "+str(float(tactic_values["heavy_infantry_defensive"])+0.25)+"\n"
    combat_tactics += "\tpikemen_defensive = "+str(float(tactic_values["pikemen_defensive"])+0.25)+"\n"
    combat_tactics += "\tlight_cavalry_defensive = "+str(float(tactic_values["light_cavalry_defensive"])+0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_defensive = "+str(float(tactic_values["camel_cavalry_defensive"])+0.25)+"\n"
    combat_tactics += "\tknights_defensive = "+str(float(tactic_values["knights_defensive"])+0.25)+"\n"
    combat_tactics += "\tarchers_defensive = "+str(float(tactic_values["archers_defensive"])+0.25)+"\n"
    combat_tactics += "\thorse_archers_defensive = "+str(float(tactic_values["horse_archers_defensive"])+0.25)+"\n"
    combat_tactics += "\twar_elephants_defensive = "+str(float(tactic_values["war_elephants_defensive"])+0.25)+"\n"
    combat_tactics += "\tenemy = {\n"
    combat_tactics += "\t\tgroup = "+tactic_values["enemy"]+"\n"
    combat_tactics += "\t\tfactor = 1\n"
    combat_tactics += "\t}\n"
    combat_tactics += "}\n"

    combat_tactics += tactic_name+" = {\n";
    localization += tactic_name+";"+tactic_values["name"]+" Tactic;;;;;;;;;;;;;x\n"
    combat_tactics += "\tdays = "+tactic_values["days"]+"\n"
    combat_tactics += "\tsprite = "+str(int(tactic_values["sprite"])-7)+"\n"
    combat_tactics += "\tgroup = "+tactic_values["group"]+"\n"
    combat_tactics += "\ttrigger = {\n"
    combat_tactics += "\t\tphase = "+tactic_values["phase"]+"\n"
    combat_tactics += big_ol_block_of_conditionals[matching_tactics_list[tactic_name]] + "\n"
    combat_tactics += "\t\tflank_has_leader = yes\n"
    if cultural_tactics_list[tactic_name] != []:
        combat_tactics += "\t\tleader = {\n"
        combat_tactics += "\t\t\tOR = {\n"
        for k in cultural_tactics_list[tactic_name]:
            if k[0:2] == "g_":
                combat_tactics += "\t\t\t\tculture_group = "+k[2:]+"\n"
            else:
                combat_tactics += "\t\t\t\tculture = "+k+"\n"
        combat_tactics += "\t\t\t}\n"
        combat_tactics += "\t\t}\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\n"
    combat_tactics += "\tmean_time_to_happen = {\n"
    combat_tactics += "\t\tdays = "+str(normal_weight)+"\n"
    combat_tactics += big_ol_block_of_conditionals['normal']+"\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\tlight_infantry_offensive = "+str(float(tactic_values["light_infantry_offensive"])+0)+"\n"
    combat_tactics += "\theavy_infantry_offensive = "+str(float(tactic_values["heavy_infantry_offensive"])+0)+"\n"
    combat_tactics += "\tpikemen_offensive = "+str(float(tactic_values["pikemen_offensive"])+0)+"\n"
    combat_tactics += "\tlight_cavalry_offensive = "+str(float(tactic_values["light_cavalry_offensive"])+0)+"\n"
    combat_tactics += "\tcamel_cavalry_offensive = "+str(float(tactic_values["camel_cavalry_offensive"])+0)+"\n"
    combat_tactics += "\tknights_offensive = "+str(float(tactic_values["knights_offensive"])+0)+"\n"
    combat_tactics += "\tarchers_offensive = "+str(float(tactic_values["archers_offensive"])+0)+"\n"
    combat_tactics += "\thorse_archers_offensive = "+str(float(tactic_values["horse_archers_offensive"])+0)+"\n"
    combat_tactics += "\twar_elephants_offensive = "+str(float(tactic_values["war_elephants_offensive"])+0)+"\n"
    combat_tactics += "\n"
    combat_tactics += "\tlight_infantry_defensive = "+str(float(tactic_values["light_infantry_defensive"])+0)+"\n"
    combat_tactics += "\theavy_infantry_defensive = "+str(float(tactic_values["heavy_infantry_defensive"])+0)+"\n"
    combat_tactics += "\tpikemen_defensive = "+str(float(tactic_values["pikemen_defensive"])+0)+"\n"
    combat_tactics += "\tlight_cavalry_defensive = "+str(float(tactic_values["light_cavalry_defensive"])+0)+"\n"
    combat_tactics += "\tcamel_cavalry_defensive = "+str(float(tactic_values["camel_cavalry_defensive"])+0)+"\n"
    combat_tactics += "\tknights_defensive = "+str(float(tactic_values["knights_defensive"])+0)+"\n"
    combat_tactics += "\tarchers_defensive = "+str(float(tactic_values["archers_defensive"])+0)+"\n"
    combat_tactics += "\thorse_archers_defensive = "+str(float(tactic_values["horse_archers_defensive"])+0)+"\n"
    combat_tactics += "\twar_elephants_defensive = "+str(float(tactic_values["war_elephants_defensive"])+0)+"\n"
    combat_tactics += "\tenemy = {\n"
    combat_tactics += "\t\tgroup = "+tactic_values["enemy"]+"\n"
    combat_tactics += "\t\tfactor = 1\n"
    combat_tactics += "\t}\n"
    combat_tactics += "}\n"

    combat_tactics += "bad_"+tactic_name+" = {\n";
    localization += "bad_"+tactic_name+";Failed "+tactic_values["name"]+" Tactic;;;;;;;;;;;;;x\n"
    combat_tactics += "\tdays = "+tactic_values["days"]+"\n"
    combat_tactics += "\tsprite = "+str(int(tactic_values["sprite"])-7)+"\n"
    combat_tactics += "\tgroup = "+tactic_values["group"]+"\n"
    combat_tactics += "\ttrigger = {\n"
    combat_tactics += "\t\tphase = "+tactic_values["phase"]+"\n"
    combat_tactics += big_ol_block_of_conditionals[matching_tactics_list[tactic_name]] + "\n"
    combat_tactics += "\t\tflank_has_leader = yes\n"
    if cultural_tactics_list[tactic_name] != []:
        combat_tactics += "\t\tleader = {\n"
        combat_tactics += "\t\t\tOR = {\n"
        for k in cultural_tactics_list[tactic_name]:
            if k[0:2] == "g_":
                combat_tactics += "\t\t\t\tculture_group = "+k[2:]+"\n"
            else:
                combat_tactics += "\t\t\t\tculture = "+k+"\n"
        combat_tactics += "\t\t\t}\n"
        combat_tactics += "\t\t}\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\n"
    combat_tactics += "\tmean_time_to_happen = {\n"
    combat_tactics += "\t\tdays = "+str(normal_weight)+"\n"
    combat_tactics += big_ol_block_of_conditionals['bad']+"\n"
    combat_tactics += "\t}\n"
    combat_tactics += "\tlight_infantry_offensive = "+str(float(tactic_values["light_infantry_offensive"])-0.25)+"\n"
    combat_tactics += "\theavy_infantry_offensive = "+str(float(tactic_values["heavy_infantry_offensive"])-0.25)+"\n"
    combat_tactics += "\tpikemen_offensive = "+str(float(tactic_values["pikemen_offensive"])-0.25)+"\n"
    combat_tactics += "\tlight_cavalry_offensive = "+str(float(tactic_values["light_cavalry_offensive"])-0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_offensive = "+str(float(tactic_values["camel_cavalry_offensive"])-0.25)+"\n"
    combat_tactics += "\tknights_offensive = "+str(float(tactic_values["knights_offensive"])-0.25)+"\n"
    combat_tactics += "\tarchers_offensive = "+str(float(tactic_values["archers_offensive"])-0.25)+"\n"
    combat_tactics += "\thorse_archers_offensive = "+str(float(tactic_values["horse_archers_offensive"])-0.25)+"\n"
    combat_tactics += "\twar_elephants_offensive = "+str(float(tactic_values["war_elephants_offensive"])-0.25)+"\n"
    combat_tactics += "\n"
    combat_tactics += "\tlight_infantry_defensive = "+str(float(tactic_values["light_infantry_defensive"])-0.25)+"\n"
    combat_tactics += "\theavy_infantry_defensive = "+str(float(tactic_values["heavy_infantry_defensive"])-0.25)+"\n"
    combat_tactics += "\tpikemen_defensive = "+str(float(tactic_values["pikemen_defensive"])-0.25)+"\n"
    combat_tactics += "\tlight_cavalry_defensive = "+str(float(tactic_values["light_cavalry_defensive"])-0.25)+"\n"
    combat_tactics += "\tcamel_cavalry_defensive = "+str(float(tactic_values["camel_cavalry_defensive"])-0.25)+"\n"
    combat_tactics += "\tknights_defensive = "+str(float(tactic_values["knights_defensive"])-0.25)+"\n"
    combat_tactics += "\tarchers_defensive = "+str(float(tactic_values["archers_defensive"])-0.25)+"\n"
    combat_tactics += "\thorse_archers_defensive = "+str(float(tactic_values["horse_archers_defensive"])-0.25)+"\n"
    combat_tactics += "\twar_elephants_defensive = "+str(float(tactic_values["war_elephants_defensive"])-0.25)+"\n"
    combat_tactics += "\tenemy = {\n"
    combat_tactics += "\t\tgroup = "+tactic_values["enemy"]+"\n"
    combat_tactics += "\t\tfactor = 1\n"
    combat_tactics += "\t}\n"
    combat_tactics += "}\n"
                
combat_tactics = base_tactics + combat_tactics
f = open(".."+os.sep+"common"+os.sep+"combat_tactics.txt", "w")
f.write(combat_tactics)
f.close()
f = open(".."+os.sep+"localisation"+os.sep+"emf_sts.csv", "w")
f.write(localization)
f.close()
