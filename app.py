from flask import Flask, render_template, request, redirect, url_for, session
from db import engine, Base, SessionLocal
import models  # Registers User and Reports tables
from ai import analyze_resume  # Imports your OpenAI analysis function
import PyPDF2
import docx
import json

app = Flask(__name__)
app.secret_key = "secret123"

# Fixed: Typo 'matadata' corrected to 'metadata'
Base.metadata.create_all(bind=engine)  


@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


# --- SIGNUP ---
@app.route("/signup", methods=["GET", "POST"])
def signup():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            db.close()
            return "User already exists. Please log in."
        
        user = models.User(email=email, password=password)
        db.add(user)
        db.commit()
        db.close()

        return redirect("/login")
    
    db.close()
    return render_template("signup.html")


# --- LOGIN ---
# Fixed: 'method' corrected to plural 'methods'
@app.route("/login", methods=["GET", "POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(models.User).filter_by(email=email, password=password).first()
        if user:
            session["user"] = user.email
            db.close()
            return redirect("/dashboard") 
        else:
            db.close()
            return "Invalid credentials. Please try again."
            
    db.close()
    return render_template("login.html")


# --- DASHBOARD ---
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    
    # Fixed: Removed the early 'return render_template' that was blocking this entire block!
    result = None
    resume_text = ""
    user_goal = ""

    if request.method == "POST":
        # Fixed: Changed 'user.goal' to local variable 'user_goal' matching the check below
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume") or ""
        file = request.files.get("file")

        # --- File Handling ---
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted
                    resume_text += text
                except Exception as e:
                    result = {"error": f"Error reading PDF file: {str(e)}"}

            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text += text
                except Exception as e:
                    result = {"error": f"Error reading DOCX file: {str(e)}"}     

        # --- Process and Save Report ---
        if resume_text and user_goal:
            try:
                # Fixed: Corrected typo 'anlyze_resume' to 'analyze_resume'
                result = analyze_resume(resume_text, user_goal)

                db = SessionLocal()
                user = db.query(models.User).filter_by(email=session["user"]).first()

                if user:
                    # Fixed: Corrected 'models.report{...}' to 'models.Reports(...)'
                    report = models.Reports(
                        user_id=user.id,
                        resume_text=resume_text,
                        result=json.dumps(result)
                    )
                    db.add(report)
                    db.commit()  # Fixed: Added db.commit() so it saves to TiDB Cloud!
                db.close()

            except Exception as e: # Fixed: Capitalized 'Exception'
                result = {"error": f"Processing error: {str(e)}"}

    # Fixed: Added commas inside the render_template call parameters
    return render_template(
        "dashboard.html",
        user=session["user"],
        result=result
    )


# --- HISTORY ---
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db = SessionLocal()
    user = db.query(models.User).filter_by(email=session["user"]).first()

    # Fixed: Changed 'models.Report' to plural 'models.Reports' to match models.py
    reports = db.query(models.Reports).filter_by(user_id=user.id).all()

    parsed_reports = []
    for r in reports:
        try:
            parsed_result = json.loads(r.result)
        except Exception:
            parsed_result = {}

        parsed_reports.append({
            "resume": r.resume_text,
            "result": parsed_result
        })
    
    db.close()
    return render_template("history.html", reports=parsed_reports)


# --- LOGOUT ---
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)