"""
Extracts known skills from raw resume/JD text using the curated taxonomy.

Uses regex with word boundaries so we don't get false positives like
matching "C" inside the word "Communication", or "Go" inside "Google".
Special characters in aliases (like "C++", ".NET") are escaped properly
since they'd otherwise break the regex.
"""
import re
from app.services.skills_taxonomy import flatten_taxonomy, get_category_for_skill

_ALIAS_TO_SKILL = flatten_taxonomy()


def _build_pattern(alias: str) -> re.Pattern:
    """
    Builds a word-boundary-safe regex for a given alias.
    Standard \b word boundaries don't work well around symbols like '+' or '.',
    so we handle those aliases with lookaround instead of \b.
    """
    escaped = re.escape(alias)
    has_symbols = any(ch in alias for ch in "+.#/")
    if has_symbols:
        # Use lookaround so we match "C++" even though \b fails next to '+'
        pattern = rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])"
    else:
        # Negative lookbehind for '.' stops bare aliases like "js" from matching
        # inside "Node.js" / "Express.js" (those are separate skills, not JavaScript)
        pattern = rf"(?<!\.)\b{escaped}\b"
    return re.compile(pattern, re.IGNORECASE)


# Precompile all patterns once (aliases -> compiled regex), reused for every extraction call
_COMPILED_PATTERNS = {alias: _build_pattern(alias) for alias in _ALIAS_TO_SKILL}


def extract_skills(text: str) -> list[dict]:
    """
    Scans text and returns a list of matched skills:
    [{"skill": "Python", "category": "languages", "matched_as": "python"}, ...]
    Deduplicated by canonical skill name (keeps the first alias matched).
    """
    if not text:
        return []

    found = {}  # canonical_skill -> matched_as (first alias found)
    for alias, pattern in _COMPILED_PATTERNS.items():
        canonical = _ALIAS_TO_SKILL[alias]
        if canonical in found:
            continue  # already matched this skill via another alias
        if pattern.search(text):
            found[canonical] = alias

    results = [
        {
            "skill": skill,
            "category": get_category_for_skill(skill),
            "matched_as": matched_as,
        }
        for skill, matched_as in found.items()
    ]
    # Sort by category then skill name for a clean, grouped output
    results.sort(key=lambda r: (r["category"], r["skill"]))
    return results