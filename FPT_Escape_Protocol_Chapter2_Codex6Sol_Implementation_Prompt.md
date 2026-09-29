# FPT Escape Protocol — Chapter 2 Implementation Brief + Full Narrative Script
## Target agent: ChatGPT / Codex 6-Sol

> **Purpose:** Add a complete, production-ready Chapter 2 to the existing **FPT Escape Protocol** project after the player successfully reaches the **Good Ending of Chapter 1**.  
> The agent must inspect the existing repository first, preserve the current architecture, reuse the current VN framework/UI conventions, and integrate Chapter 2 without breaking Chapter 1.

---

# 0. EXECUTION RULES FOR THE AGENT

## 0.1 Repository-first workflow
Before editing any file:

1. Inspect the project structure.
2. Identify:
   - engine/framework,
   - scene/chapter architecture,
   - dialogue data format,
   - save/load system,
   - character sprite system,
   - background/map system,
   - audio system,
   - menu/chapter select system,
   - ending/unlock flags,
   - any existing relationship/choice system.
3. Reuse the existing architecture instead of creating a parallel framework.
4. Only add abstractions if the current architecture genuinely cannot support the requested behavior.
5. Keep Chapter 1 fully playable and unchanged unless a small compatibility change is required.

Do **not** rewrite the project from scratch.

---

# 1. CHAPTER 2 HIGH-LEVEL GOAL

Chapter 2 continues immediately after the **Good Ending of Chapter 1**.

Chapter 1 was primarily about escaping FPT.

Chapter 2 deliberately changes the tone:

> The protagonist survived the escape protocol.  
> Now he must survive something far more dangerous: trying to confess to a girl with **zero dating experience and maximum IT-brain behavior**.

The chapter introduces:

- **Nghi** — new female lead / new student.
- **Ngân** — female supporting character, the protagonist's close classmate and longtime friend.
- **Cô Triết** — philosophy lecturer.
- **Cô Y Tá** — school nurse.
- **Thầy Thể Dục** — physical education lecturer.

Returning characters:

- **Main / Nam chính**
- **Minh** — best friend.

The main route focuses on the protagonist gradually falling for **Nghi** and awkwardly trying to raise her affinity through several new school events.

At the same time, **Ngân** quietly becomes emotionally important and supports the protagonist throughout the chapter.

This creates three endings:

1. **Good Ending — Nghi accepts the confession.**
2. **Bad Ending — Nghi refuses the confession; Main goes drinking with Minh.**
3. **Easter Egg Ending — Main realizes he actually loves Ngân and successfully confesses to her.**
   - This is a full-game terminal ending.
   - It intentionally closes the future chapter route.

---

# 2. CHAPTER UNLOCK + MAIN MENU INTEGRATION

## 2.1 Unlock rule

After the player completes Chapter 1 with its Good Ending, persist:

```text
chapter2_unlocked = true
chapter1_canonical_result = "good"
```

This must survive save/load and app restart.

## 2.2 Continue flow

At the end of Chapter 1 Good Ending, after the Chapter 1 ending screen, present:

```text
[Tiếp tục Chương 2]
[Trở về Menu Chính]
```

Selecting `Tiếp tục Chương 2` must initialize Chapter 2 state and begin `CH2_00`.

## 2.3 Chapter Select

Add or extend the main menu with:

```text
CHAPTER SELECT
- Chương 1
- Chương 2
```

Rules:

- Before Chapter 1 Good Ending:
  - Chapter 2 is visible but locked.
- After Chapter 1 Good Ending:
  - Chapter 2 becomes selectable.
- Starting Chapter 2 directly from Chapter Select must assume the canonical Chapter 1 Good Ending state.
- Do not require the player to replay Chapter 1 once Chapter 2 is unlocked.

If the project already has a chapter select system, extend it instead of replacing it.

---

# 3. IMPORTANT CORRECTION: CHARACTER VISIBILITY / SPEAKER FOCUS SYSTEM

This corrects a previous implementation misunderstanding.

## 3.1 Do NOT literally hide characters who are still present in the conversation

If multiple characters are physically present in the current scene, they should remain visible even when they are not currently speaking.

The meaning of “hide/show focus” is:

### Current speaker
- move visually slightly forward,
- use normal/full brightness,
- full opacity,
- normal or slightly larger scale,
- highest relevant z-order.

### Non-speaking characters who are still present
- remain visible,
- dim/darken them,
- move them visually slightly backward,
- optionally reduce scale slightly,
- lower z-order.

### Only fully hide/remove a character when
- they physically leave the scene,
- the script explicitly cuts away from them,
- the scene changes.

Recommended behavior:

```text
speaker:
  brightness = 1.0
  alpha = 1.0
  scale = 1.00
  z = foreground

non_speaker_present:
  brightness = 0.55–0.70
  alpha = 0.85–1.0
  scale = 0.94–0.97
  z = background

transition:
  0.15–0.25 sec smooth tween
```

Never flicker a character fully on/off simply because another character begins speaking.

---

# 4. NEW CHAPTER 2 GAMEPLAY SYSTEMS

Use the existing choice/dialogue system and add these chapter-local state variables.

```text
NghiAffinity       = 0
NghiComfort        = 0

NganAffinity       = 0
NganSpecialFlags   = 0

NganHintsRemaining = 3
NganHintsUsed      = 0

CH2MajorFail       = false
```

`NganAffinity` and `NganSpecialFlags` should remain hidden from the player.

`NghiAffinity` and `NghiComfort` can also remain hidden unless the existing game already visibly exposes affinity.

---

# 5. NGÂN HINT SYSTEM — CHAPTER 2 SPECIAL FEATURE

## 5.1 Core concept

Ngân acts like a hilariously human “dating assistant” for Main.

During selected conversations where Main is trying to:

- impress Nghi,
- avoid saying something stupid,
- increase NghiAffinity,
- increase NghiComfort,

show a special optional button:

```text
💡 Hỏi Ngân (3/3)
```

After use:

```text
💡 Hỏi Ngân (2/3)
```

and so on.

Maximum for all of Chapter 2:

```text
3 total hints
```

No recharge.
No restoration.
No item can refill hints.

## 5.2 Hint philosophy

A hint should **not always reveal the best answer directly**.

Ngân often:

- eliminates the worst option,
- warns Main not to say something stupid,
- gives a short social clue,
- teases him.

This keeps player agency intact.

Example:

Choice:

```text
A. "Bạn đang đọc gì vậy?"
B. "Hôm nay bạn xinh thật."
C. "Tôi cũng đọc nhiều lắm."
D. Im lặng ngồi cạnh.
```

Ngân hint:

```text
Ngân: "Đừng chọn B."
Ngân: "Tao không biết mày đang định làm gì, nhưng đừng chọn B."
```

## 5.3 Important secret-route behavior

The Easter Egg Ngân route is intentionally easier if the player does **not** treat Ngân purely as a tool.

One ending condition is:

```text
NganHintsUsed <= 1
```

This creates a thematic contrast:

> If the player only talks to Ngân when they need help getting Nghi, they remain on Nghi's route.  
> If the player actually spends time with Ngân as a person, her route becomes possible.

---

# 6. NEW CHARACTERS

## 6.1 Nghi — Female Lead

Role:
- Main romance target.
- New student in class.

Personality:
- Kuudere.
- Quiet.
- Observant.
- Polite.
- Intelligent.
- Emotionally reserved.
- Not rude.
- Not edgy.
- Not emotionless.

Her cold appearance comes from:
- social awkwardness,
- difficulty initiating conversations,
- being new,
- preferring to observe before speaking.

Over the chapter, her expressions should gradually soften.

Required sprite emotions:

```text
Nghi_Normal
Nghi_SoftSmile
Nghi_HappySmile
Nghi_Confused
Nghi_Annoyed
Nghi_Sad
Nghi_Embarrassed
```

Visual:
- long pale/blonde hair,
- elegant FPT-themed school uniform,
- white shirt,
- pleated skirt,
- two long black stockings,
- subtle hair accessory,
- clean and academically proper appearance.

---

## 6.2 Ngân — Female Supporting Character / Secret Route

Role:
- Main's close classmate.
- Longtime friend.
- Social bridge between Main and Nghi.
- Optional final romantic route.

Personality:
- energetic,
- teasing,
- socially competent,
- playful,
- warm,
- fast-talking,
- knows Main extremely well.

Ngân must NOT feel like a disposable dating tutorial NPC.

She must have:
- her own reactions,
- her own feelings,
- moments unrelated to helping Main,
- subtle jealousy / pauses,
- genuine friendship chemistry.

Required sprite emotions:

```text
Ngan_Normal
Ngan_Happy
Ngan_Excited
Ngan_Sad
Ngan_Angry
Ngan_BigLaugh
Ngan_Confused
Ngan_Thinking
Ngan_Embarrassed
```

---

## 6.3 Cô Triết — Philosophy Lecturer

Role:
- New lecturer.
- Provides comedy and thematic framing.
- Uses Marxist-Leninist philosophy concepts as part of the jokes and emotional theme.

Personality:
- strict,
- intelligent,
- composed,
- sharp,
- dry humor,
- instantly notices when Main whispers nonsense.

Do not make her a caricature who only yells.

She should occasionally deliver surprisingly meaningful lines.

---

## 6.4 Thầy Thể Dục — PE Lecturer

Role:
- Physical comedy character.
- Introduces the sports field.
- Causes Main's disastrous attempt to impress Nghi.

Personality:
- enthusiastic,
- loud,
- intimidating physique,
- ultimately supportive teacher.

He looks like a final boss but behaves like a legitimate lecturer.

---

## 6.5 Cô Y Tá — School Nurse

Role:
- Infirmary character.
- Deadpan comedy.
- Helps create an intimate Nghi/Main recovery scene.

Personality:
- calm,
- matter-of-fact,
- slightly mysterious,
- dry humor.

---

## 6.6 Minh — Returning Best Friend

Role:
- Main's best friend.
- Comic relief.
- Bad Ending drinking partner.

Keep his existing Chapter 1 personality and voice.

---

# 7. NEW / REUSED MAPS

Use the new assets if already present in the project. Search asset directories before creating placeholders.

## New backgrounds

### Philosophy classroom
```text
Philosophy_Morning
Philosophy_Afternoon
Philosophy_Night
```

### Sports field
```text
SportsField_Morning
SportsField_Afternoon
SportsField_Night
```

### Infirmary
```text
Infirmary_Morning
Infirmary_Afternoon
Infirmary_Night
```

### Library
```text
Library_Morning
Library_Afternoon
Library_Night
```

### School rooftop
```text
Rooftop_Morning
Rooftop_Afternoon
Rooftop_Night
```

### Nearby drinking place
```text
NearbyPub_Night
```

## Reuse existing maps if available

```text
Main Classroom
School Hallway
School Gate
Canteen
Campus Courtyard
```

---

# 8. CHAPTER 2 FLOW

Recommended scene order:

```text
CH2_00  The Escape Was Temporary
CH2_01  Ngân
CH2_02  New Student
CH2_03  First Contact
CH2_04  Human Dating Assistant
CH2_05  Library Event
CH2_06  Physical Education Boss Fight
CH2_07  Infirmary Event
CH2_08  Contradictions
CH2_09  After-School Quiet
CH2_10  The Question
CH2_11  Confession Setup
CH2_12A Good Ending — Nghi
CH2_12B Bad Ending — 404 Love Not Found
CH2_12C Easter Egg Ending — Ngân
```

The exact implementation can split these into more engine scenes if required, but the narrative order must remain consistent.

---

# 9. FULL CHAPTER 2 DIALOGUE SCRIPT

---

# CH2_00 — THE ESCAPE WAS TEMPORARY

**Map:** Existing school gate — Morning  
**Cast:** Main, Minh

Purpose:
- Direct continuation from Chapter 1 Good Ending.
- Immediate comedy.
- Establish that “escaping FPT” did not mean graduating.

### Dialogue

**Minh:**  
“Dậy rồi à, chiến thần vượt ngục?”

**Main:**  
“Đừng gọi tao như phạm nhân.”

**Minh:**  
“Hôm qua mày chạy khỏi trường như đang né truy nã.”

**Main:**  
“Tao đã thoát.”

**Minh:**  
“Ừ.”

**Main:**  
“Cuối cùng tao cũng tự do.”

**Minh:**  
“...Mày biết hôm nay vẫn có tiết đúng không?”

**Main:**  
“...”

**Minh:**  
“...”

**Main:**  
“Tao tưởng Good Ending rồi?”

**Minh:**  
“Good Ending của hôm qua.”

**Main:**  
“Game gì scam vậy?”

**Minh:**  
“Đời.”

Pause.

**Main:**  
“Cho tao quay lại Bad Ending được không?”

**Minh:**  
“Đi học.”

Transition into campus.

---

# CH2_01 — NGÂN

**Map:** Main classroom / hallway — Morning  
**Cast:** Main, Minh, Ngân

Ngân approaches from behind.

**Ngân:**  
“Ê.”

Main turns.

**Main:**  
“Ồ.”

**Ngân:**  
“Nghe nói hôm qua có thằng chạy khỏi trường như tội phạm.”

**Main:**  
“Tin giả.”

**Ngân:**  
“Camera quay được.”

**Main:**  
“Tin thật.”

**Ngân:**  
“Lại còn chạy ngang qua chỗ bảo vệ.”

**Main:**  
“Đấy gọi là route tối ưu.”

**Minh:**  
“Tối ưu kiểu gì suýt ăn biên bản?”

**Main:**  
“Dynamic routing.”

**Ngân:**  
“Dynamic cái đầu mày.”

Ngân lightly hits Main's shoulder.

### Optional hidden Ngân choice

```text
A. "Sáng nay trông mày vui dữ."
B. "Sáng nay trông mày xinh đấy."
C. "Đi lẹ không trễ."
```

### A
**Ngân:**  
“Vui vì thấy mày vẫn còn sống.”

No stat change.

### B — Secret route flag
**Main:**  
“Sáng nay trông mày xinh đấy.”

Ngân pauses.

Switch briefly to `Ngan_Embarrassed`, then back to normal.

**Ngân:**  
“...”

**Main:**  
“Gì?”

**Ngân:**  
“Không có gì.”

**Main:**  
“Ủa?”

**Ngân:**  
“Đi học.”

State:

```text
NganAffinity += 2
NganSpecialFlags += 1
```

### C
Proceed normally.

---

# CH2_02 — NEW STUDENT

**Map:** Philosophy classroom — Morning  
**Cast:** Main, Minh, Ngân, Cô Triết, Nghi

Cô Triết enters.

All student sprites remain visible according to the speaker-focus rule.

**Cô Triết:**  
“Ổn định chỗ ngồi.”

**Cô Triết:**  
“Hôm nay chúng ta bắt đầu với một khái niệm rất đơn giản.”

She writes on the board.

**Cô Triết:**  
“Mâu thuẫn.”

Main whispers to Minh.

**Main:**  
“Mâu thuẫn lớn nhất đời tao là muốn ngủ nhưng phải đi học.”

Without turning around:

**Cô Triết:**  
“Em áo đen cuối lớp.”

Main freezes.

**Main:**  
“Dạ?”

**Cô Triết:**  
“Ví dụ rất thực tế.”

Minh lowers his head, laughing.

**Ngân:**  
“Chết chưa.”

**Main:**  
“Cô nghe kiểu gì vậy...”

**Cô Triết:**  
“Cô vẫn nghe.”

**Main:**  
“Dạ em xin lỗi.”

A short beat.

**Cô Triết:**  
“Trước khi bắt đầu, lớp chúng ta có một sinh viên mới.”

Nghi enters.

**Nghi:**  
“Chào mọi người.”

**Nghi:**  
“Mình là Nghi.”

**Nghi:**  
“Mong được mọi người giúp đỡ.”

Main looks at Nghi.

Use comedic internal/system overlay if the project supports it:

```text
[UNKNOWN PROCESS DETECTED]
Heart.exe CPU usage: 97%
SocialSkill.dll: NOT FOUND
```

**Minh:**  
“Ê.”

No answer.

**Minh:**  
“Ê.”

No answer.

Ngân looks at Main, then Nghi, then Main again.

**Ngân:**  
“...Đừng nói với tao.”

**Main:**  
“Tao yêu rồi.”

**Ngân:**  
“Mày còn chưa biết họ người ta.”

**Main:**  
“Tình yêu không cần database đầy đủ.”

**Ngân:**  
“Im.”

---

# CH2_03 — FIRST CONTACT

**Map:** Philosophy classroom — Morning  
**Cast:** Main, Ngân, Nghi, Cô Triết

Cô Triết assigns small group discussion.

**Cô Triết:**  
“Ba người một nhóm.”

**Cô Triết:**  
“Trả lời câu hỏi này.”

Board:

```text
"Mâu thuẫn có phải lúc nào cũng mang ý nghĩa tiêu cực?"
```

Main, Ngân, Nghi end up in the same group.

**Ngân:**  
“Nghi nghĩ sao?”

**Nghi:**  
“Không hẳn.”

**Nghi:**  
“Nếu không có mâu thuẫn thì nhiều sự vật cũng không có động lực để thay đổi.”

**Nghi:**  
“Quan trọng là mâu thuẫn đó phát triển theo hướng nào.”

Main is clearly more focused on Nghi than the philosophy topic.

**Ngân:**  
“Ê.”

**Main:**  
“Hả?”

**Ngân:**  
“Nghe người ta nói kìa.”

---

## Choice 1 — First Nghi affinity choice

Display Ngân Hint button here.

```text
A. "Ý bạn khá giống sự thống nhất và đấu tranh giữa các mặt đối lập."
B. "Ừ, mình cũng nghĩ vậy."
C. "Bạn nói hay thật."
D. "Bạn có người yêu chưa?"
```

### Optional Ngân Hint

If used:

```text
NganHintsRemaining -= 1
NganHintsUsed += 1
```

Phone-style side message:

**Ngân:**  
“Nếu mày chọn D tao sẽ tự tay đẩy mày ra khỏi nhóm.”

Do not select an answer automatically.

---

### A — best intellectual answer

**Main:**  
“Ý bạn khá giống sự thống nhất và đấu tranh giữa các mặt đối lập.”

Nghi looks at Main.

**Nghi:**  
“Ừ.”

**Nghi:**  
“Bạn có nghe bài.”

**Main:**  
“...Tất nhiên.”

Ngân quietly looks at him.

**Ngân:**  
“Xạo.”

State:

```text
NghiAffinity += 2
NghiComfort += 1
```

---

### B — safe

**Main:**  
“Ừ, mình cũng nghĩ vậy.”

**Nghi:**  
“Ừm.”

State:

```text
NghiAffinity += 1
```

---

### C — awkward compliment

**Main:**  
“Bạn nói hay thật.”

**Nghi:**  
“...Cảm ơn.”

State:

```text
NghiAffinity += 1
NghiComfort -= 1
```

---

### D — social disaster

**Main:**  
“Bạn có người yêu chưa?”

Silence.

Ngân slowly turns toward him.

**Ngân:**  
“...”

Nghi blinks.

**Nghi:**  
“Không.”

**Main:**  
“Ồ.”

**Ngân:**  
“Xin lỗi Nghi.”

**Ngân:**  
“Nó bị lỗi firmware.”

State:

```text
NghiComfort -= 3
CH2MajorFail = true
```

Do not hard-lock the Good Ending yet; recovery should still be possible.

---

# CH2_04 — HUMAN DATING ASSISTANT

**Map:** Hallway — Late morning  
**Cast:** Main, Ngân

Main pulls Ngân aside.

**Main:**  
“Ngân.”

**Ngân:**  
“Không.”

**Main:**  
“Tao còn chưa nói.”

**Ngân:**  
“Tao biết.”

**Main:**  
“Biết gì?”

**Ngân:**  
“‘Dạy tao tán Nghi.’”

Pause.

**Main:**  
“...Dạy tao tán Nghi.”

**Ngân:**  
“Biết ngay.”

**Main:**  
“Cứu tao.”

**Ngân:**  
“Kinh nghiệm yêu đương?”

**Main:**  
“Không.”

**Ngân:**  
“Không là bao nhiêu?”

**Main:**  
“Không có.”

Ngân stares at him.

**Ngân:**  
“Thế bắt đầu bằng việc đừng nói mấy câu ngu.”

**Main:**  
“Cụ thể?”

**Ngân:**  
“Ví dụ như hỏi người ta có người yêu chưa sau bốn phút quen biết.”

If Choice D was selected earlier:

**Main:**  
“Đó là data collection.”

**Ngân:**  
“Đấy là phá hoại xã hội.”

Otherwise:

**Main:**  
“Tao đâu có ngu vậy.”

**Ngân:**  
“Chưa thôi.”

Ngân sighs.

**Ngân:**  
“Được rồi.”

**Ngân:**  
“Tao cứu mày ba lần.”

**Main:**  
“Ba?”

**Ngân:**  
“Ba.”

**Main:**  
“Sao ít vậy?”

**Ngân:**  
“Vì tao còn phải sống cuộc đời của tao.”

Small pause.

**Main:**  
“Deal.”

Unlock UI:

```text
NGÂN HINT UNLOCKED
3 USES AVAILABLE
```

---

# CH2_05 — LIBRARY EVENT

**Map:** Library — Afternoon  
**Cast:** Main, Nghi

Main notices Nghi studying alone.

Nghi is reading.

Main approaches.

**Main:**  
“Chỗ này có ai ngồi chưa?”

**Nghi:**  
“Chưa.”

Main sits nearby.

Small silence.

---

## Choice 2

Show Ngân Hint button.

```text
A. "Bạn đang đọc gì vậy?"
B. "Hôm nay bạn xinh thật."
C. "Tôi cũng đọc nhiều lắm."
D. Im lặng ngồi cạnh.
```

### Hint

**Ngân (message):**  
“Đừng chọn B.”

Then another message:

**Ngân:**  
“Tao nghiêm túc.”

---

### A — best conversational opener

**Main:**  
“Bạn đang đọc gì vậy?”

Nghi turns the cover slightly.

**Nghi:**  
“Tài liệu cho bài Triết.”

**Main:**  
“Bạn học trước luôn à?”

**Nghi:**  
“Ừ.”

**Main:**  
“Tôi thường học sau khi deadline đã nhìn thấy tôi.”

Nghi pauses.

Very small smile.

**Nghi:**  
“Nghe không hiệu quả lắm.”

**Main:**  
“Không hiệu quả thật.”

State:

```text
NghiAffinity += 2
NghiComfort += 1
```

---

### B — too direct

**Main:**  
“Hôm nay bạn xinh thật.”

Nghi freezes slightly.

**Nghi:**  
“...Cảm ơn.”

She returns to her book.

State:

```text
NghiAffinity += 1
NghiComfort -= 2
```

---

### C — bluff

**Main:**  
“Tôi cũng đọc nhiều lắm.”

**Nghi:**  
“Bạn hay đọc gì?”

**Main:**  
“...Documentation.”

**Nghi:**  
“Documentation?”

**Main:**  
“Vẫn là chữ.”

Nghi looks away, hiding a small smile.

State:

```text
NghiAffinity += 2
```

---

### D — quiet bonding

Main sits quietly and opens his own laptop/book.

After some time:

**Nghi:**  
“Bạn không định nói gì à?”

**Main:**  
“Tôi sợ làm phiền.”

Nghi looks at him.

**Nghi:**  
“Không sao.”

State:

```text
NghiComfort += 2
NghiAffinity += 1
```

---

## Follow-up conversation

After enough time:

**Nghi:**  
“Bạn thân với Ngân à?”

**Main:**  
“Ừ.”

**Main:**  
“Thân tới mức nó biết tao sắp nói ngu trước cả tao.”

**Nghi:**  
“Có vẻ tiện.”

**Main:**  
“Đôi lúc đáng sợ.”

**Nghi:**  
“Nhưng tốt.”

**Main:**  
“Ừ.”

Small beat.

**Main:**  
“Bạn mới chuyển tới... ổn không?”

Nghi looks toward the window.

**Nghi:**  
“Chưa quen lắm.”

**Main:**  
“Với trường?”

**Nghi:**  
“Với mọi người.”

**Nghi:**  
“Tôi không giỏi bắt chuyện.”

**Main:**  
“Ờ.”

**Main:**  
“Tôi cũng không.”

Nghi looks at him.

**Nghi:**  
“Bạn nói khá nhiều mà.”

**Main:**  
“Đó là do lỗi hệ thống.”

Nghi gives her first clearly visible soft smile.

Use `Nghi_SoftSmile`.

State:

```text
NghiAffinity += 2
NghiComfort += 2
```

---

# CH2_06 — PHYSICAL EDUCATION BOSS FIGHT

**Map:** Sports field — Morning  
**Cast:** Main, Minh, Ngân, Nghi, Thầy Thể Dục

Thầy Thể Dục enters.

**Main:**  
“...Đây là giảng viên?”

**Minh:**  
“Tao nghĩ đây là raid boss.”

**Thầy Thể Dục:**  
“KHỞI ĐỘNG!”

**Main:**  
“Đúng rồi. Boss thật.”

After warmup:

**Thầy Thể Dục:**  
“HÔM NAY CHÚNG TA CHẠY!”

**Main:**  
“Bao nhiêu vòng ạ?”

**Thầy Thể Dục:**  
“ĐẾN KHI NÀO TÔI THẤY Ý CHÍ!”

**Main:**  
“Có option nộp ý chí dạng PDF không thầy?”

**Thầy Thể Dục:**  
“CHẠY!”

Ngân runs past Main.

**Ngân:**  
“Chậm thế?”

**Main:**  
“Tao là Game Developer.”

**Ngân:**  
“Thì?”

**Main:**  
“Class tao không có stamina.”

---

## Sports choice

```text
A. Cố chạy cạnh Nghi.
B. Chạy đúng sức.
C. Cố vượt Nghi để gây ấn tượng.
D. Khi Ngân hụt chân, dừng lại hỏi cô ấy có ổn không.
```

### A
Main struggles but stays near Nghi.

**Nghi:**  
“Bạn ổn chứ?”

**Main:**  
“Rất ổn.”

He clearly is not.

**Nghi:**  
“...Không giống lắm.”

State:

```text
NghiAffinity += 1
```

---

### B
Safe.

State:

```text
NghiComfort += 1
```

---

### C
Main sprints.

**Minh:**  
“Ủa nó chạy đi đâu vậy?”

**Ngân:**  
“Đi gặp tổ tiên.”

Main overexerts.

Set up infirmary scene.

State:

```text
NghiAffinity += 1
NghiComfort -= 1
```

---

### D — Ngân secret route event

Ngân slips slightly / cramps.

Main immediately stops.

**Main:**  
“Ê, ổn không?”

**Ngân:**  
“Ổn.”

**Main:**  
“Chắc chưa?”

**Ngân:**  
“Chắc.”

**Main:**  
“Đi chậm thôi.”

Ngân looks at Main for a second.

**Ngân:**  
“...Ừ.”

State:

```text
NganAffinity += 3
NganSpecialFlags += 1
```

Thầy Thể Dục shouts from far away:

**Thầy Thể Dục:**  
“HAI EM KIA!”

**Main:**  
“Chạy.”

**Ngân:**  
“Chạy.”

---

Regardless of choice, Main eventually overdoes it enough to justify a light infirmary visit. Choice C makes the collapse more dramatic.

---

# CH2_07 — INFIRMARY EVENT

**Map:** Infirmary — Afternoon  
**Cast:** Main, Cô Y Tá, Ngân, Nghi

Main wakes up.

**Main:**  
“...”

**Cô Y Tá:**  
“Em tỉnh rồi à?”

**Main:**  
“Em đang ở thiên đường?”

**Cô Y Tá:**  
“Phòng y tế.”

**Main:**  
“À.”

**Cô Y Tá:**  
“Nếu đây là thiên đường thì cơ sở vật chất hơi thiếu.”

Ngân is nearby.

**Ngân:**  
“Mày chạy có mấy vòng.”

**Main:**  
“Mấy vòng cuối đời.”

Nghi appears at the door.

**Nghi:**  
“Bạn ổn không?”

Main immediately sits straighter.

**Cô Y Tá:**  
“Không cần diễn.”

Main slowly lies back down.

---

## Choice 3 — honesty/comfort test

Show Ngân Hint button.

```text
A. "Ổn. Chỉ hơi xấu hổ thôi."
B. "Chuyện nhỏ."
C. "Tôi cố chạy vì bạn."
D. "Tôi nghĩ thầy thể dục muốn giết tôi."
```

### Hint

If used:

**Ngân (quiet message):**  
“Đừng có flex.”

---

### A — best answer

**Main:**  
“Ổn. Chỉ hơi xấu hổ thôi.”

Nghi softens.

**Nghi:**  
“Không cần xấu hổ.”

**Nghi:**  
“Ít nhất bạn đã cố.”

**Main:**  
“Đừng động viên. Tôi sẽ tưởng mình có năng lực.”

Nghi smiles.

State:

```text
NghiAffinity += 3
NghiComfort += 2
```

---

### B — dishonest bravado

**Main:**  
“Chuyện nhỏ.”

**Cô Y Tá:**  
“Huyết áp lúc nãy tụt.”

Nghi looks at Main.

**Main:**  
“...Chuyện vừa.”

State:

```text
NghiComfort -= 1
```

---

### C — too direct

**Main:**  
“Tôi cố chạy vì bạn.”

Silence.

Nghi is visibly uncomfortable.

**Nghi:**  
“...Bạn không cần làm vậy.”

State:

```text
NghiAffinity += 1
NghiComfort -= 3
```

---

### D — comedy safe

**Main:**  
“Tôi nghĩ thầy thể dục muốn giết tôi.”

**Ngân:**  
“Không.”

**Ngân:**  
“Thầy muốn mày khỏe.”

**Main:**  
“Cách triển khai hơi cực đoan.”

Nghi lightly laughs.

State:

```text
NghiAffinity += 2
NghiComfort += 1
```

---

After Nghi leaves:

**Ngân:**  
“Thấy chưa?”

**Main:**  
“Thấy gì?”

**Ngân:**  
“Người ta tới thăm mày.”

**Main:**  
“Có hi vọng?”

**Ngân:**  
“Có.”

Small pause.

**Ngân:**  
“Nếu mày đừng có ngu.”

Main laughs.

If `NganAffinity >= 4`, give a subtle pause on Ngân's expression before she looks away.

---

# CH2_08 — CONTRADICTIONS

**Map:** Philosophy classroom — Afternoon  
**Cast:** Main, Minh, Ngân, Nghi, Cô Triết

Cô Triết is lecturing.

**Cô Triết:**  
“Con người có thể đồng thời muốn tiến lại gần một người...”

**Cô Triết:**  
“...và sợ bị chính người đó từ chối hay không?”

Main slowly looks up.

Minh slowly turns toward Main.

Ngân also turns toward Main.

Main notices both staring.

**Main:**  
“Gì?”

**Minh:**  
“Không có gì.”

**Ngân:**  
“Không có gì hết.”

Cô Triết looks directly at Main.

**Cô Triết:**  
“Em kia.”

**Main:**  
“Dạ?”

**Cô Triết:**  
“Có vẻ em hiểu ví dụ.”

**Main:**  
“Em xin quyền không phát biểu.”

**Cô Triết:**  
“Không được.”

Class laughs.

Then Cô Triết becomes more serious.

**Cô Triết:**  
“Mâu thuẫn không phải lúc nào cũng cần bị loại bỏ.”

**Cô Triết:**  
“Đôi khi chính mâu thuẫn buộc con người phải lựa chọn.”

**Cô Triết:**  
“Và lựa chọn khiến con người thay đổi.”

This line should be allowed to land without a joke immediately after it.

Nghi quietly glances at Main.

---

# CH2_09 — AFTER-SCHOOL QUIET

**Map:** Library — Evening OR Courtyard — Afternoon  
**Cast:** Main, Nghi

Main and Nghi are alone again.

**Main:**  
“Mọi người hay nghĩ bạn khó gần à?”

Nghi looks at him.

**Nghi:**  
“Có.”

**Main:**  
“Ban đầu tôi cũng nghĩ vậy.”

Nghi expression becomes slightly guarded.

**Main:**  
“Nhưng giờ thì không.”

**Nghi:**  
“Vì sao?”

---

## Choice 4

```text
A. "Chắc bạn chỉ không biết phải nói gì thôi."
B. "Tôi thấy bạn bình thường mà."
C. "Vì bạn dễ thương."
D. "Tôi quen rồi."
```

### A — best comfort answer

**Main:**  
“Chắc bạn chỉ không biết phải nói gì thôi.”

Nghi is surprised.

**Nghi:**  
“...Có lẽ.”

**Main:**  
“Tôi hiểu cảm giác đó.”

**Nghi:**  
“Bạn?”

**Main:**  
“Tôi chỉ giỏi nói linh tinh.”

Nghi smiles.

State:

```text
NghiAffinity += 2
NghiComfort += 3
```

---

### B

**Main:**  
“Tôi thấy bạn bình thường mà.”

**Nghi:**  
“Bình thường?”

**Main:**  
“Ý tốt.”

**Nghi:**  
“...Cảm ơn.”

State:

```text
NghiAffinity += 2
NghiComfort += 1
```

---

### C

**Main:**  
“Vì bạn dễ thương.”

Nghi blushes slightly but looks away.

**Nghi:**  
“...Bạn nói thẳng thật.”

State:

```text
NghiAffinity += 2
NghiComfort -= 1
```

---

### D

**Main:**  
“Tôi quen rồi.”

**Nghi:**  
“Nghe như tôi là lỗi phần mềm.”

**Main:**  
“Không, không phải ý đó.”

Small awkward silence.

No bonus.

---

# CH2_10 — NGÂN CHARACTER EVENT

**Map:** Canteen / vending machine / hallway — Afternoon  
**Cast:** Main, Ngân

This scene is very important for the secret route.

Ngân hands Main a drink.

**Main:**  
“Cho tao?”

**Ngân:**  
“Ừ.”

**Main:**  
“Sao tốt vậy?”

**Ngân:**  
“Vì mày đứng nhìn máy bán nước hai phút rồi vẫn chưa mua.”

**Main:**  
“Tao đang suy nghĩ.”

**Ngân:**  
“Mày uống đúng một loại suốt hai năm.”

**Main:**  
“...”

**Ngân:**  
“Đừng có giả bộ phức tạp.”

Main takes it.

**Main:**  
“Cảm ơn.”

They sit.

**Main:**  
“Mày nghĩ tao có cơ hội không?”

Ngân knows exactly who he means.

**Ngân:**  
“Có chứ.”

Small pause.

**Ngân:**  
“Nếu mày đừng có ngu.”

Main laughs.

**Main:**  
“Câu signature của mày à?”

**Ngân:**  
“Ừ.”

A quieter moment.

**Main:**  
“Cảm ơn thật.”

**Ngân:**  
“Vì?”

**Main:**  
“Bữa giờ giúp tao.”

Ngân looks away.

---

## Secret route choice

```text
A. "Mày đúng là best wingman."
B. "Không có mày chắc tao chết."
C. "Mà... dạo này tao toàn nói chuyện với mày về Nghi."
D. "Mai giúp tao tiếp nha."
```

### A
**Ngân:**  
“Biết vậy trả lương đi.”

Small affinity.

```text
NganAffinity += 1
```

### B
**Ngân:**  
“Dramatic vừa thôi.”

```text
NganAffinity += 1
```

### C — secret route flag

**Main:**  
“Mà... dạo này tao toàn nói chuyện với mày về Nghi.”

Ngân looks at him.

**Ngân:**  
“Thì?”

**Main:**  
“Không biết.”

**Main:**  
“Tự nhiên thấy hơi vô duyên.”

Ngân is surprised.

**Ngân:**  
“...”

**Ngân:**  
“Biết nghĩ vậy là tiến bộ rồi.”

Main laughs.

**Main:**  
“Mai tao bao nước.”

Ngân softens.

**Ngân:**  
“Nhớ đó.”

State:

```text
NganAffinity += 3
NganSpecialFlags += 1
```

### D
No secret bonus.

---

# CH2_11 — THE QUESTION

**Map:** Rooftop — Afternoon  
**Cast:** Main, Ngân

Main is visibly nervous.

**Main:**  
“Tao định nói.”

**Ngân:**  
“Nói gì?”

**Main:**  
“Tỏ tình.”

Ngân pauses.

**Ngân:**  
“Hôm nay?”

**Main:**  
“Ừ.”

Ngân looks over the rooftop.

**Ngân:**  
“...Ừ.”

**Main:**  
“‘Ừ’ là sao?”

**Ngân:**  
“Thì đi nói đi.”

**Main:**  
“Cho tao lời khuyên.”

Ngân takes a breath.

If hints remain, do NOT consume one automatically.

**Ngân:**  
“Đừng cố nói câu gì hay.”

**Main:**  
“Hả?”

**Ngân:**  
“Nói thật thôi.”

This is the strongest advice in Chapter 2.

If `NganAffinity >= 7`, show a slightly sad / mixed expression for a brief beat before returning to normal.

---

## Secret branch availability

If:

```text
NganAffinity >= 10
NganSpecialFlags >= 3
NganHintsUsed <= 1
```

prepare hidden flag:

```text
NganEndingAvailable = true
```

Do not reveal this to player yet.

---

# CH2_12 — FINAL CONFESSION SETUP

**Map:** Rooftop — Sunset  
**Cast:** Main, Nghi

Nghi arrives.

**Nghi:**  
“Bạn gọi tôi?”

**Main:**  
“Ừ.”

**Nghi:**  
“Có chuyện gì sao?”

Main hesitates.

Optional final Ngân Hint button appears only if hints remain.

If pressed:

**Ngân (scheduled/previous message):**  
“Đừng cố nói câu gì hay.”

**Ngân:**  
“Nói thật thôi.”

Consume one hint normally.

---

# 10. GOOD ENDING — NGHI

## Requirements

Recommended thresholds:

```text
NghiAffinity >= 12
NghiComfort >= 8
```

And player must choose the sincere confession:

```text
"Tôi thích bạn."
```

If the repository uses normalized or different ranges, preserve the intent and rebalance logically.

---

## Good Ending Dialogue

**Main:**  
“Nghi.”

**Nghi:**  
“Ừ?”

**Main:**  
“Tôi không giỏi nói mấy chuyện này.”

**Main:**  
“Thật ra là... cực kỳ không giỏi.”

Nghi quietly waits.

**Main:**  
“Nhưng tôi thích bạn.”

Silence.

Main starts panicking.

**Main:**  
“Nếu bạn cần thời gian thì—”

**Nghi:**  
“Tôi biết.”

Main freezes.

**Main:**  
“...Hả?”

Nghi uses `Nghi_HappySmile`.

**Nghi:**  
“Không khó đoán lắm.”

**Main:**  
“Thế sao bạn không nói?”

**Nghi:**  
“Tôi muốn xem bao giờ bạn tự nói.”

**Main:**  
“...”

**Main:**  
“Tôi bị test à?”

Nghi gives a small closed-mouth smile.

**Nghi:**  
“Có thể.”

Main visibly blushes.

**Main:**  
“Vậy...”

**Main:**  
“Câu trả lời là?”

Nghi looks at him.

**Nghi:**  
“Ừ.”

Main's brain stops.

**Main:**  
“‘Ừ’?”

**Nghi:**  
“Tôi cũng thích bạn.”

Pause.

Main looks absurdly happy but still embarrassed.

Nghi gives a gentle smile.

**Nghi:**  
“Cuối tuần này...”

**Nghi:**  
“Bạn có rảnh không?”

**Main:**  
“RẢNH.”

Nghi raises an eyebrow.

**Nghi:**  
“Tôi còn chưa nói đi đâu.”

**Main:**  
“Đi đâu cũng rảnh.”

Nghi laughs softly.

Fade to Good Ending CG:

- sunset rooftop,
- Main visibly shy and delighted,
- Nghi accepts with a gentle closed-mouth smile,
- corrected straight rooftop railing,
- both characters framed warmly.

Ending card:

```text
GOOD ENDING
LOVE PROTOCOL ESTABLISHED
```

### Post-credit tease

Nghi checks her phone.

Message from Ngân:

**Ngân:**  
“Sao rồi?”

Nghi types:

**Nghi:**  
“Ổn.”

Ngân sends:

```text
👍
```

Ngân looks at the screen for a moment.

Fade out.

Text:

```text
TO BE CONTINUED IN CHAPTER 3
```

---

# 11. BAD ENDING — 404 LOVE NOT FOUND

## Trigger

If the player reaches the confession but fails the Good Ending requirement:

```text
NghiAffinity < 12
OR
NghiComfort < 8
```

Or chooses an overly performative / selfish final confession option.

---

## Bad Ending Dialogue

**Main:**  
“Nghi.”

**Nghi:**  
“Ừ?”

**Main:**  
“Tôi thích bạn.”

Nghi becomes visibly sad.

Use `Nghi_Sad`.

Long pause.

**Nghi:**  
“Xin lỗi.”

Main does not immediately respond.

**Nghi:**  
“Tôi thật sự quý bạn.”

**Nghi:**  
“Nhưng tôi không nghĩ mình có thể trả lời bạn theo cách bạn mong muốn.”

Main forces a small smile.

**Main:**  
“Ừ.”

**Main:**  
“Không sao.”

Nghi looks even more apologetic.

**Nghi:**  
“...Xin lỗi.”

**Main:**  
“Thật mà.”

Cut before overexplaining.

---

## Bad Ending Scene 2

**Map:** NearbyPub_Night  
**Cast:** Main, Minh

Main and Minh sit at a table.

**Minh:**  
“Uống đi.”

**Main:**  
“Tình yêu là gì?”

**Minh:**  
“Tao không biết.”

**Main:**  
“Cuộc đời là gì?”

**Minh:**  
“Tao càng không biết.”

**Main:**  
“Mày biết gì?”

**Minh:**  
“Mai có deadline.”

Long silence.

**Main:**  
“Cho tao thêm chai.”

**Minh:**  
“Ờ.”

Ending card:

```text
BAD ENDING
404 — LOVE NOT FOUND
```

Return to Ending Menu / Chapter Select.

---

# 12. EASTER EGG ENDING — NGÂN

## Intent

This is not a joke-only ending.

It should feel surprising but earned.

The player gradually realizes:

> While Main spent the whole chapter trying to approach Nghi, Ngân was the person constantly beside him.

This ending must terminate the future route.

After completion:

```text
game_route_complete = true
chapter3_route_locked_for_this_save = true
ending_ngan_unlocked = true
```

The player can still use Chapter Select/new save to explore other routes.

---

## Recommended requirements

```text
NganAffinity >= 10
NganSpecialFlags >= 3
NganHintsUsed <= 1
```

Required special events should include at least three of:

- complimenting Ngân in `CH2_01`,
- helping Ngân during PE,
- choosing the self-aware vending machine dialogue,
- one additional hidden supportive choice if implemented.

---

## Secret branch

Before going to confess to Nghi, Ngân asks:

**Ngân:**  
“Đi tỏ tình à?”

**Main:**  
“Ừ.”

Ngân smiles.

**Ngân:**  
“Good luck.”

Ngân turns to leave.

If `NganEndingAvailable == true`, display special choice:

```text
[Gọi Ngân lại.]
```

It should visually look slightly different from normal choices, but not reveal the ending.

---

## Easter Egg Dialogue

Main:

**Main:**  
“Ngân.”

Ngân turns.

**Ngân:**  
“Hử?”

Main hesitates.

**Main:**  
“Tao nghĩ tao vừa nhận ra một chuyện.”

**Ngân:**  
“Chuyện gì?”

**Main:**  
“Bữa giờ tao cứ nghĩ tao đang chạy theo Nghi.”

Ngân becomes confused.

**Ngân:**  
“Ừ?”

**Main:**  
“Nhưng người tao muốn kể chuyện mỗi ngày...”

Pause.

**Main:**  
“Người tao tự nhiên tìm đầu tiên mỗi khi có chuyện...”

Ngân's smile fades into nervous confusion.

**Main:**  
“Hình như không phải Nghi.”

Use `Ngan_Confused`.

**Ngân:**  
“...Mày đang nói gì vậy?”

Main takes a breath.

**Main:**  
“Tao thích mày.”

Silence.

Switch to `Ngan_Embarrassed`.

**Ngân:**  
“...”

**Main:**  
“...”

**Ngân:**  
“...”

**Ngân:**  
“ĐM.”

Main blinks.

**Main:**  
“Đấy không phải response tao mong đợi.”

Ngân is bright red.

**Ngân:**  
“Mày cho tao thời gian load được không?!”

**Main:**  
“Xin lỗi.”

**Ngân:**  
“Đồ ngu.”

Main looks worried.

Then Ngân smiles.

**Ngân:**  
“...Nhưng tao cũng thích mày.”

Main freezes.

**Main:**  
“Thật?”

**Ngân:**  
“Không.”

Main's face falls instantly.

Ngân bursts out laughing.

**Ngân:**  
“Đùa thôi!”

**Main:**  
“Ngân!”

Use `Ngan_BigLaugh`.

**Ngân:**  
“Đi.”

**Main:**  
“Đi đâu?”

Ngân grabs his hand.

**Ngân:**  
“Đi chơi.”

**Main:**  
“Bây giờ?”

**Ngân:**  
“Bây giờ.”

**Main:**  
“Tao còn balo—”

**Ngân:**  
“Có tay còn lại.”

Ngân drags him away.

Transition to Easter Egg ending CG:

- school gate,
- Ngân pulling Main by the hand,
- Ngân ecstatic as if she just won the lottery,
- Main happily dragged behind her with a goofy/troll expression,
- high-energy daylight,
- comedic romantic framing.

Ending card:

```text
SECRET ENDING
YOU WERE NEVER LOST
```

Optional subtitle:

```text
"Some escape routes don't lead outside.
Sometimes they lead home."
```

Then:

```text
ROUTE COMPLETE
```

Do not continue to Chapter 3 on this save.

---

# 13. EXTRA OPTIONAL DIALOGUE MICRO-EVENTS

These are small optional interactions that improve pacing and help the cast feel alive.

## 13.1 Minh notices Main's crush

**Minh:**  
“Mày nhìn người ta lần thứ mấy rồi?”

**Main:**  
“Tao đang quan sát môi trường.”

**Minh:**  
“Môi trường tóc vàng à?”

---

## 13.2 Ngân catches Main rehearsing

**Main:**  
“Chào Nghi, hôm nay—”

**Ngân:**  
“Không.”

**Main:**  
“Cái gì?”

**Ngân:**  
“Nghe như NPC.”

---

## 13.3 Nghi sees Main coding

**Nghi:**  
“Bạn đang làm gì vậy?”

**Main:**  
“Fix bug.”

**Nghi:**  
“Khó không?”

**Main:**  
“Bug không khó.”

**Main:**  
“Không biết bug ở đâu mới khó.”

**Nghi:**  
“Nghe giống nhiều chuyện khác.”

Main looks at her.

**Main:**  
“...Sao tự nhiên sâu vậy?”

---

## 13.4 Cô Triết catches another whisper

**Cô Triết:**  
“Bạn cuối lớp.”

**Main:**  
“Dạ?”

**Cô Triết:**  
“Nếu chuyện của em hay hơn bài giảng, mời em lên đây giảng.”

**Main:**  
“Dạ bài cô hay hơn.”

**Cô Triết:**  
“Cô biết.”

---

## 13.5 Nurse callback

**Cô Y Tá:**  
“Lần sau đừng cố chứng minh bản thân bằng cách ngất.”

**Main:**  
“Em ghi nhận.”

**Cô Y Tá:**  
“Em nói câu đó như chuẩn bị làm lại.”

---

# 14. CHOICE / STAT BALANCING TARGET

The exact numbers may be adapted to the existing engine, but the route should be balanced around the following principle.

## Nghi route maximum approximately

```text
NghiAffinity possible total: ~18–20
NghiComfort possible total: ~12–14
```

Good Ending target:

```text
NghiAffinity >= 12
NghiComfort >= 8
```

This means:
- a player can make a few mistakes,
- one bad choice does not permanently destroy the route,
- repeated boundary-pushing does.

## Ngân route

Target:

```text
NganAffinity >= 10
NganSpecialFlags >= 3
NganHintsUsed <= 1
```

The route should feel hidden but discoverable.

---

# 15. SAVE DATA REQUIREMENTS

Chapter 2 state must be serializable.

Persist at minimum:

```text
chapter2_unlocked
chapter2_started
chapter2_completed

NghiAffinity
NghiComfort

NganAffinity
NganSpecialFlags
NganHintsRemaining
NganHintsUsed

NganEndingAvailable

chapter2_ending
ending_nghi_good_unlocked
ending_nghi_bad_unlocked
ending_ngan_unlocked

game_route_complete
chapter3_route_locked_for_this_save
```

If the existing save schema supports versioning, bump save version safely and provide backward-compatible defaults.

Older Chapter 1 saves should load without errors.

---

# 16. UI REQUIREMENTS

## 16.1 Hint button

Only show the Ngân hint button on marked eligible choices.

Example:

```text
┌─────────────────────────────────┐
│ A. ...                          │
│ B. ...                          │
│ C. ...                          │
│ D. ...                          │
│                                 │
│ 💡 Hỏi Ngân (2/3)              │
└─────────────────────────────────┘
```

Do not show it when:

```text
NganHintsRemaining == 0
```

If the player uses the final hint, remove/disable the button for the rest of Chapter 2.

## 16.2 Speaker focus

Use the dim/back system specified in Section 3.

## 16.3 Ending presentation

Each ending should show:

- ending CG if available,
- ending title,
- save/unlock state update,
- Return to Menu,
- Chapter Select,
- optionally Retry from Last Major Choice if the game already supports it.

---

# 17. ENDING CG MAPPING

Use existing CG assets if present.

## Good Ending CG
Scene:
- Nghi + Main on rooftop at sunset.
- Nghi uses a gentle **closed-mouth smile**.
- Main is embarrassed and delighted.
- Rooftop railing must be visually straight and structurally correct.
- Romantic warm sunset.

## Easter Egg Ending CG
Scene:
- school gate,
- daytime,
- Ngân excitedly pulling Main by the hand,
- Ngân looks extremely happy,
- Main looks happy but comedically overwhelmed,
- strong motion and playful energy.

## Bad Ending
Use `NearbyPub_Night` background with sprites unless a dedicated CG already exists.

---

# 18. AUDIO / PRESENTATION GUIDELINES

Do not invent filenames blindly.

Search existing audio folders and reuse fitting tracks.

Suggested moods:

```text
CH2_00     light comedy
CH2_02     classroom / neutral
Nghi scenes soft calm track
Ngân scenes bright playful track
Infirmary  light quiet comedy
CH2_08     reflective / restrained
Confession gentle emotional track
Bad End    subdued comedy-sad
Ngân End   energetic romantic-comedy
```

Use silence deliberately before:
- confession responses,
- Nghi's refusal,
- Main's realization about Ngân.

Avoid melodrama.

---

# 19. WRITING DIRECTION

The writing style must remain:

- natural Vietnamese student conversation,
- meme-aware,
- not overloaded with memes,
- emotionally sincere when necessary,
- never stiff,
- never overly literary,
- characters should sound distinct.

## Main
- IT/Game Dev brain.
- Zero romantic experience.
- Sometimes accidentally funny because he thinks socially awkward statements are logical.

## Minh
- dry best-friend commentary.

## Ngân
- fast, teasing, emotionally perceptive.

## Nghi
- short sentences,
- restrained,
- gradually warmer.

## Cô Triết
- concise,
- sharp,
- intellectually confident.

## Cô Y Tá
- deadpan.

## Thầy Thể Dục
- loud and energetic, but not stupid.

---

# 20. ENGINE IMPLEMENTATION GUIDANCE

Adapt this to the current project.

Preferred architecture if compatible:

```text
Chapter2Controller
Chapter2State
DialogueSequence / DialogueData
ChoiceNode
CharacterStageController
AffinityService
HintService
EndingResolver
```

However:

> **Do not create these classes if equivalent systems already exist.**

Reuse current game systems first.

A route resolver can conceptually be:

```pseudo
if NganEndingAvailable and player_selects_call_ngan_back:
    trigger NganSecretEnding

else if NghiAffinity >= GOOD_AFFINITY
     and NghiComfort >= GOOD_COMFORT
     and sincere_confession_selected:
    trigger NghiGoodEnding

else:
    trigger NghiBadEnding
```

---

# 21. TESTING CHECKLIST

The implementation is not complete until these tests pass.

## Chapter unlock

- [ ] New player cannot access Chapter 2.
- [ ] Chapter 1 Bad Ending does not unlock Chapter 2.
- [ ] Chapter 1 Good Ending unlocks Chapter 2.
- [ ] Unlock persists after restart.
- [ ] Chapter 2 can start immediately after Chapter 1.
- [ ] Chapter 2 can start from Chapter Select.

## Save/load

- [ ] Save during Chapter 2 restores exact scene.
- [ ] Affinity variables restore correctly.
- [ ] Hint count restores correctly.
- [ ] Old Chapter 1 saves still load.

## Hint system

- [ ] Starts at 3.
- [ ] Only appears on marked choices.
- [ ] Each use permanently subtracts one.
- [ ] Never becomes negative.
- [ ] Zero hints hides/disables hint UI.
- [ ] Hint does not automatically choose an answer.
- [ ] Hints used affect Ngân secret route correctly.

## Character presentation

- [ ] Non-speakers remain visible if physically present.
- [ ] Non-speakers are dimmed and visually pushed back.
- [ ] Current speaker becomes full brightness and foreground.
- [ ] Characters only disappear when actually leaving.

## Good Ending

- [ ] Correct affinity/comfort route reaches Nghi Good Ending.
- [ ] Good Ending CG is shown.
- [ ] Nghi has closed-mouth smile.
- [ ] Chapter 3 tease is shown.

## Bad Ending

- [ ] Low relationship state causes Nghi refusal.
- [ ] Nghi is sad, not cruel.
- [ ] Pub scene with Minh plays.
- [ ] “404 — LOVE NOT FOUND” ending appears.

## Ngân Easter Egg Ending

- [ ] Hidden route requirements work.
- [ ] Special `[Gọi Ngân lại.]` choice only appears when eligible.
- [ ] Ngân confession scene plays.
- [ ] School-gate hand-pull CG appears.
- [ ] This save is marked as full route complete.
- [ ] Chapter 3 does not automatically continue from this ending.

---

# 22. ACCEPTANCE CRITERIA

The task is complete only when:

1. Chapter 1 is still fully functional.
2. Chapter 2 unlock behavior works.
3. Chapter Select works.
4. All new characters appear correctly.
5. All requested new backgrounds are integrated.
6. Speaker focus behavior uses dim/back positioning, not literal hide/show.
7. Ngân hint system works with exactly 3 total uses.
8. NghiAffinity and NghiComfort affect the ending.
9. Ngân's hidden relationship path works.
10. All three endings are reachable.
11. Dialogue feels natural and matches the supplied script.
12. Good Ending transitions toward Chapter 3.
13. Easter Egg Ending terminates the current route.
14. Save/load works safely.
15. No critical errors or regressions remain.

---

# 23. FINAL AGENT RESPONSE FORMAT

After implementation, report:

```text
1. Files created
2. Files modified
3. New state variables
4. New scenes
5. New UI components
6. Ending logic
7. Asset mappings used
8. Tests performed
9. Any missing assets or assumptions
10. Known issues, if any
```

Do not simply say “done”.

Provide enough technical detail that another developer can audit the changes.

---

# END OF CHAPTER 2 IMPLEMENTATION BRIEF
