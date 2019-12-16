-- Diplomacy
NDefines.NDiplomacy.GAVELKIND_MAX_SIZE_BONUS = 0.50            -- from 0.30, vanilla=0.30
NDefines.NDiplomacy.VASSAL_LIMIT_LEVY_MULTIPLIER = 0
NDefines.NDiplomacy.MAX_DUCHIES_LEGALLY_HELD = 3               -- from 2, vanilla=2
NDefines.NDiplomacy.MAX_ELECTOR_TITLES_LEGALLY_HELD = 2        -- from 1, vanilla=1
NDefines.NDiplomacy.INTER_MUSLIM_WAR_MONTHLY_PIETY_COST = 1
NDefines.NDiplomacy.MUSLIM_TEMPLE_HOLDING_MONTHLY_PIETY = 0.5
NDefines.NDiplomacy.PREP_INV_REQ_PRESTIGE = 2000               -- prior to v10.3: 750; vanilla: 750
NDefines.NDiplomacy.BASE_REVOLT_CHANCE_MOD = 175
NDefines.NDiplomacy.TOG_REVOLT_CHANCE_MOD = 70
NDefines.NDiplomacy.DUKE_POWERFUL_VASSAL_COUNT = 3
NDefines.NDiplomacy.KING_POWERFUL_VASSAL_COUNT = 4
NDefines.NDiplomacy.EMPEROR_POWERFUL_VASSAL_COUNT = 5
NDefines.NDiplomacy.IMPRISON_CHARACTER_INTERACTION_PIETY = 0
NDefines.NDiplomacy.EXECUTE_IMPRISONED_INTERACTION_PIETY = 10
NDefines.NDiplomacy.DEMAND_RELIGIOUS_CONVERSION_INTERACTION_PIETY = 25
NDefines.NDiplomacy.DEMAND_RELIGIOUS_CONVERSION_INTERACTION_PRESTIGE = 50
NDefines.NDiplomacy.DEMAND_RELIGIOUS_CONVERSION_INTERACTION_THRESHOLD_FOR_YES = 35
NDefines.NDiplomacy.PREPARE_INVASION_INTERACTION_MONEY = 100                       -- prior to v10.3: 0; vanilla: 0
NDefines.NDiplomacy.PREPARE_INVASION_INTERACTION_PIETY = 500                       -- prior to v10.3: 0; vanilla: 0
NDefines.NDiplomacy.PREPARE_INVASION_INTERACTION_PRESTIGE = 1500                   -- prior to v10.3: 500; vanilla: 500
NDefines.NDiplomacy.CHANGE_CRUSADE_TARGET_INTERACTION_PIETY = 400                  -- EMF v10.0 (from 250 in vanilla)
NDefines.NDiplomacy.CHANGE_CRUSADE_TARGET_INTERACTION_PRESTIGE = 400               -- EMF v10.0 (from 0 in vanilla)
NDefines.NDiplomacy.INVITE_TO_COURT_INTERACTION_MONEY = 10
NDefines.NDiplomacy.INVITE_TO_COURT_INTERACTION_PRESTIGE = 30
NDefines.NDiplomacy.ASK_FOR_EXCOMMUNICATION_INTERACTION_PIETY = 150
NDefines.NDiplomacy.ASK_FOR_CLAIM_INTERACTION_PRESTIGE = 150
NDefines.NDiplomacy.BANISH_TAKE_WEALTH_PERCENTAGE_COURTIER = 0.2
NDefines.NDiplomacy.DEFENSIVE_PACT_THREAT_LIMIT = 0.15
NDefines.NDiplomacy.DEFENSIVE_PACT_MAX_RANGE = 300

-- Council
NDefines.NCouncil.ENFORCE_PEACE_START_DELAY = 6
NDefines.NCouncil.LAW_VOTE_CHANGE_TIME_LIMIT = 2
NDefines.NCouncil.REGENCY_VOTING = "laws enforce_peace declare_war_interaction prepare_invasion_interaction ask_to_join_war_interaction form_non_aggression_pact_interaction break_non_aggression_pact form_alliance_interaction dissolve_alliance_interaction release_tributary ask_for_vassalization_interaction release_vassal_interaction offer_vassalization_interaction revoke_title_interaction grant_landed_title_interaction retract_vassal_interaction transfer_vassal_interaction lollard_revoke_temple absorb_clan_interaction split_clan_interaction imprison_character_interaction exile_imprisoned_interaction execute_imprisoned_interaction ransom_character_interaction release_from_prison_interaction recruit_prisoner emf_prisoner_house_arrest emf_prisoner_oubliette emf_prisoner_dungeon emf_prisoner_castration emf_prisoner_blinding emf_prisoner_zun_judgement kharijite_public_execution prisoner_brazen_bull prisoner_macabre_banquet prisoner_dragon_burning" -- Added various interactions that now support council voting strategies
NDefines.NCouncil.NO_VOTING_PIETY_OVERRIDE = 0
NDefines.NCouncil.NO_VOTING_PRESTIGE_OVERRIDE = 0

-- Infamy
NDefines.NInfamy.REALM_SIZE_GROWTH_MODIFIER = 0.005 -- shrunk from v8.06
NDefines.NInfamy.REALM_SIZE_SHRINK_MODIFIER = 0.005 -- shrunk from v8.06
NDefines.NInfamy.WAR_REALM_CHANGE_VALUE = 0.5
NDefines.NInfamy.INDEPENDENCE_REALM_CHANGE_VALUE = 0.1
NDefines.NInfamy.INHERITANCE_CHANGE_VALUE = 0.05
NDefines.NInfamy.VASSAL_CHANGE_VALUE = 0
NDefines.NInfamy.MAX_INFAMY_PER_WAR_PROVINCE = 4 -- shrunk from v8.06 by 1
NDefines.NInfamy.MIN_INFAMY_PER_WAR_PROVINCE = 0

-- Character
NDefines.NCharacter.CHANGE_AMBITION_YEARS = 1
NDefines.NCharacter.CHANGE_FOCUS_YEARS = 3
NDefines.NCharacter.PRESTIGE_FROM_DYNASTY_ON_BIRTH_DIV = 20        -- < v10.6: 15; vanilla: 5; [Newly born characters get the dynasty prestige of their mother and father divided by this as their starting prestige]
NDefines.NCharacter.PRESTIGE_FROM_DYNASTY_ON_MARRIAGE_DIV = 20     -- < v10.6: 15; vanilla: 10; [Characters get the dynasty prestige of the spouse divided by this on marriage]
NDefines.NCharacter.ASSIGN_ACTION_DAYS = 56
NDefines.NCharacter.RAISED_TROOPS_VASSAL_OPINION_DAYS = 28
NDefines.NCharacter.MUSLIM_NUM_WIVES_MONTHLY_PRESTIGE_PENALTY = 0  -- < v10.6: 1.0 (vanilla); [The prestige effect from each lacking expected wife]
NDefines.NCharacter.PAGAN_NUM_CONSORTS_MONTHLY_PRESTIGE = 0        -- < v10.6; 0.2 (vanilla); [The monthly prestige effect for pagans for each young Concubine]
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
-- OUT-COMMENT: Nonzero INFANT_DEATH_CHANCE causes nondeterministic crashes on patch 3.3.0 (64-bit):
-- NDefines.NCharacter.INFANT_DEATH_CHANCE = 0.07
NDefines.NCharacter.TRIBAL_EMPTY_HOLDING_LEVY_MULTIPLIER = 0.25       -- vanilla: 0.5, < v10.6: 0.5
NDefines.NCharacter.TRIBAL_EMPTY_HOLDING_GARRISON_MULTIPLIER = 0.15   -- vanilla: 0.5, < v10.6: 0.5
NDefines.NCharacter.ADULT_DIPLOMACY_OPINION_MUL_FACTOR = 0.75         -- vanilla: 1.5, < v10.6: 1.5

-- Title
NDefines.NTitle.COUNT_TITLE_PRESTIGE = 0.05
NDefines.NTitle.DUKE_TITLE_PRESTIGE = 0.2
NDefines.NTitle.KING_TITLE_PRESTIGE = 0.4
NDefines.NTitle.EMPEROR_TITLE_PRESTIGE = 0.8
NDefines.NTitle.BARON_LANDLESS_SON_PRESTIGE = 0
NDefines.NTitle.BARON_GRANT_TO_CHURCH_PIETY = 75
NDefines.NTitle.COUNT_GRANT_TO_CHURCH_PIETY = 150
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
NDefines.NTitle.GAME_RULES_DEJURE_SHORT = 40
NDefines.NTitle.GAME_RULES_DEJURE_SHORT_EMPIRE = 40
NDefines.NTitle.GAME_RULES_DEJURE_SHORTEST = 20
NDefines.NTitle.GAME_RULES_DEJURE_SHORTEST_EMPIRE = 20
NDefines.NTitle.REQ_KINGDOMS_FOR_EMPIRE_CREATION = 3
NDefines.NTitle.ENFORCE_ONE_OF_EACH_HOLDING = 0
NDefines.NTitle.MAX_REPUBLIC_COUNTIES_IN_REALM = 0.2
NDefines.NTitle.MAX_THEOCRACY_COUNTIES_IN_REALM = 0.2
NDefines.NTitle.EMPIRE_DEJURE_COUNTY_LIMIT_TO_CREATE = 0.667
NDefines.NTitle.EMPIRE_DEJURE_COUNTY_LIMIT_TO_USURP = 0.667
NDefines.NTitle.CUSTOM_TITLE_COLOR_OFFSET = 0.2

-- Religion
NDefines.NReligion.CREATE_ANTIPOPE_PRESTIGE_COST = 1500           -- prior to EMF v8.02: 500
NDefines.NReligion.INVASION_MIN_AUTHORITY = 0.4
NDefines.NReligion.REFORM_RELIGION_MIN_AUTHORITY = 0.4            -- < v10.6: 0.45; < EMF v10.3: 0.3; vanilla: 0.5
NDefines.NReligion.REFORM_RELIGION_MIN_HOLY_SITES = 4             -- vanilla: 3
NDefines.NReligion.REFORM_RELIGION_PIETY_COST = 2500              -- < v10.6: 1500; vanilla: 750
NDefines.NReligion.AUTHORITY_FROM_HOLY_SITE = 0.05
NDefines.NReligion.AUTHORITY_FROM_ANTIPOPE = -0.1                 -- prior to EMF v8.02: -0.3
NDefines.NReligion.AUTHORITY_FROM_RELHEAD_PIETY = 0.002           -- prior to EMF v9.06: 0.001; prior to EMF v8.02: 0
NDefines.NReligion.AUTHORITY_FROM_RELHEAD_DIPLOMACY = 0.03        -- prior to EMF v9.06: 0.02
NDefines.NReligion.AUTHORITY_FROM_ORG_RELIGION = 0.3
NDefines.NReligion.DIVINE_BLOOD_FERTILITY_MULT = 0.667            -- < v10.6: 1.0; vanilla: 0.25 [Fertility multiplier in a religious close kin marriage]
NDefines.NReligion.ELECTOR_TITLE_CULTURE_GROUP_FACTOR = 50        -- doubled to vanilla from EMF v8.06
NDefines.NReligion.ELECTOR_TITLE_CULTURE_FACTOR = 50              -- prior to EMF v8.02: 200
NDefines.NReligion.ELECTOR_FAMOUS_DYNASTY_FACTOR = 0.008          -- prior to EMF v9.06: 0.005
NDefines.NReligion.AUTHORITY_FROM_PIETY_CAP = 0.1                 -- < EMF v10.6: 0.25 (vanilla)

-- Economy
NDefines.NEconomy.BISHOP_TAX_TO_POPE_FACTOR = 0.4                 -- prior to EMF v9.06: 0.25
NDefines.NEconomy.BISHOP_TAX_TO_ANTI_POPE_FACTOR = 0.1            -- prior to EMF v9.06: 0.025; prior to EMF v8.02: 0.05
NDefines.NEconomy.TRADE_POST_COST_INC_DIST = 0.0045
NDefines.NEconomy.TRADE_POST_OPINION_EFFECT = 0.5
NDefines.NEconomy.TRADETECH_LEVEL_FOR_BASE_TPS = 8
NDefines.NEconomy.MAX_TRADE_POSTS_BASE = 2							-- Calibrated with TRADETECH_LEVEL_FOR_BASE_TPS
NDefines.NEconomy.MIN_TRADE_POSTS = 7								-- Calibrated with TRADETECH_LEVEL_FOR_BASE_TPS
NDefines.NEconomy.PATRICIAN_FAMILY_SHARES_HEAD = 80
NDefines.NEconomy.PATRICIAN_FAMILY_SHARES_REST = 2
NDefines.NEconomy.POPULATION_LOOT_DEATH_MULTIPLIER = 0.25         -- < v10.6: 0.1 (vanilla); [How much population die at each loot tick]
NDefines.NEconomy.LOOT_PRESTIGE_MULT = 0.5                        -- < v10.6: 1.0 (vanilla); [Whenever you gain loot you also get prestige related to the loot]
NDefines.NEconomy.TRADE_ROUTE_SIEGE_MULTIPLIER = 0.75			  -- prior to EMF v9.06: 0.8; vanilla: 0.9 [also from v8.06]
NDefines.NEconomy.TRADE_ROUTE_OCCUPATION_MULTIPLIER = 0.5         -- prior to EMF v9.06: 0.6; vanilla: 0.75 [also from v8.06]
NDefines.NEconomy.PATRICIAN_INHERITANCE_FROM_RELATIVE_MULT = 1
NDefines.NEconomy.PATRICIAN_GOLD_TO_MONTHLY_PRESTIGE = 0
-- Patrician Elective Defines
-- Respect formula: [Campaign Funds] * PATRICIAN_CAMPAIGN_FUND_FACTOR + [Prestige] * PATRICIAN_PRESTIGE_RESPECT_FACTOR + [Age in years]^2 * PATRICIAN_AGE_RESPECT_FACTOR + [Random number between 0 and DOGE_SUCC_RANDOM_FACTOR]
NDefines.NEconomy.PATRICIAN_CAMPAIGN_FUND_FACTOR = 1
NDefines.NEconomy.PATRICIAN_PRESTIGE_RESPECT_FACTOR = 10
NDefines.NEconomy.PATRICIAN_AGE_RESPECT_FACTOR = 0
NDefines.NEconomy.DOGE_SUCC_RANDOM_FACTOR = 0

-- Nomad
NDefines.NNomad.MAX_POPULATION_EMPTY_HOLDING_MULTIPLIER = 500 -- < v10.6: 1250; vanilla: 1000; now compensated for with terrain-based province modifiers; [Base population per empty holding for grazing]
NDefines.NNomad.MANPOWER_INCREASE_MULTIPLIER = 0.075        -- < v10.6: 0.1 (vanilla); [The rate current manpower grows or declines to max manpower]
NDefines.NNomad.POPULATION_TAX_MULTIPLIER = 0.0005          -- < v10.6: 0.0005 (vanilla); [Monthly tax income determined by the current population]
NDefines.NNomad.STARTING_HORDE_MAX_FRACTION = 1

-- Military
NDefines.NMilitary.LEVY_MAINTENANCE_FACTOR = 2.3               -- prior to EMF v10.0: 2.7; prior to EMF v9.06: 2.4; prior to EMF v9.01: 2.7
NDefines.NMilitary.BATTLE_WARSCORE_DEFENDER_MULTIPLIER = 1.6
NDefines.NMilitary.MIN_LEVY_RAISE_OPINION_THRESHOLD = -75      -- prior to EMF v10.6: 0 (vanilla); [Below this opinion value you'll get the least amount of troops possible]
NDefines.NMilitary.MAX_LEVY_RAISE_OPINION_THRESHOLD = 75       -- prior to EMF v10.6: 100 (vanilla); [Above this opinion value you'll get the max amount of troops possible]
NDefines.NMilitary.REINFORCE_RATE = 0.03                       -- vanilla: 0.05
NDefines.NMilitary.LEVY_RAISED_REINFORCE_RATE_MULTIPLIER = 0.2 -- vanilla / v8.06 was 0.5
NDefines.NMilitary.NAVAL_ATTRITION = 0.035                     -- prior to EMF v9.06: 5%; prior to EMF v8.07: 0% (vanilla)
NDefines.NMilitary.ARMY_LOAD_MOVE_COST = 30.0                  -- changed by -10 cost from v8.06 (-25% EMF / +50% vanilla instead of +100% vanilla)
NDefines.NMilitary.CAPTURED_HEIR_WAR_SCORE = 20.0              -- changed by -10 WS from v8.06 (vanilla = 50 WS)
NDefines.NMilitary.RETINUE_FROM_REALMSIZE = 1.5
NDefines.NMilitary.RETINUE_INCREASE_PER_TECH = 0.5
NDefines.NMilitary.RETINUE_HIRE_COST_MULTIPLIER = 0.35         -- prior to EMF v10.6: 0.25; prior to EMF v9.06: 0.2
NDefines.NMilitary.MAX_COMMANDERS_BARON = 2                    -- EMF v8.07: barons should not be deprived of commanders (rest of commander limits reverted to vanilla, a decrease by 1 for each tier)
NDefines.NMilitary.LIEGE_LEVY_REINF_RATE = 0.03                -- changed by -0.02 from EMF v8.06 (-67%), which is now a fifth of vanilla's rate; changed again in EMF v10.6 by +0.03 to 0.04 (3/5 vanilla and same as demesne levy reinforcement)
NDefines.NMilitary.LIEGE_LEVY_SIZE_MULTIPLIER = 0.8            -- < v10.6: 0.5; vanilla: 0.5 [The Size of the liege levy will be the total troops in the vassal subrealm * this]
NDefines.NMilitary.LIEGE_LEVY_COST_MULTIPLIER = 0.25           -- as of EMF v10.0, vassals pay 25% of the upkeep on their liege levy contribution
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
NDefines.NMilitary.PIKEMEN_PHASE_SKIRMISH_ATTACK = 0.25
NDefines.NMilitary.PIKEMEN_PHASE_MELEE_ATTACK = 5
NDefines.NMilitary.PIKEMEN_PHASE_PURSUE_ATTACK = 2
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
NDefines.NMilitary.ARCHERS_MORALE = 3
NDefines.NMilitary.ARCHERS_MAINTENANCE = 1.5
NDefines.NMilitary.ARCHERS_PHASE_SKIRMISH_ATTACK = 5
NDefines.NMilitary.ARCHERS_PHASE_MELEE_ATTACK = 1
NDefines.NMilitary.ARCHERS_PHASE_PURSUE_ATTACK = 2
NDefines.NMilitary.ARCHERS_PHASE_SKIRMISH_DEFENSE = 3
NDefines.NMilitary.ARCHERS_PHASE_MELEE_DEFENSE = 3
NDefines.NMilitary.ARCHERS_PHASE_PURSUE_DEFENSE = 1.5
NDefines.NMilitary.SPECIAL_TROOPS_MORALE = 5
NDefines.NMilitary.SPECIAL_TROOPS_MAINTENANCE = 2
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_SKIRMISH_ATTACK = 4
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_MELEE_ATTACK = 3
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_PURSUE_ATTACK = 7
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_SKIRMISH_DEFENSE = 4
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_MELEE_DEFENSE = 4
NDefines.NMilitary.SPECIAL_TROOPS_PHASE_PURSUE_DEFENSE = 7
NDefines.NMilitary.SPECIAL_TROOPS_GRAPHICAL_FACTOR = 1.5
NDefines.NMilitary.GALLEYS_MAINTENANCE = 200 -- prior to EMF v10.0: 300 (vanilla)
NDefines.NMilitary.COMMAND_MODIFIER_MARTIAL_MULTIPLIER = 0.02 -- prior to EMF v10.6: 0.03; changed from vanilla by -0.02 (-40%) in EMF v8.07
NDefines.NMilitary.CAPITAL_DUCHY_LIEGE_LEVY_MULT = 0.75 -- same as vanilla, just here for completeness
NDefines.NMilitary.CAPITAL_KINGDOM_LIEGE_LEVY_MULT = 0.5 -- same as vanilla, just here for completeness
NDefines.NMilitary.CAPITAL_EMPIRE_LIEGE_LEVY_MULT = 0.25 -- reduced to be same as "outside capital empire," since most places are "outside" a de jure empire in the default EMF setup (or, rather, it's e_null, which complicates things if they're not the same)
NDefines.NMilitary.OUTSIDE_LIEGE_LEVY_MULT = 0.25 -- same as vanilla, just here for completeness
NDefines.NMilitary.FORAGING_PILLAGE_MODIFIER = 0.25 -- changed from 0.15 in vanilla for EMF v8.07 (troops will take more of a province's loot when out of supply)
NDefines.NMilitary.MONTHS_OF_UNDECIDED_WAR = 0
NDefines.NMilitary.SHATTERED_RETREAT_MORALE_MULTIPLIER = 1.2   -- prior to EMF v10.6: 1.15; prior to EMF v9.06: 1.0
NDefines.NMilitary.SHATTERED_RETREAT_PREFERRED_PROVINCES = 3
NDefines.NMilitary.SHATTERED_RETREAT_MAX_PROVINCES = 4
NDefines.NMilitary.MAX_WARSCORE_FROM_BATTLE_DEFENDERS = 200   -- from 100 in vanilla

-- Technology
NDefines.NTechnology.POINTS_PER_ATTRIBUTE = 0.02
NDefines.NTechnology.BASE_NEIGHBOUR_SPREAD_BONUS = 0.075
NDefines.NTechnology.BASE_DEMESNE_SPREAD_BONUS = 0.1
NDefines.NTechnology.MAX_DEMESNE_BONUS = 0.5
NDefines.NTechnology.TRADEPOST_SPREAD_BONUS = 0.04         -- prior to EMF v9.06: 0.01

-- Graphics
NDefines.NGraphics.CITY_SPRAWL_AMOUNT = 0.5

-- Engine
NDefines.NEngine.EVENT_PROCESS_OFFSET = 30

-- AI
NDefines.NAI.MARRIAGE_AI_PRESTIGE_VALUE = 0.25      -- EMF v10.5: 0.1; vanilla: 0.33 [worst-case, they marry a lowborn, which EMF will raise to the nobility. prestige effects of marriage tend to greatly get in the way of the AI making good matches that further its dynasty.]
NDefines.NAI.AI_EMPEROR_CREATES_KINGDOMS = 1        -- only a good idea after we creating the De Jure Vassal Kingdom Creation laws, else AI spams kingdom titles inappropriately
NDefines.NAI.DESIRED_CONSORTS = 1                   -- as of EMF v8.07, AI will actually try to get a concubine if they lack sons
NDefines.NAI.AI_ASSAULT_RATIO = 15                  -- +50% from vanilla
NDefines.NAI.RAID_MAX_REALM_SIZE = 32               -- prior to EMF v9.06: 24; vanilla is 24
NDefines.NAI.RAID_AGGRESSION = 15                   -- prior to EMF v9.06: 18; prior to EMF v9.01: 12; vanilla is 18; lower means more frequent raiding, higher means less frequent
NDefines.NAI.TRIBAL_VASSAL_EXTRA_CALL_CHANCE = 0	-- Disabled to make tribal consolidation harder (AI already honors alliances fairly often)

NDefines.NAI.NOMAD_MARRIAGE_CLAN_MODIFIER = 40 -- vanilla is 20: "How much nomad AI will prefer inter-realm clan marriages"
NDefines.NAI.NOMAD_MARRIAGE_KHAN_MODIFIER = 15 -- vanila is 5: "How much nomad AI will prefer marriages with their khan"

-- NDefines.NAI.COALITION_DISTANCE_MULTIPLIER = -1.25

-- RulerDesigner defines are in emf_ruler_designer_defines.lua; if you blank that file, the designer will revert to
-- vanilla settings and no longer be "unlocked" (free everything, you be the judge of what's reasonable).
