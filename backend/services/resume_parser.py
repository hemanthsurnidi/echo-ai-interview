"""
ECHO — Resume Intelligence Service
Extracts skills, project titles, and embedded links from PDF & DOCX resumes.
All information is optional and used only to personalize the interview.
"""

import re
import fitz  # PyMuPDF
from docx import Document
import io
from typing import Dict, Any, List

COMMON_TECH_SKILLS = [
    "python", "javascript", "typescript", "react", "next.js", "vue", "angular",
    "node.js", "express", "fastapi", "django", "flask", "java", "spring boot",
    "c++", "c#", ".net", "go", "golang", "rust", "sql", "postgresql", "mysql",
    "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp",
    "git", "github", "ci/cd", "linux", "rest api", "graphql", "html5", "css3",
    "machine learning", "deep learning", "nlp", "computer vision", "pytorch",
    "tensorflow", "scikit-learn", "pandas", "numpy", "opencv", "data structures",
    "algorithms", "system design", "microservices"
]

class ResumeParser:
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> Dict[str, Any]:
        """Extract text, links, and metadata from PDF resume"""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        extracted_links = []

        for page in doc:
            full_text += page.get_text() + "\n"
            # Extract embedded hyperlinks
            for link in page.get_links():
                uri = link.get("uri")
                if uri and uri.startswith("http"):
                    extracted_links.append(uri)

        doc.close()
        return ResumeParser._extract_entities(full_text, extracted_links)

    @staticmethod
    def parse_docx(file_bytes: bytes) -> Dict[str, Any]:
        """Extract text and metadata from DOCX resume"""
        doc = Document(io.BytesIO(file_bytes))
        full_text = ""
        extracted_links = []

        for para in doc.paragraphs:
            full_text += para.text + "\n"
            # Extract hyperlinks in DOCX
            for rel in para.part.rels.values():
                if "hyperlink" in rel.reltype:
                    target = rel.target_ref
                    if target.startswith("http"):
                        extracted_links.append(target)

        return ResumeParser._extract_entities(full_text, extracted_links)

    @staticmethod
    def _extract_entities(text: str, links: List[str]) -> Dict[str, Any]:
        lower_text = text.lower()

        # 1. Detect matching skills
        detected_skills = []
        for skill in COMMON_TECH_SKILLS:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, lower_text):
                detected_skills.append(skill.title() if len(skill) > 3 else skill.upper())

        # 2. Extract potential GitHub / Portfolio URLs from text
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        found_urls = re.findall(url_pattern, text)
        all_links = list(set(links + found_urls))

        github_links = [l for l in all_links if "github.com" in l.lower()]
        portfolio_links = [l for l in all_links if "github.com" not in l.lower() and "linkedin.com" not in l.lower()]

        # 3. Detect candidate name (heuristically from top non-empty lines)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        candidate_name = "Candidate"
        for candidate_line in lines[:5]:
            clean_cand = re.sub(r'[^a-zA-Z\s]', '', candidate_line).strip()
            if 2 <= len(clean_cand.split()) <= 4 and len(clean_cand) < 35:
                if not any(w in clean_cand.lower() for w in ["resume", "curriculum", "vitae", "profile", "contact", "phone", "email"]):
                    candidate_name = clean_cand.title()
                    break

        # 4. Extract project mentions
        project_titles = []
        project_keywords = ["projects", "project experience", "academic projects", "key projects", "personal projects", "technical projects"]
        capture = False
        captured_count = 0
        for i, line in enumerate(lines):
            line_clean = line.strip()
            if any(line_clean.lower() == kw or line_clean.lower().startswith(f"{kw}:") or line_clean.lower().startswith(f"{kw} -") for kw in project_keywords):
                capture = True
                continue
            if capture:
                # Stop if next major section heading encountered
                if any(sec in line_clean.lower() for sec in ["skills", "education", "experience", "certifications", "achievements", "interests"]) and len(line_clean) < 25:
                    break
                # Project header lines usually are 5-70 chars and often have titles, hyphens, pipes, or bold text
                clean_title = re.sub(r'^[•\-\*\d\.\s]+', '', line_clean).strip()
                # Split by | or - to take project title before tech stack or date
                for sep in ["|", " - ", " – ", " — ", "(", "http"]:
                    if sep in clean_title:
                        clean_title = clean_title.split(sep)[0].strip()
                if 4 < len(clean_title) < 55 and not clean_title.lower().startswith("developed") and not clean_title.lower().startswith("implemented"):
                    if clean_title not in project_titles:
                        project_titles.append(clean_title)
                        captured_count += 1
                        if captured_count >= 5:
                            break

        return {
            "candidate_name": candidate_name,
            "detected_skills": detected_skills[:20],
            "github_links": github_links[:5],
            "portfolio_links": portfolio_links[:3],
            "extracted_projects": project_titles[:5],
            "raw_text_length": len(text)
        }
