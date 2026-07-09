"""
Static mapping of skill -> what to learn/focus on if it's missing from the resume.
Starts as a curated dict; can later be swapped for something dynamic (e.g. an LLM call)
without changing the interface (get_recommendation takes a skill name, returns a string).
"""

RECOMMENDATIONS = {
    "Docker": "Learn Docker basics: images, containers, Dockerfile, and docker-compose for multi-service setups.",
    "Kubernetes": "Learn core K8s concepts: pods, deployments, services, and basic kubectl commands.",
    "AWS": "Get familiar with core AWS services: EC2, S3, RDS, and IAM basics. Consider AWS Cloud Practitioner cert.",
    "Azure": "Learn Azure fundamentals: App Services, Azure SQL, and resource groups.",
    "GCP": "Learn GCP basics: Compute Engine, Cloud Storage, and Cloud Run.",
    "CI/CD": "Learn to set up a basic pipeline using GitHub Actions or GitLab CI for automated testing/deployment.",
    "GraphQL": "Learn GraphQL schema design, queries/mutations, and how it differs from REST.",
    "Redis": "Learn Redis basics: caching strategies, key-value operations, and pub/sub.",
    "MongoDB": "Learn MongoDB basics: documents, collections, and when to use NoSQL vs SQL.",
    "PostgreSQL": "Strengthen SQL fundamentals and PostgreSQL-specific features like JSONB and indexing.",
    "OAuth": "Learn OAuth2 flow (authorization code grant) and how it differs from simple JWT auth.",
    "Microservices": "Study microservices patterns: service boundaries, API gateways, and inter-service communication.",
    "TypeScript": "Learn TypeScript basics: types, interfaces, and how it layers on top of JavaScript.",
    "React": "Build a small project with React: components, hooks (useState/useEffect), and props.",
    "Angular": "Learn Angular fundamentals: components, services, and dependency injection.",
    "Django": "Learn Django basics: models, views, templates, and the Django ORM.",
    "Spring Boot": "Learn Spring Boot fundamentals: REST controllers, dependency injection, and Spring Data JPA.",
    "Go": "Learn Go basics: goroutines, channels, and simple REST API building with net/http.",
    "Machine Learning": "Learn core ML concepts: supervised vs unsupervised learning, train/test splits, basic scikit-learn workflows.",
    "NLP": "Learn NLP basics: tokenization, embeddings, and using libraries like spaCy or Hugging Face transformers.",
    "Pytest": "Learn to write unit tests with pytest: fixtures, assertions, and test organization.",
    "WebSockets": "Learn WebSocket basics for real-time communication, e.g. using FastAPI's WebSocket support.",
}

DEFAULT_RECOMMENDATION = "Review this skill's fundamentals and try building a small project that uses it."


def get_recommendation(skill_name: str) -> str:
    return RECOMMENDATIONS.get(skill_name, DEFAULT_RECOMMENDATION)