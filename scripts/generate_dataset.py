"""Generate a reproducible synthetic CSV for offline analysis exercises."""
import csv, random
random.seed(27)
roles = ["Data Analyst", "ML Engineer", "Business Analyst", "Software Engineer"]
with open("candidate_sample.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["candidate_id","role","experience_years","resume_score","assessment_score","technical_score","hr_score"])
    for i in range(1, 1001):
        writer.writerow([i, random.choice(roles), random.randint(0, 8), *[random.randint(35, 100) for _ in range(4)]])
print("Created candidate_sample.csv (synthetic data)")
