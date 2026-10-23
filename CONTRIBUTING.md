# Contributing to the Prometheus Ember Loom

Anyone can propose changes. Nothing goes live without review: the `main` branch **is** the live site at https://prometheus-pantheon.com, and it only changes through an approved pull request.

## How a change goes live
1. **Propose.** Open an issue (ember idea, chapter, Forge) or fork the repo and open a pull request.
2. **Discuss.** Share the link in the Telegram group so the community can weigh in.
3. **Automatic check.** Every pull request rebuilds the site and checks that the pages and scripts are valid.
4. **Review.** A maintainer reviews it. Lore chapters need a community poll first (see `lore/README.md`).
5. **Merge = live.** Once approved and merged, the site updates within a few minutes.

## Where to edit
| You want to change | Edit this source |
|---|---|
| Home page | `site/pages/home.html` |
| The Hearth | `site/pages/hearth.html` |
| Lore and the Loom's law | `lore/*.md` |
| The proposal | `proposal.md` |
| Ember Generator ideas | `site/ember-generator.html`: hand-picked ideas in `IDEAS`, generated ones in `FAMILIES` |
| Shared look | `assets/site.css` |

Then run `python3 site/build.py` and commit both the source and the rebuilt pages.

**Multiply the Loom:** each generated family combines what × where × for whom × with whom × when × how it spreads. Adding one sensible word to a list multiplies the number of ideas. Keep every combination a real, safe, sensible deed: if a word only makes sense with some others, attach it to them (see how `where` and `for` can be set per item).

## What gets merged
- Honest, verifiable content. No claims that Andy Ayrey or Truth Terminal endorse, hold or run anything.
- No wallet addresses, except a Forge proposal's own public address.
- No personal data without consent.
- Everything is CC0: by contributing, you release your work into the public domain.

## Maintainers
Today the initiator reviews pull requests. The goal is to hand this to rotating community Tenders: once there are trusted contributors, they become maintainers and approvals no longer depend on one person.
