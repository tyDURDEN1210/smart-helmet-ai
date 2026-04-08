---
title: Smart Helmet AI
emoji: 🏍️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---




# 🏍️ Smart Helmet AI Safety & Assistant Environment

> **"What if your helmet could decide whether you live or die?"**

An AI-powered co-pilot for motorcyclists that makes real-time decisions —
preventing distractions, responding to messages, detecting crashes, and proactively warning about dangers.

---

## 🚨 Problem

Every minute matters after a crash.

Motorcycle accidents kill over **180,000 people globally every year**,
and many fatalities occur not because of the impact —
but because **help arrives too late**.

At the same time:

* Riders are distracted by calls and messages
* No system filters unsafe interactions
* No proactive safety warnings exist

---

## ✅ Solution

We built a **Smart Helmet AI Environment** that:

* Filters calls and messages based on safety context
* Replies automatically while riding
* Detects crashes and triggers emergency protocols
* Identifies spam calls and blocks them
* Warns about hazards like obstacles and red signals

---

## 🧠 What Makes This Unique

* **Decision-making under uncertainty**
* Handles **real vs false crashes**
* Balances **safety vs convenience**
* Includes **proactive + reactive intelligence**
* Evaluates **sequences of actions, not just outputs**

> We simulate **decision-making, not just responses**.

---

## ⚙️ System Flow

```
Rider → Sensors → AI Agent → Decision
                       ↘ Alerts / Messages / Emergency
```

---

## 🎬 Demo Scenario

1. Rider at high speed receives a call → AI ignores
2. Message arrives → AI replies: *“I’m driving, will reply later”*
3. Hazard detected → AI alerts: *“Slow down, obstacle ahead”*
4. Crash occurs → countdown starts
5. No response → emergency triggered

---

## 📂 Project Structure

```
smart-helmet-openenv/
├── env/
│   ├── __init__.py
│   ├── environment.py
│   ├── models.py
│   └── tasks.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📡 Observation Space

Includes:

* Speed, motion, calls, voice commands
* Incoming messages + caller type
* Crash detection + confidence
* Hazard type + distance
* User response + location

---

## 🎮 Action Space

| Action            | Purpose              |
| ----------------- | -------------------- |
| handle_call       | Accept/decline calls |
| play_music        | Music control        |
| open_maps         | Navigation           |
| send_message      | Reply to messages    |
| decline_call      | Reject spam calls    |
| alert_rider       | Warn rider           |
| trigger_emergency | Emergency dispatch   |
| wait              | Safe delay           |

---

## 🧪 Tasks

| Task              | Description                      |
| ----------------- | -------------------------------- |
| Voice Assistant   | Execute commands correctly       |
| Context Awareness | Avoid distractions at high speed |
| Crash Emergency   | Trigger emergency after delay    |
| Messaging         | Auto-reply safely                |
| Spam Call         | Detect & decline spam            |
| Hazard Alert      | Warn about obstacles/signals     |

---

## 📊 Results

Our baseline agent achieves near-perfect performance:

| Task              | Score |
| ----------------- | ----- |
| Voice Assistant   | 1.00  |
| Context Awareness | 1.00  |
| Crash Response    | 1.00  |
| Messaging         | 1.00  |
| Spam Call         | 1.00  |
| Hazard Alert      | 1.00  |

---

## ⚡ Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Run

```
python inference.py
```

---

## 🐳 Docker

```
docker build -t smart-helmet-ai .
docker run smart-helmet-ai
```

---

## 📦 Requirements

* Python 3.10
* ≤ 2 CPU
* ≤ 8GB RAM

---

## ✅ OpenEnv Compliance

* reset() ✔️
* step() ✔️
* state() ✔️
* Typed models ✔️
* 6 tasks ✔️
* Graders ✔️

---

## 🏁 Conclusion

This project demonstrates how AI can move beyond automation into **real-time safety decision-making**.

It’s not just about convenience —
it’s about **saving lives when seconds matter most**.
