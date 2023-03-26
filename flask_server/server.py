from flask import Flask, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from linkedin_api import Linkedin
from werkzeug.utils import secure_filename

from PyPDF2 import PdfReader
import openai

import re

import json

app = Flask(__name__)
CORS(app)

load_dotenv()
linkedin_api = Linkedin(os.environ['LINKEDIN_EMAIL'], os.environ['LINKEDIN_PASSWORD'])
openai.api_key = os.environ['OPENAI_API_KEY']

UPLOAD_FOLDER = "./uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USE_SAMPLE_DATA = False

@app.route('/api/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        file = request.files['file']
        pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(pdf_file_path)

        print("Extracting keywords from PDF")
        keywords = get_keywords(pdf_file_path, USE_SAMPLE_DATA)

        print("Pulling jobs from LinkedIn")
        jobs = get_job_data("software engineer", 5, USE_SAMPLE_DATA)

        rank_jobs_by_keywords(keywords, jobs)

        # remove "description" key from jobs
        for job in jobs:
            del job["description"]

        result = {}
        result["resumeParsedData"] = {"skills": keywords}
        result["jobResults"] = jobs
        result = json.dumps(result)
        try:
            os.remove(pdf_file_path)
        except Exception:
            pass
        
        return result
    return "Not a POST request"

def get_keywords(pdf_file_path, use_sample_data=True):
    keywords = None
    if not use_sample_data:
        logs = [
                {
                "role": "system",
                "content": """
                From now on, I will give you a resume in plain-text. You must respond to it in JSON format. I want you to return a dictionary with one key: skills. The skills value will be a list of technical skills, soft skills or relevant coursework in the resume.
                Ex: {"skills": ["python", "data structures"]}
                """
                },
            ]

        get_input = getText(pdf_file_path)

        logs.append({"role": "user", "content": get_input})
        res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=logs
        )
        logs.append(res["choices"][0]["message"])
        result = res["choices"][0]["message"]["content"]

        # save keyword data to sample_keywords.json
        file = open("sample_keywords.json", "w")
        file.write(result)
        keywords = json.loads(result)["skills"]
        file.close()
    else:
        file = open("sample_keywords.json", "r")
        keywords = json.load(file)["skills"]
        file.close()
    
    return keywords

def getText(pdfpath):
    
    pdf = PdfReader(pdfpath)

    number_of_pages = len(pdf.pages)
    pdf_text = []

    for page_number in range(number_of_pages):
        page = pdf.pages[page_number]
        page_content = page.extract_text()
        page_content = page_content.replace('\n', '')
        pdf_text.append(page_content)
    return "".join(pdf_text)

def get_job_data(keywords, limit, use_sample_data=True):
    jobs = None
    if not use_sample_data:
        results = linkedin_api.search_jobs(keywords=keywords, limit=limit)
        jobs = []
        for result in results:
            job = {}
            job_id = result["dashEntityUrn"][22:]
            title = result["title"]
            job_info = linkedin_api.get_job(job_id)
            description = job_info["description"]["text"]
            company = job_info["companyDetails"]["com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"]["companyResolutionResult"]["name"]
            location = job_info["formattedLocation"]

            applyMethod = job_info["applyMethod"]
            applicationLink = ""
            if "com.linkedin.voyager.jobs.ComplexOnsiteApply" in applyMethod.keys():
                applicationLink = applyMethod["com.linkedin.voyager.jobs.ComplexOnsiteApply"]["easyApplyUrl"]
            elif "com.linkedin.voyager.jobs.OffsiteApply" in applyMethod.keys():
                applicationLink = applyMethod["com.linkedin.voyager.jobs.OffsiteApply"]["companyApplyUrl"]
            
            job["title"] = title
            job["company"] = company
            job["description"] = description
            job["location"] = location
            job["applicationLink"] = applicationLink
            jobs.append(job)

        # save job data to sample_jobs.json
        json_save = {}
        json_save["jobs"] = jobs
        file = open("sample_jobs.json", "w")
        file.write(json.dumps(json_save))
        file.close()
    else:
        file = open("sample_jobs.json", "r")
        jobs = json.load(file)["jobs"]
        file.close()

    return jobs

def rank_jobs_by_keywords(keywords, jobs):
    # find and add matching keywords to jobs
    for job in jobs:
        skills = []
        for keyword in keywords:
            description = job["description"]
            if re.search(re.escape(keyword), description, re.IGNORECASE):
                skills.append(keyword)
        job["matchedAttributes"] = {"skills" : skills}
    
    # sort jobs by most number of matching keywords
    jobs.sort(key=lambda job: len(job["matchedAttributes"]["skills"]), reverse=True)