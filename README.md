# EduNexus-AI Project Notes

This is a summary of the main features and APIs implemented in the EduNexus-AI project.

---

## 1️⃣ Users Collection
- Created `users` collection using MongoShell in MongoDB.
- Handles all user data storage.

## 2️⃣ Authentication (Login & Register)
- Registration ensures **passwords are hashed** before storing in the database.
- Login:
  - Checks if the user exists in the database.
  - If user exists, returns **JWT tokens** (access + refresh).
  - If user does not exist, returns an error message.
- **Refresh token**:
  - Used to renew the access token after it expires.

## 3️⃣ User Profile
- Returns the current user's data if logged in.

## 4️⃣ Upload API
- Accepts files from the user.
- Saves the uploaded file on the server.

## 5️⃣ Analyse CV API
- Accepts a CV file.
- Performs analysis.
- Returns the result as JSON.

## 6️⃣ Roadmap API
- Uses CV analysis results to create a personalized roadmap.
- Returns roadmap data along with the results.

## 7️⃣ Summarize & Quiz API
- Summarizes content.
- Generates quizzes based on the content.

## 8️⃣ Export APIs
- Accepts data from other APIs.
- Converts data into different formats: **PDF, DOCX, PPTX**, etc.

---

### ⚡ Notes
- All endpoints requiring authentication use **JWT access tokens**.
- Refresh token mechanism is implemented for secure token renewal.
- File uploads and CV processing are stored and analyzed on the server.
