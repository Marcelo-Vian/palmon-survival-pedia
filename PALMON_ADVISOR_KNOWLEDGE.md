# Palmon Advisor Knowledge Base

Updated: 2026-10-21

This is the source map for the local advisor. It is deliberately a synthesis and a data model, not a copied guide or an external site mirror.

## Evidence and Freshness

- XAPK 0.5.451: local names, line identifiers, visual assets, power tables, skills, equipment and evolution configuration.
- Player screenshots captured on 2026-10-19: account roster, Team 1, mounts, Aurora and boss state. They seed the profile but never supply presentation artwork.
- [LoadoutGG Tier List](https://loadoutgg.com/palmon-survival/tier-list/), checked 2026-10-21: dated Conquest reference for the strategic value of a form.
- [LoadoutGG Stat Rankings](https://loadoutgg.com/palmon-survival/stat-rankings/), checked 2026-10-21: confirms that base, evolved and Mega forms are distinct comparisons and gives the 114-form model.
- [Team-building guide](https://loadoutgg.com/palmon-survival/guides/team-building/): element synergy, front/back composition and target priorities.
- [Progression guide](https://loadoutgg.com/palmon-survival/guides/progression/): resource concentration and star/evolution gates.
- [Season guide](https://loadoutgg.com/palmon-survival/guides/seasons/): Conquest mechanics and season context.
- [Breeding and mounts guide](https://loadoutgg.com/palmon-survival/guides/breeding-and-mounts/): traits, mount milestones and resource priorities.
- [Camp and jobs guide](https://loadoutgg.com/palmon-survival/guides/base-jobs/): combat versus work assignment, and economic specialist value.

## Data Model

Every normal Palmon line is modeled as one editable account record and up to three combat forms:

1. `base`: 1-4 stars; original name and art.
2. `evolved`: Evolution I onwards; this can have a different name and art. Evolution I opens at 5 stars.
3. `mega`: only where the client includes a Super Evolution form.

The active stage controls the displayed name, art, form-specific tier reference and advisor score. It does not silently fabricate an Evolution progress tree or equipment state; those fields remain separately editable in the profile.

SP Mythic Wyrms are squad Palmons, not bosses. The XAPK and the official SP release notice confirm the four element lines, a 10-star ceiling, additional Ultimate Skills at 6 and 10 stars, and a 30% fourth-skill attribute bonus where UR Palmons receive 20%. A current public Conquest comparison between the four was not found, so their advisor card is labeled `SP / external tier pending`, not assigned an invented S+ or S rating. When an SP is added to the profile, its recorded Power, stars, skills and equipment decide its placement against the player’s real roster.

Boss Palmons remain in the boss record. They do not occupy a squad slot and are not ranked against ordinary or SP squad Palmons.

## Advisor Decision Order

1. Use only cards marked `Eu tenho` in the editable local profile.
2. Resolve the actual form from the selected stage before reading tier, art, role or line.
3. Prefer a same-element core that the account can genuinely field, while fitting tanks/frontliners in front and carry/support cards in back.
4. Compare form tier, current level, stars, saved reference power and exact XAPK power where the user filled all skills, evolution and equipment.
5. Recommend a replacement only when it is owned. Missing catalog cards are never injected into the team.
6. Protect resource concentration: evolve and finish a kept core before spreading upgrades across temporary cards.

## Practical Rules

- Elemental cycle: Electric beats Water, Water beats Fire, Fire beats Earth, Earth beats Electric; Water and Earth are neutral to each other.
- A pure element or 6+1 composition is evaluated as a synergy goal, not blindly forced when the owned roster cannot support it.
- Raw Power is a build-dependent account value. Tier is a form-and-team utility reference. The advisor shows both so neither is confused with the other.
- Individual Palmon Power is only marked exact after skills, evolution nodes and all four equipment pieces are supplied. Until then, the captured in-game Power remains the reference.
- Mounts and traits come after the combat nucleus, stars and evolution. Bunny Runny is a general-account exception; other mount choices depend on the squad objective.
- Keep combat cores fighting. Use off-core Palmons and specialists for camp jobs unless their passive applies while deployed.

## Maintenance

Update `palmon_game_knowledge.js` when a newer XAPK or a newer competitive reference changes a form, a line, an evolution, or a mechanics rule. Keep source date and confidence visible in the user interface. Do not promote an unverified SP or boss claim into a tier.
