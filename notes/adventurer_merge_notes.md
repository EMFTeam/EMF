changes made to the `adventurer` branch before merging into `alpha`:

- fixed a mismatch between how long the `do_not_disturb` timer was set in `emf_travel_to_ruler_effect` and the actual scheduled event delay
  - the longer trips did not set the timer long enough, so the adventurer would end-up being detected as "idle," sent somewhere else, and then later also appear where they were originally scheduled to travel.
- removed a stray `is_ruler = no` from the limit of an `any_vassal` in `emf_adventurer_recruits_demesne` (can't happen otherwise)
- `emf_adventurer_recruits_demesne` was still recruiting from `any_realm_province`, so I converted this to only recruit from demesne provinces
  - I also converted the `county = { is_occupied = no }` to a check on the province's `capital_holding = { is_occupied = no }`, as I've run into issues recently with using `is_occupied` on county titles rather than barony titles for non-nomadic provinces-- it won't register as occupied despite being, well, occupied. [needs confirmation for current version, but heck, why not.]
- added adventurer supporter's / backer's clickable portrait to target notification event option tooltip
- removed `capable_only = yes` pre-trigger from adventure invalidation event (would skip invalidation due to becoming incapable)
- fixed a problem with finding an optimal attack court which would defeat the point of distance preference
- split main army spawn into 6 subunits instead of 3
- removed `merge = yes` from all claimant adventurer spawns
- added `only_independent = yes` pre-trigger to adventurer maintenance events [tested; only_playable & only_rulers also work]
- removed [my] unnecessary custom_tooltip to get `FROM` in the target notification event option tooltip portrait in favor of showing the opinion effect
- added a couple more random soldier courtiers for claimant adventurers, as the AI now attempts to have stacks ~10K max. in size (and ideally would have 3 flank commanders of some kind available for each stack)
