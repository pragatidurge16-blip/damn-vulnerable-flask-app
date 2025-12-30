# damn-vulnerable-flask-app/python
A deliberately vulnerable Python Flask web app for learning OWASP vulnerabilities.
# Damn Vulnerable Flask Application (DVFA)

## 📌 Project Overview

Damn Vulnerable Flask Application (DVFA) is an **intentionally vulnerable web application**
developed using **Python Flask**.  
The purpose of this project is to **demonstrate common web application vulnerabilities**
and their **secure fixes** in a practical and easy-to-understand manner.

This project is created **for educational and academic purposes only** and is inspired by
OWASP learning projects (such as OWASP Juice Shop) **only as a conceptual reference**.

> ⚠️ Warning: This application is deliberately insecure.  
> Do NOT deploy this application in production environments.

---

## 🎯 Objectives of the Project

- Understand common web application vulnerabilities
- Learn how insecure coding leads to security issues
- Demonstrate vulnerable vs secure implementations
- Practice OWASP Top 10 concepts
- Academic mini / major project demonstration

---

## 🛠 Technology Stack

| Component | Technology |
|---------|------------|
| Backend | Python Flask |
| Frontend | HTML, Jinja Templates |
| Database | SQLite |
| Session Management | Flask Sessions |
| Serialization | JSON, Pickle |

---

## 🧱 Vulnerabilities Implemented

The following vulnerabilities are intentionally implemented along with their secure fixes:

| # | Vulnerability | Description |
|--|---------------|-------------|
| 1 | SQL Injection | Authentication bypass using unsafe queries |
| 2 | Broken Authentication | Accessing dashboard without login |
| 3 | IDOR | Accessing other users’ data |
| 4 | Insecure Deserialization (JSON) | Role manipulation |
| 5 | Insecure Deserialization (Pickle) | Unsafe object deserialization |
| 6 | Cross-Site Scripting (XSS) | Script injection via user input |
| 7 | Open Redirect | Redirecting users to untrusted URLs |

---

## 📂 Project Structure
```
damn-vulnerable-flask-app/
│
├── app.py
├── requirements.txt
├── templates/
│ ├── login.html
│ ├── register.html
│ └── dashboard.html
│
├── docs/
│ ├── INTRODUCTION.md
│ ├── ARCHITECTURE.md
│ └── VULNERABILITY_CATEGORIES.md
│
├── screenshots/
│ ├── sqli.png
│ └── xss.png
│
├── README.md
└── .gitignore

```
 📚 Documentation

Detailed documentation is available inside the `docs/` folder:

- **INTRODUCTION.md** – Project overview and purpose
- **ARCHITECTURE.md** – Application architecture and flow
- **VULNERABILITY_CATEGORIES.md** – Vulnerabilities with explanation and fixes

---

```
 🚀 How to Run the Application

Step 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/damn-vulnerable-flask-app.git
cd damn-vulnerable-flask-app

Step 2️⃣ Install Dependencies
pip install flask
or
pip install -r requirements.txt

Step 3️⃣ Run the Application
python app.py

Step 4️⃣ Access in Browser
http://127.0.0.1:5000

```
🔐 Secure Coding Practices Demonstrated
Parameterized SQL queries
Session-based authentication
Input validation and output encoding
Access control checks
Allow-list validation
Avoiding unsafe deserialization

```
⚠️ Disclaimer
This project is developed strictly for learning and academic demonstration.
The author is not responsible for any misuse of this application.

```
📖 References
OWASP Top 10 Web Application Security Risks
OWASP Juice Shop (Conceptual Reference Only)
