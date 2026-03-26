# 🎓 EduBot – Institute FAQ Chatbot

EduBot is a rule-based FAQ chatbot built for the **Even Semester Hack-O-Week** project. It answers common institute questions about fees, exams, hostel, timings, and admissions. The project is built progressively across **10 weeks**, each adding a new feature on top of the previous one.

---

## 📁 Project Files

```
edubot/
├── chatbot.py        # Terminal version (Week 1–10)
├── chatbot_gui.py    # GUI version with popup chat window (Week 1–10)
└── README.md
```

---

## ▶️ How to Run

### GUI Version (Chat Window Popup)
```bash
python chatbot_gui.py
```
A chat window will open. Type your question and press **Enter** or click **Send**.

### Terminal Version
```bash
python chatbot.py
```
Chat directly in the terminal.

> **No pip install needed.** Only built-in Python libraries are used (`tkinter`, `math`, `re`, `string`).

---

## 🛠️ Requirements

- Python 3.x
- No external libraries

---

## 📅 Weekly Features (All 10 Weeks)

| Week | Feature | Description |
|------|---------|-------------|
| 1 | Basic FAQ Responder | 15 hardcoded Q&A pairs covering fees, timings, exams, hostel, contacts |
| 2 | Text Preprocessing | Lowercasing, punctuation removal, tokenization, stopword removal, typo fix |
| 3 | Synonym Expansion | Maps "tuition", "payment", "cost" → fees; synonym dictionary for 10 topics |
| 4 | TF-IDF Retrieval | Scores every FAQ against user query; picks the best match |
| 5 | Intent Classification | Detects intent: fees / exams / timetable / hostel / admissions / contacts |
| 6 | Entity Extraction | Extracts semester number, year, date from user input using regex |
| 7 | Context Follow-ups | "Tell me more" continues previous topic without re-asking |
| 8 | Fallback & Handover | Unclear queries get a fallback reply + human advisor contact |
| 9 | Multichannel Info | Type "channels" to see Web / App / WhatsApp / ERP options |
| 10 | Analytics | Type "stats" to see total queries, matches, fallbacks, intents |

---

## 💬 Sample Questions to Try

```
What are the fees?
hostel charges
sem 5 exam date
payment info          → synonym for fees
tell me more          → follow-up (Week 7)
channels              → multichannel info (Week 9)
stats                 → analytics report (Week 10)
```

---

## 🖥️ GUI Preview

- **Blue text** = your messages  
- **Green text** = bot replies  
- Press **Enter** or click **Send** to chat  
- Click **Clear** to reset the conversation  

---

## 📊 How It Works (Simple Flow)

```
User types question
        ↓
Preprocess (lowercase, remove stopwords)
        ↓
Expand synonyms
        ↓
Classify intent
        ↓
Extract entities (SEM number, date, year)
        ↓
TF-IDF match against FAQ database
        ↓
Found? → Show answer
Not found? → Fallback + human advisor contact
```

---

## 👨‍💻 Built With

- Python 3
- Tkinter (GUI)
- No external libraries

---

## 📌 Note

This project was made as part of the **Even Semester Hack-O-Week** college assignment. Each week builds on the previous one, ending in a complete FAQ chatbot with a GUI.
