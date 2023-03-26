import os
from dotenv import load_dotenv
from linkedin_api import Linkedin
import json

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

load_dotenv()
api = Linkedin(os.environ['LINKEDIN_EMAIL'], os.environ['LINKEDIN_PASSWORD'])
print(get_job_data("software", 3))
