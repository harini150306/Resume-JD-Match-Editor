"""
Core matching engine: compares resume text against JD text and produces
a match score plus a gap analysis (missing skills).

Uses a hybrid score:
- 60% skill overlap  -> % of JD's required skills that are present in the resume
- 40% semantic similarity -> cosine similarity between resume and JD embeddings,
  which catches related concepts even when exact skill keywords differ
  (e.g. resume says "container orchestration", JD says "Kubernetes")

The sentence-transformer model is loaded once at import time and reused,
since loading it per-request would be slow.
"""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.skill_extractor import extract_skills

KEYWORD_WEIGHT = 0.6
SEMANTIC_WEIGHT = 0.4

_model = None  # lazy-loaded singleton


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _skill_overlap_score(resume_skills: set, jd_skills: set) -> float:
    """% of JD-required skills that are present in the resume. 0-100 scale."""
    if not jd_skills:
        return 0.0
    matched = resume_skills & jd_skills
    return round((len(matched) / len(jd_skills)) * 100, 2)


def _semantic_similarity_score(resume_text: str, jd_text: str) -> float:
    """Cosine similarity between whole-document embeddings. 0-100 scale."""
    model = _get_model()
    embeddings = model.encode([resume_text, jd_text])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    sim = max(0.0, min(1.0, float(sim)))
    return round(sim * 100, 2)


def compute_match(resume_text: str, jd_text: str) -> dict:
    resume_skill_matches = extract_skills(resume_text)
    jd_skill_matches = extract_skills(jd_text)

    resume_skill_names = {s["skill"] for s in resume_skill_matches}
    jd_skill_names = {s["skill"] for s in jd_skill_matches}

    keyword_score = _skill_overlap_score(resume_skill_names, jd_skill_names)
    semantic_score = _semantic_similarity_score(resume_text, jd_text)

    final_score = round(
        (keyword_score * KEYWORD_WEIGHT) + (semantic_score * SEMANTIC_WEIGHT), 2
    )

    matched_skills = sorted(resume_skill_names & jd_skill_names)
    missing_skills_names = jd_skill_names - resume_skill_names

    missing_skills = [
        s for s in jd_skill_matches if s["skill"] in missing_skills_names
    ]
    missing_skills.sort(key=lambda s: (s["category"], s["skill"]))

    return {
        "match_score": final_score,
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skill_count": len(resume_skill_names),
        "jd_skill_count": len(jd_skill_names),
    }