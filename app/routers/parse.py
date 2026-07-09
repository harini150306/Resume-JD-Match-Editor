from fastapi import APIRouter, UploadFile, File, Form, Depends
from pydantic import BaseModel

from app.services.file_parser import extract_text_from_upload
from app.services.skill_extractor import extract_skills
from app.services.matcher import compute_match
from app.services.recommendations import get_recommendation
from app.dependencies import get_current_user

router = APIRouter()


class ExtractedText(BaseModel):
    text: str
    char_count: int
    word_count: int


def _to_response(text: str) -> ExtractedText:
    return ExtractedText(
        text=text,
        char_count=len(text),
        word_count=len(text.split()),
    )


@router.post("/resume/upload", response_model=ExtractedText)
async def upload_resume(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """Upload a resume file (PDF/DOCX/TXT) and get back extracted text."""
    text = await extract_text_from_upload(file)
    return _to_response(text)


@router.post("/jd/upload", response_model=ExtractedText)
async def upload_jd_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """Upload a JD as a file, if the user prefers that over pasting text."""
    text = await extract_text_from_upload(file)
    return _to_response(text)


@router.post("/jd/text", response_model=ExtractedText)
async def submit_jd_text(jd_text: str = Form(...), current_user=Depends(get_current_user)):
    """Accept a pasted job description as plain text."""
    return _to_response(jd_text.strip())


class SkillExtractionRequest(BaseModel):
    text: str


class SkillMatch(BaseModel):
    skill: str
    category: str
    matched_as: str


class SkillExtractionResponse(BaseModel):
    skills: list[SkillMatch]
    count: int


@router.post("/skills/extract", response_model=SkillExtractionResponse)
async def extract_skills_from_text(payload: SkillExtractionRequest, current_user=Depends(get_current_user)):
    """Extract known skills (from our taxonomy) out of the given text."""
    skills = extract_skills(payload.text)
    return SkillExtractionResponse(skills=skills, count=len(skills))


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str


class MissingSkill(BaseModel):
    skill: str
    category: str
    matched_as: str
    recommendation: str


class MatchResponse(BaseModel):
    match_score: float
    keyword_score: float
    semantic_score: float
    matched_skills: list[str]
    missing_skills: list[MissingSkill]
    resume_skill_count: int
    jd_skill_count: int


@router.post("/match", response_model=MatchResponse)
async def match_resume_to_jd(payload: MatchRequest, current_user=Depends(get_current_user)):
    """
    Compare resume text against JD text.
    Returns a match score plus a categorized list of missing skills,
    each with a short recommendation on what to learn.
    """
    result = compute_match(payload.resume_text, payload.jd_text)

    missing_with_recommendations = [
        MissingSkill(
            skill=s["skill"],
            category=s["category"],
            matched_as=s["matched_as"],
            recommendation=get_recommendation(s["skill"]),
        )
        for s in result["missing_skills"]
    ]

    return MatchResponse(
        match_score=result["match_score"],
        keyword_score=result["keyword_score"],
        semantic_score=result["semantic_score"],
        matched_skills=result["matched_skills"],
        missing_skills=missing_with_recommendations,
        resume_skill_count=result["resume_skill_count"],
        jd_skill_count=result["jd_skill_count"],
    )