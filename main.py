from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from resume_parser import extract_text_from_pdf, extract_keywords
from collections import defaultdict

# === Header ===
print("="*60)
print("💼 CAREER MENTOR AI - Smart Resume to Job Matcher")
print("="*60)

# === Connect to MongoDB Atlas ===
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# === Step 1: Read Resume and Extract Keywords ===
resume_path = "RESUME_text.pdf"  # Make sure this file is uploaded
resume_text = extract_text_from_pdf(resume_path)
resume_keywords = extract_keywords(resume_text)

print("\n📄 Extracted Resume Keywords:")
print(", ".join(resume_keywords))

# === Step 2: Intelligent Job Matching ===
job_scores = defaultdict(int)

for word in resume_keywords:
    query = {
        "$or": [
            {"job_title": {"$regex": word, "$options": "i"}},
            {"job_description": {"$regex": word, "$options": "i"}},
            {"required_skills": {"$regex": word, "$options": "i"}}
        ]
    }
    results = collection.find(query)
    for job in results:
        key = f"{job.get('job_title')} at {job.get('company_name')}"
        job_scores[key] += 1

# === Step 3: Rank and Display Top Matches ===
sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)

print("\n🎯 Top Matching Jobs Based on Resume:\n")
if sorted_jobs:
    for i, (job, score) in enumerate(sorted_jobs, start=1):
        print(f"{i}. ✅ {job}  | Relevance Score: {score}")
else:
    print("⚠️ No matching jobs found. Try refining your resume or keywords.")

print(f"\n📌 Resume Keywords Matched: {len(resume_keywords)} | Total Jobs Found: {len(sorted_jobs)}")
print("="*60)
