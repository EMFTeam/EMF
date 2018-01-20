-- Diplomacy
NDefines.NDiplomacy.VASSAL_LIMIT_LEVY_MULTIPLIER = 0
NDefines.NDiplomacy.TITULAR_TITLES_COUNT_TOWARDS_DUCHY_LIMIT = 0                    -- from 1
NDefines.NDiplomacy.LAW_CHANGE_PRESTIGE_COST = 150                                  -- from 100
NDefines.NDiplomacy.CROWN_LAW_CHANGE_PRESTIGE_COST = 300                            -- from 200
NDefines.NDiplomacy.INTER_MUSLIM_WAR_MONTHLY_PIETY_COST = 1
NDefines.NDiplomacy.MUSLIM_TEMPLE_HOLDING_MONTHLY_PIETY = 0.4
NDefines.NDiplomacy.BASE_REVOLT_CHANCE_MOD = 175                                    -- from 250
NDefines.NDiplomacy.TOG_REVOLT_CHANCE_MOD = 70                                      -- from 100
NDefines.NDiplomacy.DUKE_POWERFUL_VASSAL_COUNT = 3
NDefines.NDiplomacy.KING_POWERFUL_VASSAL_COUNT = 4
NDefines.NDiplomacy.EMPEROR_POWERFUL_VASSAL_COUNT = 5
NDefines.NDiplomacy.IMPRISON_CHARACTER_INTERACTION_PIETY = 0
NDefines.NDiplomacy.EXECUTE_IMPRISONED_INTERACTION_PIETY = 10
NDefines.NDiplomacy.DEMAND_RELIGIOUS_CONVERSION_INTERACTION_PIETY = 25              -- from 0
NDefines.NDiplomacy.DEMAND_RELIGIOUS_CONVERSION_INTERACTION_PRESTIGE = 50           -- from 0
NDefines.NDiplomacy.DEMAND_RELIGIOUS_CONVERSION_INTERACTION_THRESHOLD_FOR_YES = 35  -- from 25
NDefines.NDiplomacy.INVITE_TO_COURT_INTERACTION_MONEY = 10                          -- from 0
NDefines.NDiplomacy.ASK_FOR_INVASION_INTERACTION_THRESHOLD_FOR_YES = 100
NDefines.NDiplomacy.DEFENSIVE_PACT_THREAT_LIMIT = 0.15
NDefines.NDiplomacy.DEFENSIVE_PACT_MAX_RANGE = 300

-- Council
NDefines.NCouncil.ENFORCE_PEACE_START_DELAY = 6
NDefines.NCouncil.LAW_VOTE_CHANGE_TIME_LIMIT = 2

-- Infamy
NDefines.NInfamy.REALM_SIZE_GROWTH_MODIFIER = 0.0
NDefines.NInfamy.WAR_REALM_CHANGE_VALUE = 0.5
NDefines.NInfamy.INDEPENDENCE_REALM_CHANGE_VALUE = 0.1
NDefines.NInfamy.INHERITANCE_CHANGE_VALUE = 0.05
NDefines.NInfamy.VASSAL_CHANGE_VALUE = 0
NDefines.NInfamy.MAX_INFAMY_PER_WAR_PROVINCE = 5
NDefines.NInfamy.MIN_INFAMY_PER_WAR_PROVINCE = 0

-- Character
NDefines.NCharacter.CHANGE_AMBITION_YEARS = 1
NDefines.NCharacter.CHANGE_FOCUS_YEARS = 3
NDefines.NCharacter.PRESTIGE_FROM_DYNASTY_ON_BIRTH_DIV = 15
NDefines.NCharacter.PRESTIGE_FROM_DYNASTY_ON_MARRIAGE_DIV = 15
NDefines.NCharacter.ASSIGN_ACTION_DAYS = 92
NDefines.NCharacter.RAISED_TROOPS_VASSAL_OPINION_DAYS = 42
NDefines.NCharacter.MAX_JOINED_FACTIONS = 4
NDefines.NCharacter.NON_AGGRESSION_PACT_BLOCKS_FACTIONS = 0
NDefines.NCharacter.PORTRAIT_ADULT_MALE_AGE_THRESHOLD = 14
NDefines.NCharacter.PORTRAIT_ADULT_FEMALE_AGE_THRESHOLD = 14
NDefines.NCharacter.PORTRAIT_MID_AGE_THRESHOLD = 32
NDefines.NCharacter.AGE_OF_MARRIAGE_MALE = 14
NDefines.NCharacter.AGE_OF_MARRIAGE_FEMALE = 14
NDefines.NCharacter.AGE_VERY_OLD = 60
NDefines.NCharacter.NATURAL_DEATH_CHANCE_AGE_60 = 600
NDefines.NCharacter.NATURAL_DEATH_CHANCE_AGE_70 = 2100
NDefines.NCharacter.SECONDARY_SPOUSE_FERTILITY_MULT = 0.33
NDefines.NCharacter.INFANT_DEATH_CHANCE = 0.03
NDefines.NCharacter.TREASURY_CHANCE_TO_DISAPPEAR_STANDARD = 0    -- prior EMF v8.02: 0.05

-- Title
NDefines.NTitle.BARON_GRANT_TO_CHURCH_PIETY = 75
NDefines.NTitle.COUNT_GRANT_TO_CHURCH_PIETY = 150
NDefines.NTitle.COUNT_TITLE_PRESTIGE = 0.05
NDefines.NTitle.DUKE_TITLE_PRESTIGE = 0.2
NDefines.NTitle.KING_TITLE_PRESTIGE = 0.4
NDefines.NTitle.EMPEROR_TITLE_PRESTIGE = 0.8
NDefines.NTitle.DUKE_CREATION_PRESTIGE = 125
NDefines.NTitle.KING_CREATION_PRESTIGE = 250
NDefines.NTitle.EMPEROR_CREATION_PRESTIGE = 500
NDefines.NTitle.DUKE_DESTRUCTION_PRESTIGE_COST = 125
NDefines.NTitle.KING_DESTRUCTION_PRESTIGE_COST = 250
NDefines.NTitle.EMPEROR_DESTRUCTION_PRESTIGE_COST = 500
NDefines.NTitle.NORMAL_LAW_CHANGE_COUNCIL_MONTHS = 48 -- from 60
NDefines.NTitle.NORMAL_LAW_CHANGE_ABSOLUTISM_MONTHS = 120
NDefines.NTitle.MAX_CROWN_LAW_CHANGES = 64  -- intention is "unlimited" due to the way EMF CA sub-laws are designed & existence of its soft-coded cooldowns
NDefines.NTitle.CROWN_LAW_CHANGE_TIMER = 0  -- EMF crown laws assume that you will be able to change a CA sub-law after raising CA with same ruler
NDefines.NTitle.EMPIRE_DE_JURE_ASSIMILATION_YEARS = 50
NDefines.NTitle.GAME_RULES_DEJURE_LONG = 200
NDefines.NTitle.GAME_RULES_DEJURE_LONG_EMPIRE = 200
NDefines.NTitle.GAME_RULES_DEJURE_SHORT = 50
NDefines.NTitle.GAME_RULES_DEJURE_SHORT_EMPIRE = 50
NDefines.NTitle.GAME_RULES_DEJURE_SHORTEST = 25
NDefines.NTitle.GAME_RULES_DEJURE_SHORTEST_EMPIRE = 25
NDefines.NTitle.REQ_KINGDOMS_FOR_EMPIRE_CREATION = 3 -- from 2
NDefines.NTitle.ENFORCE_ONE_OF_EACH_HOLDING = 0 -- not needed, esp. on SWMH w/ its more realistic, irregular provinces
NDefines.NTitle.MAX_REPUBLIC_COUNTIES_IN_REALM = 0.2
NDefines.NTitle.MAX_THEOCRACY_COUNTIES_IN_REALM = 0.2
NDefines.NTitle.EMPIRE_DEJURE_COUNTY_LIMIT_TO_CREATE = 0.667
NDefines.NTitle.EMPIRE_DEJURE_COUNTY_LIMIT_TO_USURP = 0.667
NDefines.NTitle.CUSTOM_TITLE_COLOR_OFFSET = 0.25

-- Religion

NDefines.NReligion.CREATE_ANTIPOPE_PRESTIGE_COST = 1500           -- prior to EMF v8.02: 500
NDefines.NReligion.INVASION_MIN_AUTHORITY = 0.4
NDefines.NReligion.REFORM_RELIGION_MIN_AUTHORITY = 0.3
NDefines.NReligion.REFORM_RELIGION_MIN_HOLY_SITES = 4
NDefines.NReligion.AUTHORITY_FROM_HOLY_SITE = 0.05
NDefines.NReligion.AUTHORITY_FROM_ANTIPOPE = -0.1                 -- prior to EMF v8.02: -0.3
NDefines.NReligion.AUTHORITY_FROM_RELHEAD_PIETY = 0.001           -- prior to EMF v8.02: 0
NDefines.NReligion.AUTHORITY_FROM_RELHEAD_DIPLOMACY = 0.02
NDefines.NReligion.AUTHORITY_FROM_RELHEAD_HOLY_SITE = 0.05        -- prior to EMF v8.02: 0, now back to vanilla
NDefines.NReligion.AUTHORITY_FROM_ORG_RELIGION = 0.3
NDefines.NReligion.DIVINE_BLOOD_FERTILITY_MULT = 1.0
NDefines.NReligion.ELECTOR_TITLE_CULTURE_GROUP_FACTOR = 25        -- prior to EMF v8.02: 50
NDefines.NReligion.ELECTOR_TITLE_CULTURE_FACTOR = 50              -- prior to EMF v8.02: 200
NDefines.NReligion.ELECTOR_FAMOUS_DYNASTY_FACTOR = 0.005
NDefines.NReligion.HERESY_TAKEOVER_PROVINCES = 5

-- Economy
NDefines.NEconomy.BISHOP_TAX_TO_POPE_FACTOR = 0.25
NDefines.NEconomy.BISHOP_TAX_TO_ANTI_POPE_FACTOR = 0.025          -- prior to EMF v8.02: 0.05
NDefines.NEconomy.TRADE_POST_COST_INC_DIST = 0.0045
NDefines.NEconomy.PATRICIAN_CITY_TAX_MULT = 0.25
NDefines.NEconomy.OVER_MAX_DEMESNE_TAX_PENALTY = 0.05
NDefines.NEconomy.LOOTER_ARMY_MAINT_MULT = 0.1

-- Nomad
NDefines.NNomad.MAX_POPULATION_EMPTY_HOLDING_MULTIPLIER = 1500
NDefines.NNomad.STARTING_HORDE_MAX_FRACTION = 1

-- Military
NDefines.NMilitary.NUMBER_OF_TROOPS_PER_GALLEY = 200
NDefines.NMilitary.LEVY_MAINTENANCE_FACTOR = 2.4
NDefines.NMilitary.HOLDING_LEVY_SIZE_OWNER_MARTIAL_BASE = 0.75
NDefines.NMilitary.HOLDING_LEVY_SIZE_OWNER_MARTIAL_MULT = 0.025
NDefines.NMilitary.BATTLE_WARSCORE_DEFENDER_MULTIPLIER = 1.6
NDefines.NMilitary.MIN_LEVY_RAISE_OPINION_THRESHOLD = -50
NDefines.NMilitary.ATTACKER_SIEGE_DAMAGE = 0
NDefines.NMilitary.DEFENDER_SIEGE_DAMAGE = 0
NDefines.NMilitary.NUM_DAYS_BETWEEN_SIEGE_MORALE_LOSS = 10
NDefines.NMilitary.BATTLE_TECH_MULTIPLIER = 0.25
NDefines.NMilitary.REINFORCE_RATE = 0.03
NDefines.NMilitary.ARMY_LOAD_MOVE_COST = 40.0
NDefines.NMilitary.CAPTURED_HEIR_WAR_SCORE = 30.0
NDefines.NMilitary.RETINUE_FROM_REALMSIZE = 1.5
NDefines.NMilitary.RETINUE_INCREASE_PER_TECH = 0.5
NDefines.NMilitary.RETINUE_HIRE_COST_MULTIPLIER = 0.2
NDefines.NMilitary.MAX_COMMANDERS_DUKE = 5                   -- from 4
NDefines.NMilitary.MAX_COMMANDERS_KING = 7                   -- from 6
NDefines.NMilitary.MAX_COMMANDERS_EMPEROR = 9                -- from 8
NDefines.NMilitary.LIEGE_LEVY_REINF_RATE = 0.03
NDefines.NMilitary.LIEGE_LEVY_COST_MULTIPLIER = 0.5
NDefines.NMilitary.LIGHT_INFANTRY_MORALE = 3
NDefines.NMilitary.LIGHT_INFANTRY_MAINTENANCE = 1
NDefines.NMilitary.LIGHT_INFANTRY_PHASE_SKIRMISH_ATTACK = 1
NDefines.NMilitary.LIGHT_INFANTRY_PHASE_MELEE_ATTACK = 3
NDefines.NMilitary.LIGHT_INFANTRY_PHASE_PURSUE_ATTACK = 3
NDefines.NMilitary.LIGHT_INFANTRY_PHASE_SKIRMISH_DEFENSE = 3
NDefines.NMilitary.LIGHT_INFANTRY_PHASE_MELEE_DEFENSE = 3
NDefines.NMilitary.LIGHT_INFANTRY_PHASE_PURSUE_DEFENSE = 2
NDefines.NMilitary.HEAVY_INFANTRY_MORALE = 5
NDefines.NMilitary.HEAVY_INFANTRY_MAINTENANCE = 2
NDefines.NMilitary.HEAVY_INFANTRY_PHASE_SKIRMISH_ATTACK = 0.25
NDefines.NMilitary.HEAVY_INFANTRY_PHASE_MELEE_ATTACK = 6
NDefines.NMilitary.HEAVY_INFANTRY_PHASE_PURSUE_ATTACK = 2
NDefines.NMilitary.HEAVY_INFANTRY_PHASE_SKIRMISH_DEFENSE = 5
NDefines.NMilitary.HEAVY_INFANTRY_PHASE_MELEE_DEFENSE = 4
NDefines.NMilitary.HEAVY_INFANTRY_PHASE_PURSUE_DEFENSE = 2
NDefines.NMilitary.PIKEMEN_MORALE = 6
NDefines.NMilitary.PIKEMEN_MAINTENANCE = 2
NDefines.NMilitary.PIKEMEN_PHASE_SKIRMISH_ATTACK = 0.1
NDefines.NMilitary.PIKEMEN_PHASE_MELEE_ATTACK = 5
NDefines.NMilitary.PIKEMEN_PHASE_PURSUE_ATTACK = 0.2
NDefines.NMilitary.PIKEMEN_PHASE_SKIRMISH_DEFENSE = 4
NDefines.NMilitary.PIKEMEN_PHASE_MELEE_DEFENSE = 8
NDefines.NMilitary.PIKEMEN_PHASE_PURSUE_DEFENSE = 1.5
NDefines.NMilitary.LIGHT_CAVALRY_MORALE = 4
NDefines.NMilitary.LIGHT_CAVALRY_MAINTENANCE = 2
NDefines.NMilitary.LIGHT_CAVALRY_PHASE_SKIRMISH_ATTACK = 1.5
NDefines.NMilitary.LIGHT_CAVALRY_PHASE_MELEE_ATTACK = 4.5
NDefines.NMilitary.LIGHT_CAVALRY_PHASE_PURSUE_ATTACK = 15
NDefines.NMilitary.LIGHT_CAVALRY_PHASE_SKIRMISH_DEFENSE = 5
NDefines.NMilitary.LIGHT_CAVALRY_PHASE_MELEE_DEFENSE = 3
NDefines.NMilitary.LIGHT_CAVALRY_PHASE_PURSUE_DEFENSE = 8
NDefines.NMilitary.KNIGHTS_MORALE = 10
NDefines.NMilitary.KNIGHTS_MAINTENANCE = 4
NDefines.NMilitary.KNIGHTS_PHASE_SKIRMISH_ATTACK = 0.5
NDefines.NMilitary.KNIGHTS_PHASE_MELEE_ATTACK = 10
NDefines.NMilitary.KNIGHTS_PHASE_PURSUE_ATTACK = 8
NDefines.NMilitary.KNIGHTS_PHASE_SKIRMISH_DEFENSE = 8
NDefines.NMilitary.KNIGHTS_PHASE_MELEE_DEFENSE = 8
NDefines.NMilitary.KNIGHTS_PHASE_PURSUE_DEFENSE = 4
NDefines.NMilitary.ARCHERS_MORALE = 1
NDefines.NMilitary.ARCHERS_MAINTENANCE = 1.5
NDefines.NMilitary.ARCHERS_PHASE_SKIRMISH_ATTACK = 5
NDefines.NMilitary.ARCHERS_PHASE_MELEE_ATTACK = 1
NDefines.NMilitary.ARCHERS_PHASE_PURSUE_ATTACK = 2
NDefines.NMilitary.ARCHERS_PHASE_SKIRMISH_DEFENSE = 3
NDefines.NMilitary.ARCHERS_PHASE_MELEE_DEFENSE = 2
NDefines.NMilitary.ARCHERS_PHASE_PURSUE_DEFENSE = 2
NDefines.NMilitary.SPECIAL_TROOPS_MORALE = 5
NDefines.NMilitary.SPECIAL_TROOPS_MAINTENANCE = 2
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_SKIRMISH_ATTACK = 4
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_MELEE_ATTACK = 3
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_PURSUE_ATTACK = 7
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_SKIRMISH_DEFENSE = 4
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_MELEE_DEFENSE = 4
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_PURSUE_DEFENSE = 7
NDefines.NMilitary.SPECIAL_TROOPS_GRAPHICAL_FACTOR = 1.5
NDefines.NMilitary.CAPITAL_DUCHY_LIEGE_LEVY_MULT = 0.75 -- same as vanilla, just here for completeness
NDefines.NMilitary.CAPITAL_KINGDOM_LIEGE_LEVY_MULT = 0.5 -- same as vanilla, just here for completeness
NDefines.NMilitary.CAPITAL_EMPIRE_LIEGE_LEVY_MULT = 0.25 -- reduced to be same as "outside capital empire," since most places are "outside" a de jure empire in the default EMF setup (or, rather, it's e_null, which complicates things if they're not the same)
NDefines.NMilitary.OUTSIDE_LIEGE_LEVY_MULT = 0.25 -- same as vanilla, just here for completeness
NDefines.NMilitary.MONTHS_OF_UNDECIDED_WAR = 0
NDefines.NMilitary.SHATTERED_RETREAT_MORALE_MULTIPLIER = 1.0
NDefines.NMilitary.SHATTERED_RETREAT_PREFERRED_PROVINCES = 4
NDefines.NMilitary.SHATTERED_RETREAT_MAX_PROVINCES = 6
NDefines.NMilitary.MAX_WARSCORE_FROM_BATTLE_DEFENDERS = 200   -- from 100

-- Technology
NDefines.NTechnology.POINTS_PER_ATTRIBUTE = 0.02
NDefines.NTechnology.BASE_NEIGHBOUR_SPREAD_BONUS = 0.075
NDefines.NTechnology.BASE_DEMESNE_SPREAD_BONUS = 0.1
NDefines.NTechnology.MAX_DEMESNE_BONUS = 0.5
NDefines.NTechnology.TRADEPOST_SPREAD_BONUS = 0.01

-- Graphics
NDefines.NGraphics.CITY_SPRAWL_AMOUNT = 0.75

-- Engine
NDefines.NEngine.EVENT_PROCESS_OFFSET = 30
NDefines.NEngine.COURTIER_EVENT_PROCESS_OFFSET = 60

-- AI
NDefines.NAI.AI_EMPEROR_CREATES_KINGDOMS = 1     -- only now a good idea due to Imperial Kingdom Creation law
NDefines.NAI.RAID_AGGRESSION = 24
NDefines.NAI.TRIBAL_VASSAL_EXTRA_CALL_CHANCE = 30
-- NDefines.NAI.COALITION_DISTANCE_MULTIPLIER = -1.25

-- RulerDesigner defines are in emf_ruler_designer_defines.lua; if you blank that file, the designer will revert to
-- vanilla settings and no longer be "unlocked" (free everything, you be the judge of what's reasonable).
