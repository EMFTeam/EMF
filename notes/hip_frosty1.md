# HIP Frosty1

## Scope

### Definite Projects

These are the big ticket items which shall be the root of most further work and testing before Frosty1 is released.

- Addition of South India & miscellaneous provinces to SWMH map
- SWMH scrollable timeline extension to 993
- SWMH non-scrollable Iron Century start date (936)
- Rebalancing tribes, nomads, and feudals in terms of historical outcome promotion
- Redesign of feudal liege levies
- Nomad overhaul for sensibility and gameplay
- Artifact overhaul
- `old_hungarian` / `hungarian` (Magyar / Moger) cultural split

### Wishlist Projects

- Model Sweyn Forkbeard's invasion of England (simple version, possibly AI-only to large degree)
- 936-related historical outcome promotion
  - Requires investigation

## Action Items

### LTM

- Terrain map update for South India

### CPRplus

- Graphical culture assignments or modified portraits for `old_hungarian` vs. `hungarian` culture split
  - `old_hungarian` (Moger) reflects the pre-Christianized Magyars on the Steppe
  - Any fashion/headgear/etc. changes to reflect? How about actual face/hairstyle/eye-color/hair-color stuff?
- Same for `kavar` culture addition

## SWMH

- Setup new branch structure while merging the current `beta` into our mainline development
- Check 936 start date error.log & then whittle down inevitable issues
- Survey map (in 936, in 993-1018) for things that don't seem right
  - Province positions for the new provinces
  - Province religions & cultures
  - Title vassalage and tributary relationships (e.g., oddly independent counties and such)
  - Terrain & terrain textures in India, etc.

### Done

- Addition of South India & other misc. new provinces
- Cleared 993 start for stabilization
- Cleared 936 start for stabilization
- `old_hungarian` & kavars

## EMF

### Mandatory

- (EMF+SWMH) Check 936 start date error.log & then whittle down inevitable issues
- (EMF+SWMH) Review LT_936 (vanilla Iron Century) content & adapt to SWMH
- Finish decision to show HRE elector titles & their holders
- Ensure that all `ai_will_do` and other such triggers for discouraging the prior `hungarian` culture from getting distracted from their mission to cross the Carpathians, conquer Pannonia, and form Hungary is still WAD in the face of the addition of `old_hungarian`
- Re-run `antinomad` code generator before release
- Sweep for `TMP-SAVE-COMPAT` and `TODO` and `FIXME` (but especially the first) comments in codebase
  - Any items discovered which would be best implemented upon the first release of the Frosty series for forward save-compatibility reasons should be addressed
- Continue rebalancing feudals vs. tribes vs. nomads (observes, first-hand experience)

### Wishlist

- Player decision to form a cadet branch of their dynasty (with their character as the new dynasty head)
- Update HRE formation decision icons with new icons from Arko

### Done

- Adapt historical Seljuk invasion to 993 starts
- Initial liege levy redesign
- Artifact overhaul
- Nomadic overhaul

