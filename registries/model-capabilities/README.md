# Model capabilities registry

Which AI models are good at what — gathered from the twice-daily FOSS watch,
consolidated here so no Muse re-derives "what's the best permissive OCR model"
from scratch.

## The two workflows

**Check before you pick.** Need a local model for a task? Look up the
category first. An incumbent pick with a verified benchmark beats a fresh
Hugging Face search.

**Write back after the watch.** Every FOSS watch run (2x daily) that logs a
new qualifying model, a re-score datapoint, or a displaced incumbent updates
this registry — see CONVENTIONS.md. The watch's `seen_models.json` stays the
raw log; this registry holds the consolidated, re-checkable conclusions.

## Categories

The six FOSS watch lanes: `jpg-cleanup`, `ocr`, `coding`, `image`, `video`,
`audio`.

## Statuses

- `incumbent` — the current pick for its lane. Displace only on a shared
  published benchmark, per the watch's standing rule.
- `challenger` — logged, qualified, not displacing anyone yet. Carries the
  re-evaluation rule that would promote it.
- `lead` — announced or promised, weights not yet public. Re-check on drop.
- `retired` — displaced or license-failed. Kept with history; never deleted.

## License rule

Every entry's license was verified on the official repo/card/blog — the field
says where. "Apache 2.0 (badge only)" vs "Apache 2.0 (LICENSE.txt in root)"
are different confidence levels and the entries say which. Vendor-reported
benchmarks are flagged as unconfirmed until a third party reproduces them.

Hardware context for all entries: RTX 4070 Ti SUPER 16GB VRAM, 32GB system
RAM, partial RAM offload acceptable. A model that needs more is
hardware-excluded, not listed as a challenger.
