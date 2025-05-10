import pdfplumber
import re
import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# ===== File/Text Extraction =====
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# ===== Extractors =====
def extract_email(text):
    match = re.search(r'\b\S+@\S+\.\S+\b', text)
    return match.group() if match else "Not found"

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
    return match.group() if match else "Not found"

def extract_skills(text, skills_db):
    doc = nlp(text.lower())
    tokens = set([token.text for token in doc if not token.is_stop and token.is_alpha])
    return [skill for skill in skills_db if skill.lower() in tokens]

# ===== Main =====
def scan_resume(file_path, skills_db):
    text = extract_text_from_pdf(file_path)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text, skills_db)

    print("===== Resume Scan Result =====")
    print(f"All text: {text}")
    print(f"Email   : {email}")
    print(f"Phone   : {phone}")
    print(f"Skills  : {', '.join(skills) if skills else 'None found'}")

# ===== Run (example) =====
if __name__ == "__main__":
    sample_skills = ['Python', 'Machine Learning', 'SQL', 'Django', 'Excel', 'Communication','RDBMS']
    scan_resume("Saivamshi_s_Resume.pdf", sample_skills)
