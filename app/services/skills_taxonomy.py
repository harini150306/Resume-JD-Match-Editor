"""
Curated skills taxonomy for backend/software development roles.
Organized by category so we can later show grouped results
(e.g. "Missing Databases", "Missing DevOps tools") instead of one flat list.

Each skill maps to a list of aliases/variations that should all count
as a match for that skill (e.g. "JS" and "Javascript" both mean "JavaScript").
"""

SKILLS_TAXONOMY = {
    "languages": {
        "Python": ["python", "python3", "py"],
        "Java": ["java"],
        "JavaScript": ["javascript", "js", "es6", "ecmascript"],
        "TypeScript": ["typescript", "ts"],
        "C++": ["c++", "cpp"],
        "C": ["c programming"],
        "Go": ["golang", "go lang"],
        "SQL": ["sql"],
    },
    "backend_frameworks": {
        "FastAPI": ["fastapi", "fast api"],
        "Flask": ["flask"],
        "Django": ["django"],
        "Spring Boot": ["spring boot", "springboot", "spring"],
        "Express.js": ["express.js", "expressjs", "express"],
        "Node.js": ["node.js", "nodejs", "node"],
    },
    "frontend_frameworks": {
        "React": ["react.js", "reactjs", "react"],
        "Angular": ["angular", "angularjs"],
        "Vue.js": ["vue.js", "vuejs", "vue"],
        "HTML/CSS": ["html", "css", "html5", "css3"],
    },
    "databases": {
        "PostgreSQL": ["postgresql", "postgres"],
        "MySQL": ["mysql"],
        "MongoDB": ["mongodb", "mongo"],
        "SQLite": ["sqlite"],
        "Redis": ["redis"],
    },
    "orm_and_data": {
        "SQLAlchemy": ["sqlalchemy"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
    },
    "devops_cloud": {
        "Docker": ["docker", "containerization"],
        "Kubernetes": ["kubernetes", "k8s"],
        "AWS": ["aws", "amazon web services"],
        "Azure": ["azure", "microsoft azure"],
        "GCP": ["gcp", "google cloud", "google cloud platform"],
        "CI/CD": ["ci/cd", "cicd", "continuous integration", "continuous deployment"],
        "Git": ["git", "github", "gitlab", "version control"],
        "Linux": ["linux", "unix"],
    },
    "auth_security": {
        "JWT": ["jwt", "json web token"],
        "OAuth": ["oauth", "oauth2"],
        "RBAC": ["rbac", "role-based access control", "role based access control"],
    },
    "apis_architecture": {
        "REST API": ["rest api", "restful", "rest"],
        "GraphQL": ["graphql"],
        "Microservices": ["microservices", "microservice architecture"],
        "WebSockets": ["websocket", "websockets"],
    },
    "testing": {
        "Pytest": ["pytest"],
        "Unit Testing": ["unit testing", "unit tests"],
        "Postman": ["postman"],
    },
    "ai_ml": {
        "Machine Learning": ["machine learning", "ml"],
        "NLP": ["nlp", "natural language processing"],
        "Sentence Transformers": ["sentence-transformers", "sentence transformers"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
    },
}


def flatten_taxonomy() -> dict:
    """
    Returns a flat dict: {alias: canonical_skill_name}
    e.g. {"reactjs": "React", "react.js": "React", "react": "React", ...}
    Used by the extractor to do fast lookups.
    """
    flat = {}
    for category, skills in SKILLS_TAXONOMY.items():
        for canonical_name, aliases in skills.items():
            for alias in aliases:
                flat[alias.lower()] = canonical_name
    return flat


def get_category_for_skill(skill_name: str) -> str:
    """Given a canonical skill name, returns its category."""
    for category, skills in SKILLS_TAXONOMY.items():
        if skill_name in skills:
            return category
    return "other"