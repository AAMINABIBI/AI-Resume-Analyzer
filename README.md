# AI Resume Analyzer

A Flask web app that analyzes a resume against a specific career goal using
Google's Gemini API, and returns a structured breakdown: extracted skills,
missing skills for that goal, a learning roadmap, and likely interview
questions.

## How it works

1. User signs up / logs in (session-based auth, credentials stored in MySQL)
2. User uploads a resume (PDF or DOCX) or pastes resume text, and states
   their target role/goal
3. The app extracts text from the file using `PyPDF2` (PDF) or `python-docx`
   (DOCX)
4. That text + the user's goal is sent to Gemini with a strict JSON schema,
   instructing it to act as a hiring manager and return:
   - `skills` — relevant skills found in the resume
   - `missing_skills` — real gaps for the stated goal
   - `roadmap` — steps to close those gaps
   - `interview_questions` — questions likely for that role
5. The result is saved to the database and viewable later in **History**

## Tech stack

- **Backend:** Flask, Python
- **Database:** MySQL (TiDB Cloud), SQLAlchemy ORM
- **AI:** Google Gemini API (`google-genai`)
- **File parsing:** PyPDF2, python-docx
- **Auth:** Flask session-based login/signup

## Project structure

```
├── app.py        # Routes: signup, login, dashboard, history, logout
├── ai.py         # Gemini prompt + structured JSON schema for analysis
├── models.py     # SQLAlchemy models: User, Reports
├── db.py         # Database engine/session setup
└── templates/    # HTML templates (signup, login, dashboard, history)
```

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install flask sqlalchemy pymysql PyPDF2 python-docx google-genai python-dotenv
   ```
2. Create a `.env` file with your database URL and Gemini API key:
   ```
   DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:4000/<db>
   GEMINI_API_KEY=your_key_here
   ```
3. Run the app:
   ```bash
   python app.py
   ```

## Status

Actively being developed as I continue learning Python, Flask, and AI/ML —
current focus is on improving the analysis prompt and adding features.

## Author

Aamina Bibi — [GitHub](https://github.com/AAMINABIBI) · [LinkedIn](https://www.linkedin.com/in/aamina-bibi/)
