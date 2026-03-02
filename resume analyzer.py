import re
import nltk
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

# ---------------------------------------
# Predefined Important Skills
# ---------------------------------------
IMPORTANT_SKILLS = [
    "python", "machine learning", "data analysis",
    "sql", "excel", "communication",
    "teamwork", "problem solving",
    "leadership", "project management"
]

# ---------------------------------------
# Extract Text from PDF
# ---------------------------------------
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "
    return text

# ---------------------------------------
# Extract Text from TXT
# ---------------------------------------
def extract_text_from_txt(file):
    return file.read().decode("utf-8")


# ---------------------------------------
# Clean Text
# ---------------------------------------
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    return text


# ---------------------------------------
# Skill Detection
# ---------------------------------------
def detect_skills(text):
    detected = []
    missing = []

    for skill in IMPORTANT_SKILLS:
        if skill in text:
            detected.append(skill)
        else:
            missing.append(skill)

    return detected, missing


# ---------------------------------------
# Grammar Feedback (Basic NLP Logic)
# ---------------------------------------
def grammar_analysis(text):
    sentences = sent_tokenize(text)

    short_sentences = [s for s in sentences if len(s.split()) < 4]
    long_sentences = [s for s in sentences if len(s.split()) > 30]

    feedback = []

    if len(short_sentences) > 3:
        feedback.append("Too many very short sentences detected.")

    if len(long_sentences) > 2:
        feedback.append("Some sentences are too long. Improve readability.")

    if not feedback:
        feedback.append("Sentence structure looks balanced.")

    return " ".join(feedback)


# ---------------------------------------
# Resume Strength Score
# ---------------------------------------
def calculate_score(detected_skills, text):
    skill_score = (len(detected_skills) / len(IMPORTANT_SKILLS)) * 70

    word_count = len(text.split())
    length_score = 0

    if 300 <= word_count <= 800:
        length_score = 30
    elif word_count < 300:
        length_score = 15
    else:
        length_score = 20

    final_score = round(skill_score + length_score, 2)
    return min(final_score, 100)


# ---------------------------------------
# Main Analyzer Function
# ---------------------------------------
def analyze_resume(file):

    if file is None:
        return "Please upload a resume file."

    # Detect file type
    if file.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file)
    elif file.name.endswith(".txt"):
        raw_text = extract_text_from_txt(file)
    else:
        return "Unsupported file format. Upload PDF or TXT."

    cleaned = clean_text(raw_text)

    detected, missing = detect_skills(cleaned)

    grammar_feedback = grammar_analysis(raw_text)

    score = calculate_score(detected, cleaned)

    result = f"""
Resume Strength Score: {score}/100

Detected Skills:
{', '.join(detected) if detected else 'No important skills detected'}

Missing Important Skills:
{', '.join(missing)}

Grammar Feedback:
{grammar_feedback}
"""

    return result
