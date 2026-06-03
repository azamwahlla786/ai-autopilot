import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Isse frontend aur backend bina security error ke connect ho jate hain

# ==========================================
# ROUTE 1: LINKEDIN JOB SCRAPER
# ==========================================
def get_linkedin_jobs(keyword="Python Developer", location="Pakistan", limit=5):
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location={location}&start=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('li')
        
        extracted_jobs = []
        for index, card in enumerate(cards):
            if len(extracted_jobs) >= limit:
                break
            try:
                title_el = card.find('h3', class_='base-search-card__title')
                company_el = card.find('h4', class_='base-search-card__subtitle')
                location_el = card.find('span', class_='job-search-card__location')
                link_el = card.find('a', class_='base-card__full-link')
                
                if title_el and company_el:
                    title_text = title_el.text.strip()
                    # Profile Match Score Simulation
                    match_score = 95 if "Python" in title_text or "Azure" in title_text else 82
                    
                    extracted_jobs.append({
                        "id": index + 1,
                        "title": title_text,
                        "company": company_el.text.strip(),
                        "location": location_el.text.strip() if location_el else location,
                        "link": link_el['href'] if link_el else "#",
                        "platform": "LinkedIn",
                        "match_score": match_score
                    })
            except Exception:
                continue
        return extracted_jobs
    except Exception:
        return []

@app.route('/api/jobs', methods=['GET'])
def fetch_jobs_api():
    jobs_data = get_linkedin_jobs(keyword="Python Developer", location="Pakistan", limit=5)
    return jsonify(jobs_data)


# ==========================================
# ROUTE 2: COVER LETTER GENERATOR
# ==========================================
@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    data = request.json
    title = data.get("title", "Software Engineer")
    company = data.get("company", "Enterprise Corp")
    specs = data.get("specs", "")

    letter_content = f"""
[YOUR NAME]
Candidate ID: AI-AUTOPILOT-VIP

To,
The Hiring Committee,
{company}

Subject: Application for the Position of {title}

Dear Hiring Team,

I am writing to express my strong interest in the {title} role at {company}. With a deep focus on technical agility, automated architecture systems, and structured code logic, I am confident in my capability to optimize production pipelines within your enterprise matrix.

Regarding your specifications ({specs if specs else "Standard Enterprise Protocols"}), my core engineering background aligns perfectly with building resilient applications, managing cloud-native infrastructure, and writing pristine code structures.

Thank you for considering my application. I look forward to contributing to your dynamic deployment streams.

Sincerely,
Automated Candidate Core
    """
    return jsonify({"cover_letter": letter_content.strip()})


# ==========================================
# ROUTE 3: AI INTERVIEW SIMULATOR
# ==========================================
@app.route('/api/evaluate-interview', methods=['POST'])
def evaluate_interview():
    data = request.json
    user_response = data.get("response", "")

    if len(user_response.strip()) < 15:
        feedback = "Evaluation Matrix: Critical Alert. The provided response lacks the required technical depth and architectural vocabulary expected for enterprise optimization queries. Kindly expand on specific structural patterns."
        score = "45%"
    else:
        feedback = "Evaluation Matrix: Optimal Delivery. Your response demonstrates structural awareness, clear programmatic control structures, and an enterprise engineering mindset. Grammar and deployment tone are highly coherent."
        score = "88%"

    return jsonify({
        "feedback": feedback,
        "score": score
    })

if __name__ == "__main__":
    print("🚀 FYP Master Core Server Active on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    # ==========================================
# ROUTE 4: UPGRADED PREMIUM RESUME ENGINE
# ==========================================
@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    name = data.get("name", "Muhammad Azam").upper()
    title = data.get("title", "Software Engineer").upper()
    skills = data.get("skills", "")
    education = data.get("education", "")
    experience = data.get("experience", "")

    # Skills format
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    skills_html = "".join([f'<span style="background: #f1f5f9; color: #1e293b; padding: 4px 12px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; border: 1px solid #cbd5e1; display: inline-block; margin: 2px;">{skill}</span>' for skill in skills_list])

    resume_template = f"""
    <div id="printable-cv-area" style="font-family: 'Arial', sans-serif; color: #1e293b; background: #ffffff; padding: 2rem; border-radius: 4px; text-align: left; line-height: 1.5;">
        
        <div style="border-bottom: 2px solid #0284c7; padding-bottom: 1rem; margin-bottom: 1.5rem;">
            <h1 style="font-size: 2rem; color: #0f172a; margin: 0 0 0.25rem 0; font-weight: 800; letter-spacing: -0.5px;">{name}</h1>
            <p style="color: #0284c7; font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem 0; letter-spacing: 0.5px;">{title}</p>
        </div>

        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #0f172a; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 2px; font-weight: 700;">🎓 Education</h3>
            <p style="font-size: 0.95rem; color: #334155; margin: 0; font-weight: 600;">{education}</p>
        </div>

        <div style="margin-bottom: 1.5rem;">
            <h3 style="color: #0f172a; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 2px; font-weight: 700;">💼 Key Projects & Experience</h3>
            <p style="font-size: 0.95rem; line-height: 1.6; color: #334155; margin: 0; white-space: pre-line;">{experience if experience else "Developed integrated dynamic automation layers matching custom profile matrices with live web data streams safely."}</p>
        </div>

        <div style="margin-bottom: 1rem;">
            <h3 style="color: #0f172a; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.6rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 2px; font-weight: 700;">🛠️ Technical Competencies</h3>
            <div style="margin-top: 0.5rem;">
                {skills_html if skills else '<span style="color:#64748b; font-size:0.9rem;">No competencies declared.</span>'}
            </div>
        </div>

    </div>
    """
    return jsonify({"resume_html": resume_template})