# IntelliHire BIA — Full-Stack Prototype

A GitHub-ready prototype for **AI-Based Candidate Readiness & Hiring Decision Analytics**, aligned to the IntelliHire synopsis: resume/ATS, adaptive assessment, technical interview and HR/behavioral evidence are integrated into descriptive, diagnostic, predictive and prescriptive analytics.

## Architecture

- **Frontend:** React + TypeScript + Vite + Recharts. Deploys to GitHub Pages.
- **API:** FastAPI + Pydantic + SQLAlchemy. Runs locally or in Docker.
- **Database:** PostgreSQL via Docker Compose. SQLite is used automatically for a quick local demo if `DATABASE_URL` is not set.
- **Analytics:** Pandas/NumPy + transparent weighted readiness score.
- **ML:** Scikit-learn Random Forest baseline, trained from seeded synthetic data. Its output is explicitly a demonstration estimate, not a validated hiring outcome.

> GitHub Pages only hosts static files. It cannot run FastAPI or PostgreSQL. The Pages deployment therefore uses the frontend's demo mode by default. To use live API data, deploy the backend separately and set the `VITE_API_BASE_URL` repository variable to its HTTPS URL before building.

## Quick start (full stack)

Requirements: Docker Desktop and Git.

```bash
git clone https://github.com/<YOUR-USER>/intellihire-bia.git
cd intellihire-bia
docker compose up --build
```

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

For development without Docker:

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend falls back to a bundled demo dataset if the API is unavailable.

## GitHub Pages deployment

1. Create a GitHub repository named `intellihire-bia` and push this project to its default branch (`main`).
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
3. The included `.github/workflows/deploy-pages.yml` builds and deploys the Vite frontend on every push to `main`.
4. Optional live backend: deploy `backend/` + PostgreSQL on a host that supports containers. In **Settings → Secrets and variables → Actions → Variables**, add `VITE_API_BASE_URL` with the backend HTTPS base URL (no trailing slash). Push again to rebuild the frontend.

The workflow grants only the Pages deployment permissions it needs. The `frontend/vite.config.ts` uses the repository name as the Pages base path; change `base` if your repository has a different name or is a user/org site.

## Main features

- Executive overview: candidate count, average readiness, ready share and evaluation-stage averages.
- Candidate explorer with search and readiness filters.
- Candidate detail with four-stage evidence, skill profile and gap priorities.
- Candidate comparison.
- Transparent readiness score and rule-based next-step recommendations.
- ML baseline endpoint and model metrics for experimentation.
- API health and OpenAPI documentation.

## Readiness score

Default prototype weights: resume 20%, assessment 25%, technical 35%, HR/behavioral 20%. The weights and thresholds are configurable in `backend/app/analytics.py`. The sample labels and scores are synthetic and are not empirical hiring standards.

Readiness bands (demo defaults):
- Ready: score >= 80
- Needs Improvement: 60–79.99
- Not Ready: below 60

The score is decision support only. Do not use it as an automated rejection/selection mechanism. Validate criteria for the relevant role, audit for disparate impact, and require human review before any consequential decision.

## API endpoints

- `GET /health`
- `GET /api/candidates`
- `GET /api/candidates/{candidate_id}`
- `GET /api/analytics/overview`
- `GET /api/analytics/skills`
- `GET /api/analytics/compare?ids=1,2,3`
- `POST /api/predict/{candidate_id}`
- `GET /api/model/metrics`

## Repository layout

```text
.github/workflows/   CI checks and GitHub Pages deployment
frontend/            React + TypeScript + Vite application
backend/app/         FastAPI, SQLAlchemy, analytics and ML
backend/tests/       API and scoring tests
database/            PostgreSQL initialization SQL
scripts/             Synthetic data generator
compose.yaml         Local full-stack environment
```

## Data and model notes

`backend/app/seed.py` creates a reproducible synthetic candidate dataset on first startup. The Random Forest demonstration model is trained against a synthetic readiness label derived from the same evaluation dimensions; consequently, its metrics are illustrative only and do **not** establish real-world predictive validity. For a defensible predictive study, replace these labels with independently observed outcomes, define a suitable prediction horizon, use leakage-safe temporal/group splits, and report calibration and subgroup performance.

## License

Educational prototype. Review and add an institutional/project-specific license before public redistribution.
