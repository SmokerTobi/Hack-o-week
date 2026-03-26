# Institute FAQ Chatbot - GUI Version
# Even Semester Hack-O-Week Project
# Run this file -> a chat window will pop up!

import math
import re
import string
import tkinter as tk
from tkinter import scrolledtext

# -------------------------------------------------------
# WEEK 1 - Basic FAQ Data (15 fixed questions)
# -------------------------------------------------------

faq_data = {
    "what are the fees": "The tuition fee is Rs.85,000 per year. SC/ST students get 50% concession.",
    "what is the tuition fee": "The tuition fee is Rs.85,000 per year. SC/ST students get 50% concession.",
    "what is the hostel fee": "Hostel fee is Rs.45,000 per year including mess charges.",
    "what are the college timings": "College timings are Monday to Saturday, 8:00 AM to 5:00 PM.",
    "what are the library timings": "Library is open 8 AM to 9 PM on weekdays, 9 AM to 6 PM on Saturday.",
    "when is the sem 5 exam": "SEM 5 exams are in November. Unit tests are in September.",
    "how to apply for admission": "Apply online on the college portal. Submit documents to Room 10, Block A.",
    "what documents are required": "10th & 12th marksheets, TC, migration certificate, Aadhaar, 6 photos.",
    "what is the exam fee": "Exam fee is Rs.1,200 per semester. Practical exam fee is Rs.300 per subject.",
    "how to contact the principal": "Principal office is Room 1, Admin Block. Phone: 0712-2345678.",
    "what are the hostel rules": "Hostel curfew is 9 PM for boys, 8:30 PM for girls. No ragging allowed.",
    "is there any scholarship": "Yes! Merit scholarship for students above 75%. Govt scholarships also available.",
    "what is the canteen timing": "Canteen is open 7:30 AM to 7:00 PM on weekdays.",
    "how to contact exam section": "Exam section is Room 102, Admin Block. Email: exams@institute.edu.in",
    "where is the sem 3 timetable": "Timetable is on the department notice board and college ERP portal.",
}

# -------------------------------------------------------
# WEEK 2 - Text Preprocessing
# -------------------------------------------------------

stopwords = ["a", "an", "the", "is", "are", "was", "were", "i", "me", "my",
             "we", "you", "your", "he", "she", "it", "they", "this", "that",
             "what", "which", "who", "how", "when", "where", "of", "in", "on",
             "at", "to", "for", "with", "do", "does", "did", "can", "could",
             "will", "would", "please", "tell", "me", "about", "give", "know"]

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    words = [w for w in words if w not in stopwords]
    return words

# -------------------------------------------------------
# WEEK 3 - Synonym Dictionary
# -------------------------------------------------------

synonyms = {
    "fees":        ["fee", "fees", "tuition", "payment", "cost", "charge", "money", "pay", "price"],
    "hostel":      ["hostel", "dorm", "dormitory", "accommodation", "room", "boarding", "mess"],
    "exam":        ["exam", "exams", "examination", "test", "semester", "sem", "paper", "unit"],
    "timing":      ["timing", "timings", "time", "hours", "schedule", "open", "close"],
    "admission":   ["admission", "admissions", "apply", "enrollment", "join", "registration"],
    "contact":     ["contact", "phone", "email", "reach", "call", "number", "office"],
    "scholarship": ["scholarship", "merit", "aid", "concession", "discount", "financial"],
    "timetable":   ["timetable", "schedule", "class", "lecture", "period"],
    "library":     ["library", "lib", "books", "reading"],
    "canteen":     ["canteen", "cafeteria", "food", "lunch", "eat"],
}

def expand_synonyms(words):
    expanded = list(words)
    for word in words:
        for canonical, syn_list in synonyms.items():
            if word in syn_list:
                if canonical not in expanded:
                    expanded.append(canonical)
    return expanded

# -------------------------------------------------------
# WEEK 4 - TF-IDF Retrieval
# -------------------------------------------------------

corpus = list(faq_data.keys())

def compute_tfidf_score(query_words, doc):
    doc_words = doc.split()
    score = 0
    N = len(corpus)
    for qw in query_words:
        tf = doc_words.count(qw) / (len(doc_words) + 1)
        df = sum(1 for d in corpus if qw in d.split())
        idf = math.log((N + 1) / (df + 1)) + 1
        score += tf * idf
    return score

def find_best_match(user_input):
    words = preprocess(user_input)
    words = expand_synonyms(words)
    best_match = None
    best_score = 0
    for question in corpus:
        score = compute_tfidf_score(words, question)
        if score > best_score:
            best_score = score
            best_match = question
    if best_score > 0.05:
        return best_match, best_score
    return None, 0

# -------------------------------------------------------
# WEEK 5 - Intent Classification
# -------------------------------------------------------

intent_keywords = {
    "fees":        ["fee", "fees", "tuition", "payment", "cost", "charge", "money"],
    "exams":       ["exam", "test", "result", "marks", "grade", "paper", "unit"],
    "timetable":   ["timetable", "schedule", "class", "lecture", "period"],
    "hostel":      ["hostel", "dorm", "room", "mess", "warden", "curfew"],
    "admissions":  ["admission", "apply", "document", "certificate", "registration"],
    "contacts":    ["contact", "phone", "email", "principal", "office", "call"],
    "scholarship": ["scholarship", "merit", "aid", "concession"],
}

def classify_intent(words):
    best_intent = "general"
    best_count = 0
    for intent, keywords in intent_keywords.items():
        count = sum(1 for w in words if w in keywords)
        if count > best_count:
            best_count = count
            best_intent = intent
    return best_intent

# -------------------------------------------------------
# WEEK 6 - Entity Extraction
# -------------------------------------------------------

def extract_entities(text):
    entities = {}
    sem_match = re.search(r'sem(?:ester)?\s*(\d+)', text.lower())
    if sem_match:
        entities["semester"] = "SEM " + sem_match.group(1)
    year_match = re.search(r'(first|second|third|fourth|1st|2nd|3rd|4th)\s+year', text.lower())
    if year_match:
        entities["year"] = year_match.group(0)
    date_match = re.search(r'\b(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*)', text.lower())
    if date_match:
        entities["date"] = date_match.group(0)
    return entities

# -------------------------------------------------------
# WEEK 7 - Context Handling
# -------------------------------------------------------

context = {
    "last_intent": None,
    "last_answer": None,
    "last_question": None,
}

def is_followup(user_input):
    followup_words = ["more", "detail", "explain", "what about", "tell me more", "elaborate", "also"]
    for word in followup_words:
        if word in user_input.lower():
            return True
    return False

# -------------------------------------------------------
# WEEK 8 - Fallback and Handover
# -------------------------------------------------------

human_advisors = {
    "fees":       "Finance Office - Room 5, Admin Block | fees@institute.edu.in",
    "exams":      "Exam Section - Room 102, Admin Block | exams@institute.edu.in",
    "hostel":     "Hostel Warden - Hostel Block A | hostel@institute.edu.in",
    "admissions": "Admission Office - Room 10, Block A | admissions@institute.edu.in",
    "contacts":   "Reception - Ground Floor | 0712-2345678",
    "general":    "Student Help Desk - Room 15 | helpdesk@institute.edu.in",
}

fallback_replies = [
    "Sorry, I didn't understand that. Can you rephrase?",
    "I'm not sure about that. Try asking about fees, exams, hostel or timings.",
    "Hmm, I don't have info on that.",
]
fallback_index = [0]

def get_fallback(intent):
    reply = fallback_replies[fallback_index[0] % len(fallback_replies)]
    fallback_index[0] += 1
    advisor = human_advisors.get(intent, human_advisors["general"])
    return reply + "\n\nYou can also contact:\n" + advisor

# -------------------------------------------------------
# WEEK 9 - Multichannel Info
# -------------------------------------------------------

def get_channel_info():
    return ("EduBot is available on:\n"
            "  Web     -> Open index.html in browser\n"
            "  App     -> Download EduBot from Play Store\n"
            "  WhatsApp-> Send HI to +91-9876543210\n"
            "  ERP     -> Login -> Chat Assistant")

# -------------------------------------------------------
# WEEK 10 - Analytics
# -------------------------------------------------------

analytics = {
    "total_queries": 0,
    "matched": 0,
    "fallbacks": 0,
    "intents": {},
}

def update_analytics(matched, intent):
    analytics["total_queries"] += 1
    if matched:
        analytics["matched"] += 1
    else:
        analytics["fallbacks"] += 1
    if intent != "general":
        analytics["intents"][intent] = analytics["intents"].get(intent, 0) + 1

def get_analytics_text():
    lines = []
    lines.append("======= ANALYTICS =======")
    lines.append("Total queries  : " + str(analytics["total_queries"]))
    lines.append("Matched        : " + str(analytics["matched"]))
    lines.append("Fallbacks      : " + str(analytics["fallbacks"]))
    lines.append("Intents seen   : " + str(analytics["intents"]))
    lines.append("=========================")
    return "\n".join(lines)

# -------------------------------------------------------
# CORE BOT LOGIC
# -------------------------------------------------------

def get_bot_reply(user_input):
    user_input = user_input.strip()
    if not user_input:
        return ""

    if user_input.lower() == "stats":
        return get_analytics_text()

    if any(w in user_input.lower() for w in ["channel", "whatsapp", "mobile", "app", "deploy"]):
        return get_channel_info()

    if is_followup(user_input) and context["last_answer"]:
        return "Following up on your last question:\n\n" + context["last_answer"]

    words = preprocess(user_input)
    words = expand_synonyms(words)
    intent = classify_intent(words)
    entities = extract_entities(user_input)

    best_question, score = find_best_match(user_input)

    if best_question:
        answer = faq_data[best_question]
        context["last_intent"] = intent
        context["last_answer"] = answer
        context["last_question"] = best_question
        update_analytics(True, intent)

        info = "[Intent: " + intent + "]"
        if entities:
            info += " [Entities: " + str(entities) + "]"

        return info + "\n\n" + answer
    else:
        update_analytics(False, intent)
        return get_fallback(intent)

# -------------------------------------------------------
# GUI - Tkinter Chat Window
# -------------------------------------------------------

def send_message(event=None):
    user_text = entry_box.get().strip()
    if not user_text:
        return

    # show user message
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, "You: " + user_text + "\n", "user")
    entry_box.delete(0, tk.END)

    # get bot reply
    reply = get_bot_reply(user_text)
    chat_box.insert(tk.END, "Bot: " + reply + "\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)


def clear_chat():
    chat_box.config(state=tk.NORMAL)
    chat_box.delete(1.0, tk.END)
    chat_box.insert(tk.END, "Bot: Chat cleared. Ask me anything!\n\n", "bot")
    chat_box.config(state=tk.DISABLED)


# --- build window ---
window = tk.Tk()
window.title("EduBot - Institute FAQ Chatbot")
window.geometry("600x550")
window.resizable(False, False)
window.configure(bg="#f0f0f0")

# title label
title_label = tk.Label(window, text="EduBot - Institute FAQ Assistant",
                       font=("Arial", 14, "bold"), bg="#4a90d9", fg="white",
                       pady=10)
title_label.pack(fill=tk.X)

hint_label = tk.Label(window, text="Type 'stats' for analytics | Type 'channels' for deployment info",
                      font=("Arial", 9), bg="#d0e4f7", fg="#333", pady=4)
hint_label.pack(fill=tk.X)

# chat display area
chat_box = scrolledtext.ScrolledText(window, state=tk.DISABLED,
                                     font=("Courier", 11),
                                     bg="#ffffff", fg="#222",
                                     wrap=tk.WORD, pady=8, padx=8,
                                     height=22)
chat_box.pack(padx=10, pady=8, fill=tk.BOTH, expand=True)

# color tags
chat_box.tag_config("user", foreground="#1a5276", font=("Courier", 11, "bold"))
chat_box.tag_config("bot",  foreground="#117a65", font=("Courier", 11))

# welcome message
chat_box.config(state=tk.NORMAL)
chat_box.insert(tk.END, "Bot: Hello! I am EduBot, your institute FAQ assistant.\n", "bot")
chat_box.insert(tk.END, "Bot: Ask me about fees, exams, hostel, timings, admissions etc.\n\n", "bot")
chat_box.config(state=tk.DISABLED)

# bottom frame for input + buttons
bottom_frame = tk.Frame(window, bg="#f0f0f0")
bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

entry_box = tk.Entry(bottom_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE)
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
entry_box.bind("<Return>", send_message)
entry_box.focus()

send_btn = tk.Button(bottom_frame, text="Send", font=("Arial", 11, "bold"),
                     bg="#4a90d9", fg="white", padx=12, pady=4,
                     relief=tk.FLAT, cursor="hand2",
                     command=send_message)
send_btn.pack(side=tk.LEFT, padx=(6, 4))

clear_btn = tk.Button(bottom_frame, text="Clear", font=("Arial", 11),
                      bg="#e0e0e0", fg="#333", padx=10, pady=4,
                      relief=tk.FLAT, cursor="hand2",
                      command=clear_chat)
clear_btn.pack(side=tk.LEFT)

window.mainloop()
