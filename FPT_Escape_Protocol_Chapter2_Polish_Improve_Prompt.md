# FPT Escape Protocol — Chapter 2 Polish & Presentation Fix Prompt

Please improve the current implementation of **FPT Escape Protocol Chapter 2** based on the following presentation, UI, scene-composition, and startup-flow corrections.

Do not redesign the whole game. Preserve the existing architecture, dialogue content, assets, chapter logic, save system, affinity system, ending logic, and current working features unless a change is explicitly required below.

The main goal of this task is to make Chapter 2 feel cleaner, more intentional, less visually crowded, and more like a polished visual novel.

---

## 1. Fix Character Overcrowding in Dialogue Scenes

The current implementation sometimes places too many characters on screen at the same time.

This is especially noticeable in Chapter 2 classroom scenes such as the philosophy lesson, where the system may display the entire cast even when only a few characters are actually relevant to the current conversation.

This must be corrected.

### New Scene Composition Rule

Do not automatically display every character who is logically present in the same room.

A visual novel scene should only display characters who are currently important to the immediate dialogue or interaction.

For most scenes:

```text
Recommended visible characters:
1–2 characters

Maximum visible characters:
3 characters
```

Three characters in one frame should already be treated as the practical upper limit.

Do not place 4, 5, or more character sprites on screen unless there is an extremely specific cinematic reason.

### Example: Philosophy Classroom

Even though the classroom logically contains:

```text
Main
Minh
Ngân
Nghi
Cô Triết
other students
```

they should NOT all be shown simultaneously.

If the current interaction is:

```text
Cô Triết speaking to Main
```

the screen may show:

```text
Cô Triết
Main
```

or, if Minh is directly participating:

```text
Cô Triết
Main
Minh
```

If the scene later changes to a group discussion:

```text
Main
Ngân
Nghi
```

then Cô Triết and Minh can temporarily disappear from the active composition.

They are still logically inside the classroom.

This is a **presentation decision**, not a literal story event.

Do not interpret this as characters physically leaving the room.

---

## 2. Distinguish “Scene Presence” from “Story Presence”

This rule is very important.

A character can still exist in the current location without needing to remain visually rendered.

Use two concepts:

```text
story_present
visual_active
```

Example:

```text
Cô Triết:
story_present = true
visual_active = false
```

This means she is still in the classroom, but she is not part of the current shot.

When her dialogue becomes relevant again, bring her back visually.

This avoids unnecessary sprite clutter.

---

## 3. Speaker Focus Still Applies

When multiple characters are visible:

### Current speaker

```text
brightness = normal
scale = normal or slightly emphasized
z-order = foreground
```

### Visible but non-speaking characters

```text
slightly dimmed
slightly pushed backward
lower visual emphasis
```

Do not completely hide a character merely because someone else starts speaking if that character is still part of the active shot.

However, characters that are no longer relevant to the current shot may be visually removed from the composition.

This is different from physically leaving the story scene.

---

## 4. Fix Dialogue Manager Position During Selection Options

There is currently a UI positioning bug in Chapter 2.

During normal dialogue, the dialogue manager / dialogue box correctly appears near the bottom of the screen.

However, when a selection / choice option appears, the dialogue UI is pushed upward toward the middle of the screen.

This must be fixed.

### Required Behavior

The dialogue box must remain anchored to the same lower-screen position during:

```text
normal dialogue
choice selection
Ngân Hint interaction
branch selection
ending choices
```

The appearance of choice buttons must not move the base dialogue box upward.

### Correct layout

Conceptually:

```text
---------------------------------
        CHARACTER AREA
---------------------------------



        CHOICE OPTIONS
        [ Choice A ]
        [ Choice B ]
        [ Choice C ]

---------------------------------
        DIALOGUE BOX
---------------------------------
```

The dialogue box stays in the bottom area.

The choice list should expand upward above it.

Do not vertically re-center the entire UI container.

---

## 5. Preserve Existing Dialogue Box Height and Anchor

If the current UI uses anchors, containers, or layout groups, keep the dialogue panel fixed to the lower region.

Suggested behavior:

```text
DialogueBox:
anchor_bottom = true
position = fixed

ChoiceContainer:
anchor relative to DialogueBox
expand_direction = upward
```

Do not solve the issue using arbitrary hardcoded offsets if the existing UI architecture supports proper anchoring.

The layout should remain stable across different resolutions.

---

## 6. Fix Game Startup Behavior

There is currently a startup-flow issue where launching the game may immediately enter gameplay.

This is incorrect.

Every normal game launch must begin at the **Main Menu**.

Correct startup flow:

```text
Launch Game
↓
Main Menu
↓
Player chooses:
- Continue
- New Game
- Chapter Select
- Load Game
- Settings
- Exit
```

Do not automatically enter Chapter 1 or Chapter 2 when launching the game.

### Exception

Automatic chapter transitions are allowed only after the player is already inside gameplay.

For example:

```text
Chapter 1 Good Ending
↓
[Continue to Chapter 2]
```

This is valid.

But a fresh application launch must never skip the Main Menu.

---

## 7. Improve Character Entrance and Exit Animations

The current character presentation relies too heavily on sprites moving in from the left side of the screen.

This animation is being overused and makes scenes feel repetitive and awkward.

Replace most of these character entrances with cleaner visual-novel-style transitions.

The desired feeling should be closer to:

```text
PowerPoint appearance/disappearance transitions
```

rather than characters physically sliding across the whole screen.

---

## 8. Recommended Character Appearance Animations

Use a small library of subtle transitions.

### Fade In

```text
opacity: 0 → 1
duration: 0.20–0.35 sec
```

Best default animation.

### Fade + Slight Scale

```text
opacity: 0 → 1
scale: 0.97 → 1.00
duration: 0.20–0.30 sec
```

Useful for important character appearances.

### Soft Rise

```text
opacity: 0 → 1
vertical offset: +20px → 0
duration: 0.20–0.30 sec
```

Useful occasionally.

Keep movement subtle.

### Crossfade Character Expression

When changing expression:

```text
old sprite → fade out
new sprite → fade in
```

Duration:

```text
0.10–0.20 sec
```

Do not make expression changes look like a new character entering the room.

---

## 9. Recommended Character Disappearance

Use:

```text
Fade Out
```

or:

```text
Fade + Slight Scale Down
```

Example:

```text
opacity: 1 → 0
scale: 1.00 → 0.97
duration: 0.20–0.30 sec
```

Avoid repeatedly sliding characters off the edge of the screen.

---

## 10. Sliding Animation Should Become Rare

Do not completely delete slide transitions if the existing system uses them.

Instead, change their usage priority.

Recommended priority:

```text
Fade                         = very common
Fade + slight scale          = common
Soft rise                    = occasional
Short directional slide      = rare
Full screen side entrance    = very rare
```

A full left-to-right entrance should only be used if it actually matches the scene.

Example:

```text
Ngân suddenly runs into the scene
```

A slide may be appropriate.

But for:

```text
Nghi begins speaking
Cô Triết returns to the active shot
Minh becomes relevant
```

use fade/crossfade instead.

---

## 11. Do Not Animate Every Speaker Change

Changing the active speaker does not mean the entire sprite composition must re-enter.

If three characters are already visible:

```text
Main
Ngân
Nghi
```

and speaker changes:

```text
Ngân → Nghi → Main
```

do not repeatedly remove and re-add sprites.

Instead:

```text
dim previous speaker
highlight current speaker
adjust z-order
slightly change scale if needed
```

This should be smooth and subtle.

---

## 12. Suggested Visual State System

If compatible with the current codebase, every character could conceptually have:

```text
Hidden
Background
Active
Entering
Leaving
```

Where:

### Hidden
Not currently shown.

### Background
Visible but not speaking.

### Active
Current speaker.

### Entering
Playing appearance animation.

### Leaving
Playing disappearance animation.

Do not implement a new state machine if the project already has equivalent logic.

Reuse existing systems where possible.

---

## 13. Example — Improved Philosophy Scene Composition

Instead of:

```text
Main
Minh
Ngân
Nghi
Cô Triết
```

all visible simultaneously:

### Lecturer section

Show:

```text
Cô Triết
Main
Minh
```

Then when Nghi is introduced:

fade out Minh if unnecessary.

Show:

```text
Cô Triết
Nghi
Main
```

Then during group discussion:

fade out Cô Triết.

Show:

```text
Main
Ngân
Nghi
```

This is much cleaner.

No character has literally left the classroom.

Only the active composition changes.

---

## 14. Example — Ngân Hint Scene

During:

```text
Main + Nghi conversation
```

normally show:

```text
Main
Nghi
```

When the player presses:

```text
💡 Hỏi Ngân
```

do not necessarily add Ngân as a third full-size sprite.

Prefer:

```text
small message UI
phone-style popup
Ngân avatar portrait
text message panel
```

This prevents unnecessary sprite spam.

Only show full Ngân sprite if she is physically part of that conversation.

---

## 15. Scene Direction Principle

For every dialogue scene, ask:

```text
Who does the player need to visually focus on right now?
```

Do not ask:

```text
Who logically exists somewhere in this location?
```

The first question determines sprite composition.

The second only determines story logic.

---

## 16. Maintain Visual Hierarchy

Recommended priority:

```text
1. Current speaker
2. Direct conversation partner
3. Optional third participant
4. Everyone else → not visually rendered
```

This should be the default rule for Chapter 2.

---

## 17. Do Not Break Existing Features

While making these fixes, preserve:

```text
Chapter 1
Chapter 2 unlock
Chapter Select
save/load
NghiAffinity
NghiComfort
Ngân hidden route
Ngân Hint system
all Chapter 2 endings
existing CGs
existing dialogue branching
```

Do not rewrite working narrative logic unnecessarily.

---

## 18. Required Regression Checks

After implementation, verify:

### Startup

```text
[ ] Game launches into Main Menu.
[ ] New Game still works.
[ ] Continue still works.
[ ] Chapter Select still works.
```

### Dialogue UI

```text
[ ] Dialogue box remains at bottom during normal dialogue.
[ ] Dialogue box remains at bottom during choices.
[ ] Choice list expands upward.
[ ] Ngân Hint does not move dialogue UI.
[ ] Different screen resolutions do not break the layout.
```

### Character rendering

```text
[ ] Scenes no longer spam unnecessary characters.
[ ] Most shots contain 1–2 characters.
[ ] Maximum normal composition is 3 characters.
[ ] Characters may remain story-present without being visually shown.
[ ] Current speaker receives foreground emphasis.
[ ] Background speakers are dimmed correctly.
```

### Character animations

```text
[ ] Default entrance uses Fade In.
[ ] Default exit uses Fade Out.
[ ] Expression changes use crossfade.
[ ] Speaker changes do not trigger full entrance animations.
[ ] Full screen slide-in is rare.
[ ] Repetitive left-side entrance spam is removed.
```

---

## 19. Final Quality Target

Chapter 2 should feel like a polished visual novel rather than a stage where every available character sprite is constantly visible.

The desired visual rhythm is:

```text
clean composition
→ clear speaker focus
→ subtle fade transitions
→ stable dialogue UI
→ minimal unnecessary movement
→ cinematic scene changes
```

Prioritize clarity and natural presentation over showing more sprites.

The final result should feel intentional, readable, smooth, and professionally staged.

---

## Final Report

After completing the improvements, report:

```text
1. Files modified
2. Character rendering logic changed
3. New entrance/exit animations
4. Dialogue UI positioning fix
5. Startup flow fix
6. Scenes cleaned up
7. Any scenes still using slide transitions and why
8. Regression tests performed
9. Remaining known issues
```

Do not only respond with “Done.”
