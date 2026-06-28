# config.md — Business Configuration (primary reference)

> Declarative business configuration for the platform. **Secrets live only in `.env`, never here.**
> Profiles: development / testing / production. Business logic must stay provider-agnostic.

## active_profile
development

## profiles

### development
- app_name: Agentic AI Strategic Governance Platform
- mode: development
- version: 0.1.0
- llm_provider: groq
- llm_model: llama-3.3-70b-versatile
- embedding_provider: sentence-transformer   # local; or "openai"
- embedding_model: all-MiniLM-L6-v2
- database_url: sqlite:///./app_dev.db
- vector_store: chroma                        # or "keyword" fallback for V1
- cors_origins: ["http://localhost:5173"]

### testing
- app_name: Agentic AI Strategic Governance Platform
- mode: testing
- version: 0.1.0
- llm_provider: groq                          # or "mock"
- embedding_provider: sentence-transformer
- database_url: sqlite:///./app_test.db
- vector_store: keyword
- cors_origins: ["http://localhost:5173"]

### production
- app_name: Agentic AI Strategic Governance Platform
- mode: production
- version: 0.1.0
- llm_provider: openai                        # or "anthropic"
- llm_model: gpt-4o
- embedding_provider: openai
- embedding_model: text-embedding-3-large
- database_url: postgresql+psycopg://USER:PASS@HOST:5432/govdb   # creds via .env
- vector_store: pgvector
- cors_origins: ["https://<approved-production-origin>"]
- https_required: true
- encrypt_at_rest: true

> NOTE: CP1 reads only app_name / mode / version for the health endpoint. Provider, DB and vector
> settings are wired in later coding prompts (CP2/CP3+). No secrets in this file.
