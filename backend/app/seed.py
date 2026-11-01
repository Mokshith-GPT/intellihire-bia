from sqlalchemy.orm import Session
from .models import Candidate
from .analytics import readiness_score, readiness_status, recommendations

SAMPLE = [
(1001,'Aarav Sharma','Data Analyst','Analytics',2,88,82,91,86,{'Python':91,'SQL':78,'PowerBI':88,'Statistics':84,'Communication':86}),
(1002,'Diya Reddy','ML Engineer','Engineering',1,76,89,72,83,{'Python':88,'SQL':65,'MachineLearning':72,'Statistics':81,'Communication':83}),
(1003,'Ishaan Patel','Business Analyst','Analytics',3,92,74,68,90,{'Excel':92,'SQL':70,'PowerBI':85,'Statistics':68,'Communication':90}),
(1004,'Meera Nair','Data Analyst','Analytics',2,64,58,61,72,{'Python':62,'SQL':58,'PowerBI':74,'Statistics':55,'Communication':72}),
(1005,'Kabir Singh','Software Engineer','Engineering',4,55,49,52,61,{'Python':50,'SQL':48,'Algorithms':55,'Testing':59,'Communication':61}),
(1006,'Ananya Iyer','ML Engineer','Engineering',3,94,92,96,89,{'Python':96,'SQL':87,'MachineLearning':95,'Statistics':93,'Communication':89}),
(1007,'Rohan Das','Business Analyst','Operations',1,71,66,74,69,{'Excel':78,'SQL':67,'PowerBI':72,'Statistics':65,'Communication':69}),
(1008,'Sara Khan','Data Analyst','Analytics',5,83,86,81,92,{'Python':82,'SQL':88,'PowerBI':84,'Statistics':79,'Communication':92}),
]

def seed_candidates(db: Session):
    if db.query(Candidate).count():
        return
    for row in SAMPLE:
        cid,name,role,dept,exp,res,ass,tech,hr,skills = row
        payload = dict(resume_score=res, assessment_score=ass, technical_score=tech, hr_score=hr)
        db.add(Candidate(id=cid,name=name,role=role,department=dept,experience=exp,
            resume_score=res,assessment_score=ass,technical_score=tech,hr_score=hr,
            skills=skills,recommendations=recommendations(skills)))
    db.commit()
