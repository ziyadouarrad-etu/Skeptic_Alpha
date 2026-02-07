# Skeptical Alpha: Neuro-Symbolic Engineering Solver

## Overview

**Skeptical Alpha** is a multi-agent system designed to bridge the **Stochastic–Symbolic Gap** in engineering mathematics. It combines the creative problem-solving abilities of **Large Language Models (LLMs)** with the absolute precision of **symbolic computation (SymPy)** to eliminate mathematical hallucinations.

The system ensures that every generated solution is **formally verified**, not just plausibly correct.

---

## 🚀 Key Features

- **Neuro-Symbolic Pipeline**  
  Implements a **Proposer–Skeptic–Auditor** architecture to certify mathematical truth.

- **Hallucination Detection**  
  Deterministically identifies cases where an LLM produces *plausible-but-incorrect* derivations.

- **API Resilience**  
  Uses a synchronous rotation system across multiple API keys to bypass rate limits during heavy batch processing.

- **Live Analytics**  
  Built-in dashboard for tracking:
  - Hallucination rates  
  - Verification statuses  
  - Average retries across engineering domains  

---

## 🛠️ Setup Instructions

### 1. Environment Configuration

Clone the repository and create a `.env` file in the root directory. Add your API keys to support the rotation logic:

```plaintext
GROQ_API_KEY_1=your_first_key
GROQ_API_KEY_2=your_second_key
GROQ_API_KEY_3=your_third_key
```

### 2. Installation
Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies
```
pip install django sympy requests python-dotenv
```
### 3. Database Initialization
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 📊 Running the Research Study
To replicate the Hallucination Analysis I conducted (50-problem batch), execute the automated runner:
```
python automator.py
```
Once completed, visit the /analytics/ endpoint in your browser to view the distribution of verified vs. hallucinated solutions.

---

## 📸Screenshots
### landing page
<img width="1920" height="895" alt="image" src="https://github.com/user-attachments/assets/019f7b4e-53e7-4737-9077-6c1ee2523c1f" />

### The math keyboard
<img width="1920" height="883" alt="image" src="https://github.com/user-attachments/assets/432aa362-160f-465f-a8c1-908e7abbfa0e" />

### The result page
<img width="1920" height="891" alt="image" src="https://github.com/user-attachments/assets/f6ce3545-c859-4478-ad48-7095a6c7a529" />
<img width="1920" height="889" alt="image" src="https://github.com/user-attachments/assets/6abfc4f5-2f66-46a1-896b-db23ae2f8bc4" />

### The audit trail
<img width="910" height="656" alt="image" src="https://github.com/user-attachments/assets/44d27bf6-7c21-4ec4-bb48-9135a4e17c1d" />

## The Analytics page
<img width="1213" height="888" alt="image" src="https://github.com/user-attachments/assets/19cc3ea8-34eb-45e2-b596-732c88b9eb86" />

---

## 🎓 Author
Developed by **Ouarrad Ziyad** an AI and CS Engeneering student at ENSAM Casablanca

This project was built as part of the AgorAI Hackathon
