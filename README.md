



# 🧠 EduNexusAI - MongoDB Export Automation

This Python script connects to your **MongoDB database (`EduNexusAI`)**, fetches all documents from the **`summaries`** collection, and automatically generates:

* 📄 **Word file** → `example.docx`
* 🧾 **PDF file** → `example.pdf`
* 🖼️ **PowerPoint file** → `example.pptx`

Each file includes data such as the **title**, **introduction**, **professional summary**, **student summary**, and **creation date** of each entry in your MongoDB collection.

---

## ⚙️ 1. Requirements

Before you begin, make sure you have installed:

* 🐍 **Python 3.8+**
* 🍃 **MongoDB** (running locally or remotely)
* 💻 **Visual Studio Code** or another IDE (optional)

---

## 📁 2. Project Structure

Your folder should look like this:

```
EduNexus/
│
├── core/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── scripts/
│   ├── create_files.py   ← (Your main script)
│
├── venv/                 ← (Virtual environment)
│
├── manage.py
└── README.md             ← (This file)
```

---

## 📦 3. Installation Steps

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/EduNexusAI.git
cd EduNexusAI
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3 — Activate the Environment

* **Windows PowerShell:**

  ```bash
  .\venv\Scripts\Activate.ps1
  ```
* **macOS/Linux:**

  ```bash
  source venv/bin/activate
  ```

### Step 4 — Install Required Libraries

```bash
pip install python-docx reportlab python-pptx pymongo
```

---

## 🗄️ 4. MongoDB Setup

Make sure your MongoDB server is running and contains the following:

* Database: `EduNexusAI`
* Collection: `summaries`

### Example Document:

```json
{
  "title": "Artificial Intelligence",
  "introduction": "AI aims to create systems capable of performing tasks that require human intelligence.",
  "professional_summary": "Artificial Intelligence (AI) is a branch of computer science focused on creating intelligent machines.",
  "student_summary": "AI helps computers think and learn like humans.",
  "created_at": "2025-10-22T08:49:15.016Z"
}
```

---

## ▶️ 5. Running the Script

If you’re inside the `scripts` folder, run:

```bash
python create_files.py
```

Once the script finishes, you’ll find the following files generated:

```
example.docx
example.pdf
example.pptx
```

These files will contain your MongoDB summary data neatly formatted.

---

## 📘 6. What Each File Contains

### 📝 Word File (`example.docx`)

* A heading: “AI Summaries from MongoDB”
* Each summary with title, introduction, and summaries separated by spacing.

### 🧾 PDF File (`example.pdf`)

* A printable version of the same data.
* Each record appears with spacing and automatic page breaks.

### 🖼️ PowerPoint File (`example.pptx`)

* A title slide.
* Each MongoDB document on a separate slide with structured content.

---

## 🔧 7. Troubleshooting

| Issue                      | Solution                                                                      |
| -------------------------- | ----------------------------------------------------------------------------- |
| `ModuleNotFoundError`      | Run `pip install python-docx reportlab python-pptx pymongo`                   |
| `No data found in MongoDB` | Ensure your MongoDB server is running and the `summaries` collection has data |
| `Permission denied`        | Try running your terminal or VS Code as administrator                         |

---

## ✅ 8. Example Command Summary

If you’re working from scratch:

```bash
cd C:\Users\User\EduNexus\scripts
.\venv\Scripts\Activate.ps1
pip install python-docx reportlab python-pptx pymongo
python create_files.py
```

---

## 🧾 9. requirements.txt (Optional)

You can create a `requirements.txt` file to simplify setup:

```
python-docx
reportlab
python-pptx
pymongo
```

Then install everything using:

```bash
pip install -r requirements.txt
```

---

## 👨‍💻 10. Author

**EduNexus AI Team**
Building smart educational automation tools with Python 🧠⚡


