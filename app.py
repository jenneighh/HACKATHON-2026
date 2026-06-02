from flask import Flask, render_template, request, jsonify, session
import anthropic
import os
import json
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

client = anthropic.AnthropicBedrock(
    aws_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    aws_region="us-east-1",
)

# STEM Career Database with detailed information
STEM_CAREERS = {
    "software_engineer": {
        "title": "Software Engineer",
        "description": "Design, develop, and maintain software applications and systems",
        "skills": ["programming", "problem-solving", "logical thinking", "creativity"],
        "subjects": ["computer science", "mathematics", "logic"],
        "salary_range": "$80k - $180k+",
        "growth": "High (22% projected growth)",
        "education": "Bachelor's in Computer Science or related field"
    },
    "data_scientist": {
        "title": "Data Scientist",
        "description": "Analyze complex data to help organizations make better decisions",
        "skills": ["statistics", "programming", "analytics", "communication"],
        "subjects": ["mathematics", "statistics", "computer science"],
        "salary_range": "$95k - $165k+",
        "growth": "Very High (36% projected growth)",
        "education": "Bachelor's/Master's in Data Science, Statistics, or related field"
    },
    "biomedical_engineer": {
        "title": "Biomedical Engineer",
        "description": "Combine engineering principles with medical sciences to design healthcare solutions",
        "skills": ["biology", "engineering", "problem-solving", "innovation"],
        "subjects": ["biology", "physics", "mathematics", "chemistry"],
        "salary_range": "$65k - $120k",
        "growth": "High (10% projected growth)",
        "education": "Bachelor's in Biomedical Engineering"
    },
    "environmental_scientist": {
        "title": "Environmental Scientist",
        "description": "Study the environment and develop solutions to environmental problems",
        "skills": ["research", "analysis", "fieldwork", "communication"],
        "subjects": ["environmental science", "biology", "chemistry", "earth science"],
        "salary_range": "$50k - $95k",
        "growth": "Moderate (6% projected growth)",
        "education": "Bachelor's in Environmental Science or related field"
    },
    "mechanical_engineer": {
        "title": "Mechanical Engineer",
        "description": "Design, develop, and test mechanical systems and devices",
        "skills": ["design", "mathematics", "physics", "problem-solving"],
        "subjects": ["physics", "mathematics", "engineering"],
        "salary_range": "$70k - $130k",
        "growth": "Moderate (6% projected growth)",
        "education": "Bachelor's in Mechanical Engineering"
    },
    "cybersecurity_analyst": {
        "title": "Cybersecurity Analyst",
        "description": "Protect computer systems and networks from cyber threats",
        "skills": ["security", "problem-solving", "technical skills", "attention to detail"],
        "subjects": ["computer science", "information security", "networking"],
        "salary_range": "$75k - $150k+",
        "growth": "Very High (33% projected growth)",
        "education": "Bachelor's in Cybersecurity, Computer Science, or related field"
    },
    "aerospace_engineer": {
        "title": "Aerospace Engineer",
        "description": "Design aircraft, spacecraft, satellites, and missiles",
        "skills": ["mathematics", "physics", "design", "problem-solving"],
        "subjects": ["physics", "mathematics", "engineering"],
        "salary_range": "$80k - $145k",
        "growth": "Moderate (6% projected growth)",
        "education": "Bachelor's in Aerospace Engineering"
    },
    "ux_designer": {
        "title": "UX/UI Designer",
        "description": "Create user-friendly digital experiences and interfaces",
        "skills": ["design", "creativity", "empathy", "technical skills"],
        "subjects": ["design", "psychology", "computer science"],
        "salary_range": "$65k - $135k",
        "growth": "High (16% projected growth)",
        "education": "Bachelor's in Design, HCI, or related field"
    }
}

# Role Models Database - diverse STEM professionals
ROLE_MODELS = [
    {
        "name": "Dr. Mae Jemison",
        "career": "aerospace_engineer",
        "title": "Astronaut & Engineer",
        "background": "First African American woman in space",
        "quote": "Never limit yourself because of others' limited imagination.",
        "ethnicity": "African American",
        "gender": "Female"
    },
    {
        "name": "Grace Hopper",
        "career": "software_engineer",
        "title": "Computer Scientist & Naval Officer",
        "background": "Pioneered computer programming and created the first compiler",
        "quote": "The most dangerous phrase is: 'We've always done it this way.'",
        "ethnicity": "Caucasian",
        "gender": "Female"
    },
    {
        "name": "Neil deGrasse Tyson",
        "career": "environmental_scientist",
        "title": "Astrophysicist & Science Communicator",
        "background": "Director of Hayden Planetarium, popular science educator",
        "quote": "The good thing about science is that it's true whether or not you believe in it.",
        "ethnicity": "African American",
        "gender": "Male"
    },
    {
        "name": "Katherine Johnson",
        "career": "data_scientist",
        "title": "Mathematician & NASA Scientist",
        "background": "Calculated flight trajectories for NASA space missions",
        "quote": "I counted everything. I counted the steps, the dishes, the stars in the sky.",
        "ethnicity": "African American",
        "gender": "Female"
    },
    {
        "name": "Ellen Ochoa",
        "career": "aerospace_engineer",
        "title": "Astronaut & Engineer",
        "background": "First Hispanic woman to go to space, former NASA Director",
        "quote": "Don't be afraid to reach for the stars.",
        "ethnicity": "Hispanic",
        "gender": "Female"
    },
    {
        "name": "Fei-Fei Li",
        "career": "data_scientist",
        "title": "AI Researcher & Professor",
        "background": "Co-director of Stanford Human-Centered AI Institute",
        "quote": "AI is not just a technology, it's a way to amplify human potential.",
        "ethnicity": "Asian",
        "gender": "Female"
    },
    {
        "name": "Marc Hannah",
        "career": "software_engineer",
        "title": "Computer Graphics Pioneer",
        "background": "Co-founded Silicon Graphics Inc., revolutionized 3D graphics",
        "quote": "Innovation comes from understanding what people need.",
        "ethnicity": "African American",
        "gender": "Male"
    },
    {
        "name": "Aprille Ericsson",
        "career": "aerospace_engineer",
        "title": "Aerospace Engineer",
        "background": "First African American woman to receive a PhD in Mechanical Engineering from NASA",
        "quote": "If you can see it, you can be it.",
        "ethnicity": "African American",
        "gender": "Female"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/careers")
def careers():
    return render_template("careers.html", careers=STEM_CAREERS)

@app.route("/role-models")
def role_models():
    return render_template("role_models.html", role_models=ROLE_MODELS)

@app.route("/api/match-careers", methods=["POST"])
def match_careers():
    try:
        data = request.get_json()

        # Build a detailed prompt for Claude
        prompt = f"""You are a STEM career counselor helping a student find their ideal career path.

Student Profile:
- Interests: {', '.join(data.get('interests', []))}
- Favorite Subjects: {', '.join(data.get('subjects', []))}
- Skills: {', '.join(data.get('skills', []))}
- Work Environment Preference: {data.get('environment', 'Not specified')}
- Goals: {data.get('goals', 'Not specified')}

Available STEM Careers:
{json.dumps(STEM_CAREERS, indent=2)}

Based on this student's profile, recommend the top 3 most suitable STEM careers from the list above. For each recommendation:
1. Explain why it's a good match (2-3 sentences)
2. Highlight how their interests and skills align
3. Provide encouragement and next steps

Format your response as JSON with this structure:
{{
  "matches": [
    {{
      "career_id": "career_key_from_database",
      "match_score": 95,
      "why_good_fit": "explanation here",
      "next_steps": "what they should do to explore this path"
    }}
  ],
  "overall_message": "encouraging message for the student"
}}

Be enthusiastic, encouraging, and specific. Remember this is for a student exploring their future!"""

        response = client.messages.create(
            model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.content[0].text

        # Try to parse JSON from the response
        try:
            # Extract JSON if it's wrapped in markdown code blocks
            if "```json" in reply:
                json_start = reply.find("```json") + 7
                json_end = reply.find("```", json_start)
                reply = reply[json_start:json_end].strip()
            elif "```" in reply:
                json_start = reply.find("```") + 3
                json_end = reply.find("```", json_start)
                reply = reply[json_start:json_end].strip()

            result = json.loads(reply)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response
            result = {
                "matches": [
                    {
                        "career_id": "software_engineer",
                        "match_score": 85,
                        "why_good_fit": "Based on your interests, this career would be a great fit!",
                        "next_steps": reply
                    }
                ],
                "overall_message": "You have great potential in STEM!"
            }

        # Enhance matches with full career data
        enhanced_matches = []
        for match in result.get("matches", []):
            career_id = match.get("career_id")
            if career_id in STEM_CAREERS:
                enhanced_match = {**match, **STEM_CAREERS[career_id]}

                # Find relevant role models
                relevant_role_models = [
                    rm for rm in ROLE_MODELS
                    if rm["career"] == career_id
                ]
                enhanced_match["role_models"] = relevant_role_models
                enhanced_matches.append(enhanced_match)

        result["matches"] = enhanced_matches

        # Store in session
        session['quiz_results'] = data
        session['career_matches'] = result

        return jsonify(result)

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]
        career_context = data.get("career_context", "")

        prompt = f"""You are a friendly STEM career counselor chatting with a student.
Be encouraging, informative, and relatable. Keep responses conversational and not too long.

{f"Context: The student is exploring {career_context}" if career_context else ""}

Student: {user_message}"""

        response = client.messages.create(
            model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.content[0].text
        return jsonify({"response": reply})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
