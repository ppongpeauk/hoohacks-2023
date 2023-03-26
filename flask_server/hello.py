from flask import Flask, request
import os
from dotenv import load_dotenv
from linkedin_api import Linkedin
import json

app = Flask(__name__)
load_dotenv()
api = Linkedin(os.environ['LINKEDIN_EMAIL'], os.environ['LINKEDIN_PASSWORD'])

@app.route('/job-data')
def hello():
    keywords = request.args.get('keywords')
    limit = int(request.args.get('limit'))
    return get_job_data(keywords, limit)

def get_job_data(keywords, limit):
    results = api.search_jobs(keywords=keywords, limit=limit)
    jobs = []
    for result in results:
        job = {}
        job_id = result["dashEntityUrn"][22:]
        title = result["title"]
        job_info = api.get_job(job_id)
        description = job_info["description"]["text"]
        company_name = job_info["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["name"]
        
        job["title"] = title
        job["company_name"] = company_name
        job["description"] = description
        jobs.append(job)
    
    return jobs
