from flask import Flask, request, jsonify
import os
import pdfplumber

from matcher import calculate_match_score, analyze_skills, generate_suggestions


# --------------------------------
# Flask App
# --------------------------------

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)


# --------------------------------
# Upload Folder
# --------------------------------

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------------
# Home Page
# --------------------------------

@app.route("/")
def home():

    return app.send_static_file("index.html")


# --------------------------------
# Resume Upload
# --------------------------------

@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume uploaded"
        }), 400


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    if not file.filename.lower().endswith(".pdf"):

        return jsonify({
            "error": "Please upload a PDF file"
        }), 400


    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )


    file.save(file_path)


    # Extract text from PDF

    extracted_text = ""


    try:

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                text = page.extract_text()

                if text:

                    extracted_text += text + "\n"


    except Exception as error:

        return jsonify({
            "error": "Could not read the PDF",
            "details": str(error)
        }), 500


    return jsonify({

        "message": "Resume uploaded successfully!",

        "filename": file.filename,

        "text": extracted_text

    })


# --------------------------------
# Resume + Job Matching
# --------------------------------

@app.route("/match", methods=["POST"])
def match_resume():
    data = request.get_json()

    resume_text = data.get("resume_text", "")
    job_description = data.get("job_description", "")

    if not resume_text.strip() or not job_description.strip():
        return jsonify({
            "error": "Resume text and job description are required."
        }), 400

    match_score = calculate_match_score(
        resume_text,
        job_description
    )

    skills_result = analyze_skills(
        resume_text,
        job_description
    )

    suggestions = generate_suggestions(
    resume_text,
    job_description
)

    return jsonify({
    "match_score": match_score,
    "matching_skills": skills_result["matching_skills"],
    "missing_skills": skills_result["missing_skills"],
    "suggestions": suggestions
})

# --------------------------------
# Run Flask
# --------------------------------

if __name__ == "__main__":

    app.run(debug=True)