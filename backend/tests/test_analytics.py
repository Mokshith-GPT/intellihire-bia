import pytest
from app.analytics import readiness_score, readiness_status

def test_weighted_score():
    assert readiness_score({"resume_score":85,"assessment_score":78,"technical_score":90,"hr_score":80}) == 84.0

def test_missing_evidence_rejected():
    with pytest.raises(ValueError): readiness_score({"resume_score":90})

def test_out_of_range_rejected():
    with pytest.raises(ValueError): readiness_score({"resume_score":120,"assessment_score":80,"technical_score":80,"hr_score":80})

def test_status_bands():
    assert readiness_status(80)=="Ready"
    assert readiness_status(79.9)=="Needs Improvement"
    assert readiness_status(59)=="Not Ready"
