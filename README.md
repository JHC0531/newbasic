# 🦝 Verb Form Learner — Regular Past Tense (`-ed`)

An interactive web app that helps Korean middle-school students master the **regular past tense** — the four `-ed` spelling rules **and** the three `-ed` pronunciations (`/t/`, `/d/`, `/ɪd/`) — through diagnosis, explanation, listening, games, and homework.

🔗 **Live app:** https://newbasic.streamlit.app/
🛠️ **Built with:** Streamlit · Python · Google Sheets · Browser TTS

---

## 🏫 Teaching Context

### Who are your learners?
First-year middle-school students (Grade 7) at a Korean public school. They are **EFL learners** whose first language is Korean, in a **mixed-ability class** ranging from lower to higher proficiency.

### What is your classroom environment?
A regular English classroom with **1:1 devices** (tablets or phones) or a shared projector screen, connected to Wi-Fi. The app runs in any browser — no installation needed.

### What challenges do learners have?
- The past tense is **memorization-heavy**, and motivation drops quickly.
- A **single pace** doesn't fit a mixed-ability class — fast learners get bored, slower learners fall behind.
- The `-ed` ending has **three different pronunciations** (`/t/`, `/d/`, `/ɪd/`) that learners easily overlook (e.g. *liked*, *played*, *wanted*).
- Teachers can't give **instant, individual feedback** to every student at once.

---

## 🎯 Lesson Purpose

### What does this lesson teach?
The **regular past tense of English verbs**:
- The four `-ed` **spelling rules** (add `-ed`; consonant+`e` → `-d`; `-y` rules; double the final consonant)
- The three `-ed` **pronunciations** — `/t/` after voiceless sounds (liked), `/d/` after voiced sounds (played), `/ɪd/` after t/d (wanted)

### Why is this lesson meaningful?
The past tense is a **core building block** for everyday communication. Spelling alone isn't enough — without the pronunciation distinction, students mispronounce common verbs. Turning rote drills into **interactive practice with instant feedback** makes a dry but essential topic engaging.

---

## 💡 App Purpose

### Why did you build this app?
To replace passive worksheet drills with an **active, self-paced tool**. Students can hear pronunciation, get immediate corrective feedback, diagnose their own weak points, and compete in games — none of which a paper handout offers.

### What learning need does it address?
- **Self-paced practice** for a mixed-ability class
- **Instant feedback** that explains *why* an answer is wrong, freeing the teacher to circulate
- **Pronunciation support** for the often-ignored `-ed` sounds
- **Self-diagnosis** so learners know which rule or sound to review
- **Motivation** through games and a class-wide leaderboard

---

## 🧩 App Design

### How does it work?
The **Regular Change** page is organized into **7 tabs**, with a raccoon "teacher" guiding learners throughout:

| Tab | What it does |
|-----|--------------|
| **🩺 Diagnostic** | 10 mixed questions (pronunciation + rule application). At the end, the raccoon gives a **study prescription**: ✅ rules you know / 📌 rules to review / 🔊 sounds to re-listen |
| **1️⃣ base + -ed** | Rule explanation + card-style mini-quiz with instant feedback |
| **2️⃣ consonant + e → -d** | Rule explanation + mini-quiz |
| **3️⃣ -y rules** | Rule explanation + mini-quiz |
| **4️⃣ short vowel + consonant** | Rule explanation + mini-quiz |
| **🐦 Bird-Catching Game** | Timed (60 s) game — click the bird carrying the correct past form; **class leaderboard** |
| **📒 HOMEWORK** | 10 questions (5 pronunciation + 5 three-form), per-question feedback, and a downloadable **completion certificate** image |

**The pronunciation question** is the app's signature feature: a word card (e.g. `walked`) appears with **three speaker buttons**. Each plays a different `-ed` sound (`walkt` /t/, `walkd` /d/, `walkid` /ɪd/) using text-to-speech. Students listen to all three and choose the correct pronunciation.

### What data or content does it use?
- **~40 regular verbs** curated for the lesson, each tagged with its spelling rule and `-ed` sound (≈19 `/d/`, 12 `/t/`, 8 `/ɪd/`)
- **30 mini-quiz items** with attractive distractors (common mistakes like *goed*, *studyed*)
- **Browser text-to-speech (TTS)** for pronunciation — no audio files needed
- **Google Sheets** as a lightweight database for the class leaderboard (separate rankings for regular vs. irregular games)

### How do learners interact with it?
Learners tap tabs, press 🔊 to compare sounds, choose answer cards, type responses, and play games. Feedback (correct/incorrect **with the rule or sound explained**) appears instantly. Game scores save to a shared class ranking, and finishing the homework produces a personal certificate.

---

## 🪧 Classroom Use

### How is the app used in the lesson?
The app bookends the lesson (teacher-led explanation in the middle):
- **Warm-up:** the **Diagnostic tab** acts as a pre-assessment — its prescription tells both student and teacher what to focus on.
- **Wrap-up:** the **mini-quizzes** and **bird game** provide practice and formative assessment, each at the learner's own pace.
- **Homework:** the **HOMEWORK tab** (pronunciation + three-form) is assigned for independent review, ending with a completion certificate.

### What does it improve?
- **Engagement** — games, a mascot, and certificates make practice fun
- **Differentiation** — each learner works at their own level and pace
- **Pronunciation awareness** — the three `-ed` sounds become explicit and audible
- **Feedback efficiency** — the app explains every mistake, so the teacher focuses on individuals
- **Self-direction** — the diagnostic and homework support independent review

---

## ⚠️ Limitations

- **TTS quality varies** by browser/device, and the fake spellings (walkt/walkd/walkid) used to force the three sounds can sound unnatural — best verified in the actual classroom.
- The leaderboard score is **registered after the game** (auto-send with a manual backup), so it relies on honest input in a supervised setting.
- Content is **curated, not adaptive** — the verb set and questions are fixed.
- Requires **internet** and a device per student (or a shared screen).
- Pronunciation is currently **recognition only** (listen-and-choose), not speaking practice.

---

## 🚀 Future Development

- [ ] Replace TTS fake spellings with **recorded native-speaker audio** for clearer `-ed` sounds
- [ ] Add **speaking practice** (record and compare the learner's own pronunciation)
- [ ] Make the leaderboard **fully automatic** (direct score capture)
- [ ] Add **adaptive difficulty** that responds to each learner's mistakes
- [ ] Provide a **teacher dashboard** to track class progress and homework completion
- [ ] Support **offline / installable (PWA)** use for low-connectivity classrooms

