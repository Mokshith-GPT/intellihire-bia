import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Candidate
from .seed import seed_candidates
from .analytics import readiness_score, readiness_status, recommendations
from .ml import train_demo_model

model, model_metrics = train_demo_model()

def candidate_dict(c):
    d = {"id":c.id,"name":c.name,"role":c.role,"department":c.department,"experience":c.experience,
         "resume_score":c.resume_score,"assessment_score":c.assessment_score,"technical_score":c.technical_score,"hr_score":c.hr_score,
         "skills":c.skills or {},"recommendations":c.recommendations or []}
    d["readiness_score"] = readiness_score(d)
    d["readiness_status"] = readiness_status(d["readiness_score"])
    return d

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    from .database import SessionLocal
    db = SessionLocal()
    try: seed_candidates(db)
    finally: db.close()
    yield

app = FastAPI(title="IntelliHire BIA API", version="1.0.0", description="Candidate readiness and hiring decision analytics prototype", lifespan=lifespan)
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET","POST"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status":"ok","service":"intellihire-api"}

@app.get("/api/candidates")
def list_candidates(db: Session = Depends(get_db)):
    return [candidate_dict(c) for c in db.query(Candidate).order_by(Candidate.id).all()]

@app.get("/api/candidates/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    c = db.get(Candidate, candidate_id)
    if not c: raise HTTPException(404, "Candidate not found")
    return candidate_dict(c)

@app.get("/api/analytics/overview")
def overview(db: Session = Depends(get_db)):
    rows = [candidate_dict(c) for c in db.query(Candidate).all()]
    if not rows: return {"total_candidates":0,"average_readiness":0,"ready_candidates":0,"stage_averages":{}}
    stages = ["resume_score","assessment_score","technical_score","hr_score"]
    return {"total_candidates":len(rows),"average_readiness":round(sum(r['readiness_score'] for r in rows)/len(rows),1),
            "ready_candidates":sum(r['readiness_status']=="Ready" for r in rows),
            "stage_averages":{k:round(sum(r[k] for r in rows)/len(rows),1) for k in stages}}

@app.get("/api/analytics/skills")
def skill_analytics(db: Session = Depends(get_db)):
    rows = [c.skills or {} for c in db.query(Candidate).all()]
    totals = {}
    counts = {}
    for row in rows:
        for key,value in row.items(): totals[key]=totals.get(key,0)+float(value); counts[key]=counts.get(key,0)+1
    return sorted([{"skill":k,"average":round(totals[k]/counts[k],1)} for k in totals], key=lambda x:x['average'])

@app.get("/api/analytics/compare")
def compare(ids: str, db: Session = Depends(get_db)):
    try: wanted = [int(x.strip()) for x in ids.split(",") if x.strip()]
    except ValueError: raise HTTPException(400,"ids must be comma-separated integers")
    if not wanted or len(wanted)>10: raise HTTPException(400,"Provide between 1 and 10 candidate IDs")
    rows = [candidate_dict(c) for c in db.query(Candidate).filter(Candidate.id.in_(wanted)).all()]
    return rows

@app.post("/api/predict/{candidate_id}")
def predict(candidate_id: int, db: Session = Depends(get_db)):
    c = db.get(Candidate,candidate_id)
    if not c: raise HTTPException(404,"Candidate not found")
    d=candidate_dict(c); features=[[d[k] for k in ("resume_score","assessment_score","technical_score","hr_score")]]
    probs=model.predict_proba(features)[0]
    return {"candidate_id":candidate_id,"prediction":str(model.predict(features)[0]),"class_probabilities":{str(k):round(float(v),3) for k,v in zip(model.classes_,probs)},"weighted_score":d['readiness_score'],"recommendations":recommendations(d['skills']),"model_note":model_metrics['note']}

@app.get("/api/model/metrics")
def metrics(): return model_metrics
