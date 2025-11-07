# 🧠 EduNexus-AI  
> **An AI-powered educational assistant** that leverages Django, Hugging Face NLP for intelligent text summarization, resume analysis, and career guidance.

---

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-3.2.25-darkgreen?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14.0-red?logo=django&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-API-orange?logo=huggingface&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📚 Table of Contents
<details>
<summary>Click to expand</summary>

1. [Overview](#-overview)
2. [Project Structure](#-project-structure)
3. [Setup Instructions](#-setup-instructions)
4. [Authentication APIs](#-authentication-apis)
5. [Career Assistant APIs](#-career-assistant-apis)
6. [Summarization APIs (Hugging Face)](#-summarization-apis-hugging-face)
7. [Technology Stack](#️-technology-stack)
8. [Testing with Postman](#-testing-with-postman)
9. [Environment Configuration](#-environment-configuration)
10. [Security Notes](#-security--notes)
</details>

---

## 🌟 Overview

**EduNexus-AI** is an intelligent educational assistant that integrates **Django REST Framework** with the **Hugging Face Transformers API** to provide:

- 🔐 Secure JWT-based authentication  
- 🧾 AI-powered text summarization (title, introduction, student-friendly, professional, full)  
- 🧑‍🎓 Resume parsing and skill extraction  
- 🧩 Personalized career roadmap generation  
- 📄 Support for both raw text and uploaded `.pdf`/`.docx` files  

---

## 🧩 Project Structure

```

EduNexus-AI/
├── accounts/               # User registration, login, and roles
├── career_assistant/       # Resume analysis, skill extraction, AI roadmap
├── core/                   # Common utilities and shared services
├── EduNexus/               # Django configs (settings, URLs, WSGI/ASGI)
├── exports/                # Output files and reports
├── manage.py
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/EduNexus-AI.git
cd EduNexus-AI
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up Environment

Create a `.env` file in your project root:

```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=mongodb://localhost:27017/edunexus
HUGGINGFACE_API_KEY=your_huggingface_token
```

### 5️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 6️⃣ Run the Server

```bash
python manage.py runserver
```

Visit 👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔐 Authentication APIs

### 🧾 Register

`POST /auth/register/`

| Key      | Type | Example                                     |
| -------- | ---- | ------------------------------------------- |
| email    | text | [user@example.com](mailto:user@example.com) |
| password | text | 12345                                       |

**Response**

```json
{
  "id": 2,
  "email": "user@example.com",
  "role": "student",
  "is_active": true,
  "date_joined": "2025-11-07T17:33:46.854480Z"
}
```

---

### 🔑 Login

`POST /auth/login/`

| Key      | Type | Example                                     |
| -------- | ---- | ------------------------------------------- |
| email    | text | [user@example.com](mailto:user@example.com) |
| password | text | 12345                                       |

**Response**

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Use the access token in your headers:
`Authorization: Bearer <access_token>`

---

## 🧰 Career Assistant APIs

### 📄 Analyze Resume

`POST /analyze/cv/`

**form-data**

| Key  | Type | Description                     |
| ---- | ---- | ------------------------------- |
| file | file | Upload `.pdf` or `.docx` resume |

**Response**

```json
{
  "filename": "My Resume.pdf",
  "skills_found": ["Python", "Data Analysis"],
  "skills_missing": ["Machine Learning", "Deep Learning"],
  "roadmap": ["Learn ML basics", "Complete DL projects"]
}
```

---

## 🤖 Summarization APIs (Hugging Face)

All summarization endpoints use **Hugging Face Transformers API** to generate natural language summaries.
Each endpoint accepts **either**:

* **Raw text** (key = `text`)
* **File upload** (key = `file`) — supports `.pdf` and `.docx`

---

### 🪶 Title Extraction

`POST http://127.0.0.1:8000/api/summarize/title/`

**Input Options**

```json
{ "text": "Artificial Intelligence (AI) is a branch of computer science..." }
```

*or*
**form-data**

| Key  | Type | Description       |
| ---- | ---- | ----------------- |
| file | file | `.pdf` or `.docx` |

**Response**

```json
{
  "title": "Artificial Intelligence (AI) aims to create systems capable of performing tasks that require human intelligence."
}
```

---

### 🧭 Introduction Summarization

`POST http://127.0.0.1:8000/api/summarize/intro/`

**Input:** `text` or `file`
**Response**

```json
{
  "introduction": "Artificial Intelligence (AI) is a branch of computer science focused on building systems that simulate human reasoning and learning."
}
```

---

### 🧑‍🎓 Student-Friendly Summary

`POST http://127.0.0.1:8000/api/summarize/student/`

**Input:** `text` or `file`
**Response**

```json
{
  "student_friendly_summary": "AI helps computers think and learn like people. It’s used in apps, robots, and smart assistants."
}
```

---

### 👨‍💼 Professional Summary

`POST http://127.0.0.1:8000/api/summarize/professional/`

**Input:** `text` or `file`
**Response**

```json
{
  "professional_summary": "Artificial Intelligence (AI) integrates into diverse domains such as data analytics, automation, and decision-support systems..."
}
```

---

### 📚 Full Document Summarization

`POST http://127.0.0.1:8000/api/summarize/all/`

**Input:** `text` or `file`
**Response**

```json
{
  "title": "The network classification is based on: Geographic Proximity - Host Roles",
  "introduction": "...",
  "professional_summary": "...",
  "student_friendly_summary": "..."
}
```

---

## 🧱️ Technology Stack

| Component            | Technology                              |
| -------------------- | --------------------------------------- |
| **Backend**          | Django 3.2.25                           |
| **API Framework**    | Django REST Framework                   |
| **Authentication**   | Simple JWT                              |
| **Database**         | MongoDB (Djongo)                        |
| **AI/NLP**           | Hugging Face Transformers API + PyTorch |
| **Text/Doc Parsing** | pdfminer.six, pdfplumber, docx2txt      |
| **Environment**      | Python 3.11 +, Virtualenv               |

---

## 🧪 Testing with Postman

1. Use **POST** for all endpoints.
2. Provide input as either:

   * **Raw JSON** → `{ "text": "your text here" }`
   * **form-data** → key = `file`, type = File.
3. Include JWT token if authentication is required:

   ```
   Authorization: Bearer <access_token>
   ```
4. Verify responses: 200 OK or 201 Created.

---

## ⚙️ Environment Configuration

Example `.env` file:

```bash
SECRET_KEY=django-insecure-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=mongodb://localhost:27017/edunexus

# Hugging Face API
HUGGINGFACE_API_KEY=hf_your_personal_access_token
HUGGINGFACE_SUMMARIZATION_MODEL=facebook/bart-large-cnn
```

> ⚡ *Ensure your Hugging Face API key has access to inference endpoints (e.g., `api-inference.huggingface.co`).*

---

## 🛡️ Security & Notes

* JWT authentication required for protected endpoints
* Uploaded files are processed securely and deleted afterward
* `.pdf` and `.docx` only — all others are rejected
* Add `uploads/` and `.env` to `.gitignore`
* Use HTTPS and secure tokens in production

---

⭐ *If you found this project useful, please star the repository!*
