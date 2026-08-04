---
format: 1080x1920
duration: 17.6s
message: "Cho Gao coconut — a Mekong Delta specialty, naturally sweet, rich and fresh"
arc: Hook → Product intro (origin) → Sensory benefit → Versatility benefit → CTA
audience: "Consumers curious about Vietnamese regional specialties and clean local produce"
mode: autonomous
music: none
---

## Video direction

- **Palette system** (from `frame.md`): cream (`#efe7d4`) as the default reading ground; forest green (`#2e4a2a`) reserved for the hook and CTA — the two gravity moments; pink accent used only where display-scale contrast holds (large hero words on green), never as small body text on cream (see the Contrast fix in Frame 3's history — pink-on-cream fails the 3:1 floor at this scale).
- **Motion grammar + reveal model:** long-tail `power3` eases throughout (no bounce/spring except the restrained marker-pop accents named below). This build now carries real narration (`SCRIPT.md`, Kokoro `af_heart`, English) with captions enabled — each frame's on-screen copy is therefore SHORT hero copy (2–4 words), not the full spoken sentence (the caption track already shows the full line). Reveal each hero phrase on its spoken cue, never before. Type is Source Serif 4 weight 500 for every display line where a real font file exists in the project; fall back to the generic `serif` keyword when it doesn't (no font files are currently staged — see Known Gaps in prior frame builds).
- **Rhythm / held-frame allocation:** Frame 1 (hook) and Frame 5 (CTA) are the two deliberate holds — each resolves early and sits still for its back half. Frames 2–4 stay lightly active (one reveal move each) but still end on a settle, never a freeze mid-motion.
- **Negative list:** no shadows, no gradients, no glow, no third typeface, no stock photography, no floating decorative shapes standing in for a real asset (there are no real assets in this no-capture build — content stays typographic). Both failure modes are forbidden: no slideshow (front-load-then-freeze) and no screensaver (independent drift with no named reveal).

## Frame 1 — Hook

- scene: Short hero words punch in on a deep green field, timed to the VO
- voiceover: "There's a coconut you'll remember after just one taste."
- duration: 3.072s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Curiosity
- beat: curiosity
- blueprint: kinetic-type-beats (Reproduce) — Hook (flash) variant
- focal: none — typography-only frame
- asset_candidates:

narrativeRole: Open with curiosity before naming the product.
keyMessage: There's a coconut worth remembering.

Scene 1 (0.0–1.35s): solid green (`{colors.green}`) field. As the VO says "a coconut," the hero words "ONE TASTE." flash-cut in dead-center — cream Source Serif 4 `title-card`, weight 500, no fade/slide, hard CUT only. Centered, ~35% of frame, deep negative space around it.
Scene 2 (1.35–3.072s): as the VO reaches "you'll remember," hard cut clears line 1; "YOU'LL REMEMBER." lands dead-center in pink `title-card` (pink only valid here at display scale on green), same size class, with a pink drawn underline sweeping left→right beneath "REMEMBER." Holds to end — settle only, no further motion.

## Frame 2 — Product intro (origin)

- scene: Product name, then origin, as short hero lines timed to the VO
- voiceover: "Cho Gao coconut — a specialty from Tien Giang, in Vietnam's Mekong Delta."
- duration: 4.928s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-intro.html
- type: product_intro
- persuasion: Authority by association
- beat: pride
- blueprint: titlecard-reveal (Adapt) — Benefits' single slide-up crossfade, repurposed for a name→origin handoff instead of a value→qualifier one
- focal: none — typography-only frame
- asset_candidates:

narrativeRole: Introduce the product name and anchor it to a well-known growing region.
keyMessage: This specialty has a clear, proud origin.

Adapt: keep titlecard-reveal's one-restrained-move + hold contract and its single slide-up crossfade signature; change only what fills the two beats (product name, then origin) in place of a value/qualifier pair.
Scene 1 (0.0–0.49s): static cream (`{colors.cream}`) field, camera locked — establishes the calm open, timed just ahead of the VO naming the product.
Scene 2 (0.49–2.63s): as the VO says "Cho Gao coconut," "Cho Gao Coconut" fades in centered while scaling ~95%→100%, green `headline-xl`, smooth ease-out settle. Centered, ~40% of frame.
Scene 3 (2.63–4.928s): as the VO reaches "Tien Giang," the ONE move — the name translates up and fades while "Tien Giang, Vietnam" (ink `title-card-sm`) translates up from below-center and fades in to take its place. Holds to end.

## Frame 3 — Sensory benefit

- scene: Two short taste-word beats timed to the VO's two sentences
- voiceover: "Naturally sweet water. Thick, rich coconut meat."
- duration: 3.093s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-taste.html
- type: benefit_highlight
- persuasion: Show-don't-tell proof
- beat: satisfaction
- blueprint: titlecard-reveal (Reproduce) — one clean two-line value beat, single slide-up crossfade
- focal: none — typography-only frame
- asset_candidates:

narrativeRole: Give the taste a concrete, specific character.
keyMessage: The taste has clear, recognizable traits.

Scene 1 (0.0–0.265s): static cream field, camera locked.
Scene 2 (0.265–1.414s): as the VO says "sweet water," "Sweet Water." fades in centered, scaling ~95%→100%, ink `headline` (ink-on-cream — the contrast-safe pairing), settle.
Scene 3 (1.414–3.093s): as the VO reaches "rich coconut meat," the ONE move — "Sweet Water." translates up and fades while "Rich Coconut Meat." (green `headline`) translates up from below-center and fades in to take its place. Holds to end.

## Frame 4 — Versatility benefit

- scene: Three short use-case items timed to the VO's three clauses
- voiceover: "Drink it fresh. Cook with it. It fits every meal."
- duration: 2.752s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-versatility.html
- type: benefit_highlight
- persuasion: Value stacking
- beat: ease
- blueprint: grid-card-assemble (Reproduce) — Benefits vertical-list, BUILD sub-mode
- focal: none — typography-only frame
- asset_candidates:

narrativeRole: Show the product fits naturally into everyday use.
keyMessage: It works in more than one way, without effort.

Scene 1 (0.0–0.55s): cream field; mono `label` "WAYS TO ENJOY" sets the topbar/list header, upper-left. As the VO says "drink it fresh," item 1 "Drink Fresh" arrives: pink marker spring-pops, a pill mask-wipe reveals the ink text sliding into slot 1. Upper-left third, ~35% of frame.
Scene 2 (0.55–1.56s): as the VO says "cook with it," item 2 "Cook With It" arrives via the same marker-pop + pill mask-wipe into slot 2, directly beneath; item 1 stays fully lit (co-resident, accumulating).
Scene 3 (1.56–2.752s): as the VO says "every meal," item 3 "Every Meal" arrives into slot 3 the same way; the completed 3-line list holds with a gentle continuous parallax/sine float — no further arrivals, settle to end.

## Frame 5 — CTA

- scene: Name, then a calm closing line, timed to the VO
- voiceover: "Cho Gao coconut — a taste of the Mekong Delta, worth trying."
- duration: 3.776s
- transition_in: crossfade
- status: animated
- src: compositions/frames/05-cta.html
- type: cta
- persuasion: Future pacing
- beat: peace of mind
- blueprint: titlecard-reveal (Adapt) — CTA end-card register without a logo mark; the product name itself is the lockup
- focal: none — typography-only frame
- asset_candidates:

narrativeRole: Close with a gentle, non-inflated invitation.
keyMessage: Worth trying, said plainly.

Adapt: keep the one-restrained-move + long static hold contract; the "logo" this build lands on is the product wordmark itself (no real brand mark exists), so the closing card is name → tagline via one slide-up crossfade, held the longest of the shot.
Scene 1 (0.0–0.377s): static green (`{colors.green}`) field, camera locked — mirrors Frame 1's ground for a bookend feel.
Scene 2 (0.377–1.636s): as the VO says "Cho Gao coconut" again, "Cho Gao Coconut" fades in centered, scaling ~95%→100%, pink `display` (valid at display scale on green), settle.
Scene 3 (1.636–3.776s): as the VO reaches "worth trying," the ONE move — the name translates up and fades while "Worth trying." (cream `body-card`) translates up from below-center and fades in beneath. Holds static to the final frame — the longest beat of the shot.
