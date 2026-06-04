from flask import Flask, render_template, request, jsonify, session
import os
import json
from dotenv import load_dotenv
from datetime import timedelta
import anthropic

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# STEM Career Database with detailed information
STEM_CAREERS = {
    "software_engineer": {
        "title": "Software Engineer",
        "description": "Design, develop, and maintain software applications and systems",
        "skills": ["programming", "problem-solving", "logical thinking", "creativity"],
        "subjects": ["computer science", "mathematics", "logic"],
        "salary_range": "$80,000 - $180,000+",
        "avg_salary": "$120,000",
        "growth": "High (22% projected growth)",
        "education": "Bachelor's in Computer Science or related field",
        "impact": "Create apps and software used by millions of people worldwide",
        "day_in_life": "Write code, debug programs, collaborate with designers, attend team meetings, and solve technical challenges",
        "beginner_projects": ["Build a personal website", "Create a mobile app", "Contribute to open source projects"],
        "next_steps": ["Learn Python or JavaScript", "Complete online coding courses", "Build a portfolio of projects"]
    },
    "biomedical_engineer": {
        "title": "Biomedical Engineer",
        "description": "Combine engineering principles with medical sciences to design healthcare solutions",
        "skills": ["biology", "engineering", "problem-solving", "innovation"],
        "subjects": ["biology", "physics", "mathematics", "chemistry"],
        "salary_range": "$65,000 - $120,000",
        "avg_salary": "$92,000",
        "growth": "High (10% projected growth)",
        "education": "Bachelor's in Biomedical Engineering",
        "impact": "Design medical devices and technologies that save lives and improve healthcare",
        "day_in_life": "Design prosthetics, test medical equipment, collaborate with doctors, research new technologies",
        "beginner_projects": ["Build a simple heart rate monitor", "Design a 3D-printed prosthetic", "Create health tracking apps"],
        "next_steps": ["Take biology and physics courses", "Join robotics or engineering clubs", "Shadow a biomedical engineer"]
    },
    "cybersecurity_analyst": {
        "title": "Cybersecurity Analyst",
        "description": "Protect computer systems and networks from cyber threats and hackers",
        "skills": ["security", "problem-solving", "technical skills", "attention to detail"],
        "subjects": ["computer science", "information security", "networking"],
        "salary_range": "$75,000 - $150,000+",
        "avg_salary": "$105,000",
        "growth": "Very High (33% projected growth)",
        "education": "Bachelor's in Cybersecurity, Computer Science, or related field",
        "impact": "Protect companies and individuals from cyber attacks and keep data safe",
        "day_in_life": "Monitor networks for threats, investigate security breaches, implement security measures, train employees",
        "beginner_projects": ["Learn ethical hacking basics", "Set up a secure home network", "Complete cybersecurity challenges"],
        "next_steps": ["Learn networking fundamentals", "Study encryption and security", "Practice on platforms like TryHackMe"]
    },
    "computer_science_engineer": {
        "title": "Computer Science Engineer",
        "description": "Develop innovative computing solutions and advance technology through research and development",
        "skills": ["algorithms", "system design", "programming", "mathematics"],
        "subjects": ["computer science", "mathematics", "engineering", "logic"],
        "salary_range": "$85,000 - $175,000+",
        "avg_salary": "$125,000",
        "growth": "Very High (25% projected growth)",
        "education": "Bachelor's in Computer Science or Computer Engineering",
        "impact": "Build the future of technology, from AI to quantum computing",
        "day_in_life": "Develop algorithms, optimize systems, research new technologies, collaborate on innovative projects",
        "beginner_projects": ["Build an AI chatbot", "Create a machine learning model", "Design efficient algorithms"],
        "next_steps": ["Master data structures and algorithms", "Learn multiple programming languages", "Participate in coding competitions"]
    },
    "aerospace_engineer": {
        "title": "Aerospace Engineer",
        "description": "Design aircraft, spacecraft, satellites, and technology that explores the universe",
        "skills": ["mathematics", "physics", "design", "problem-solving"],
        "subjects": ["physics", "mathematics", "engineering"],
        "salary_range": "$80,000 - $145,000",
        "avg_salary": "$118,000",
        "growth": "Moderate (6% projected growth)",
        "education": "Bachelor's in Aerospace Engineering",
        "impact": "Help humanity explore space and advance aviation technology",
        "day_in_life": "Design aircraft components, run simulations, test prototypes, work with NASA or aerospace companies",
        "beginner_projects": ["Build and launch model rockets", "Design paper airplanes and test aerodynamics", "Use flight simulators"],
        "next_steps": ["Excel in physics and calculus", "Join rocketry or aviation clubs", "Learn CAD software for design"]
    }
}

# Role Models Database - diverse STEM professionals
ROLE_MODELS = [
    {
        "name": "Dr. Mae Jemison",
        "career": "aerospace_engineer",
        "title": "Astronaut & Engineer",
        "background": "First African American woman in space. She flew on the Space Shuttle Endeavour in 1992 and has since worked on advancing science education.",
        "quote": "Never limit yourself because of others' limited imagination.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "Faced discrimination in STEM but persevered through determination and excellence",
        "advice": "Don't let anyone define what you can achieve. Your background is your strength, not a limitation.",
        "what_students_learn": "How to break barriers in space exploration and inspire the next generation of astronauts"
    },
    {
        "name": "Grace Hopper",
        "career": "software_engineer",
        "title": "Computer Scientist & Naval Officer",
        "background": "Pioneered computer programming and created the first compiler. Known as the 'Queen of Code,' she revolutionized how we program computers.",
        "quote": "The most dangerous phrase is: 'We've always done it this way.'",
        "ethnicity": "Caucasian",
        "gender": "Female",
        "challenges": "Worked in a male-dominated field and had to prove herself constantly",
        "advice": "Be innovative and don't be afraid to challenge the status quo. The best solutions come from thinking differently.",
        "what_students_learn": "Programming fundamentals and how to innovate in technology"
    },
    {
        "name": "Katherine Johnson",
        "career": "computer_science_engineer",
        "title": "Mathematician & NASA Scientist",
        "background": "Her precise calculations of orbital mechanics were critical to the success of NASA's first manned spaceflights.",
        "quote": "I counted everything. I counted the steps, the dishes, the stars in the sky.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "Overcame racial and gender barriers in the 1960s to become essential to NASA",
        "advice": "Love mathematics and never stop learning. Your skills are valuable, even when others don't see it.",
        "what_students_learn": "Advanced mathematics and computational problem-solving for space missions"
    },
    {
        "name": "Ellen Ochoa",
        "career": "aerospace_engineer",
        "title": "Astronaut & Former NASA Director",
        "background": "First Hispanic woman to go to space. Flew on four shuttle missions and later became Director of Johnson Space Center.",
        "quote": "Don't be afraid to reach for the stars.",
        "ethnicity": "Hispanic",
        "gender": "Female",
        "challenges": "As a first-generation college student, had to navigate higher education without family guidance",
        "advice": "Education opens doors. Stay curious and keep pursuing your dreams, no matter the obstacles.",
        "what_students_learn": "Leadership in aerospace and how to achieve ambitious goals"
    },
    {
        "name": "Fei-Fei Li",
        "career": "computer_science_engineer",
        "title": "AI Researcher & Professor",
        "background": "Co-director of Stanford Human-Centered AI Institute. Pioneer in computer vision and AI ethics.",
        "quote": "AI is not just a technology, it's a way to amplify human potential.",
        "ethnicity": "Asian",
        "gender": "Female",
        "challenges": "Immigrated to the US and worked multiple jobs while pursuing her education",
        "advice": "Combine technical excellence with empathy. The best AI serves humanity.",
        "what_students_learn": "Artificial intelligence, machine learning, and ethical technology development"
    },
    {
        "name": "Marc Hannah",
        "career": "software_engineer",
        "title": "Computer Graphics Pioneer",
        "background": "Co-founded Silicon Graphics Inc., revolutionizing 3D graphics used in movies, video games, and scientific visualization.",
        "quote": "Innovation comes from understanding what people need.",
        "ethnicity": "African American",
        "gender": "Male",
        "challenges": "Had to fight for recognition in Silicon Valley's tech scene",
        "advice": "Focus on creating technology that solves real problems. Success follows impact.",
        "what_students_learn": "Computer graphics, entrepreneurship, and building groundbreaking technology"
    },
    {
        "name": "Aprille Ericsson",
        "career": "aerospace_engineer",
        "title": "Aerospace Engineer at NASA",
        "background": "First African American woman to receive a PhD in Mechanical Engineering from NASA. Designs spacecraft instruments.",
        "quote": "If you can see it, you can be it.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "Faced skepticism as a Black woman in engineering but excelled through dedication",
        "advice": "Representation matters. Be the role model you wish you had.",
        "what_students_learn": "Spacecraft design, mechanical engineering, and persistence in STEM"
    },
    {
        "name": "José Hernández",
        "career": "aerospace_engineer",
        "title": "Astronaut & Engineer",
        "background": "Former migrant farmworker who became a NASA astronaut. Flew on the Space Shuttle Discovery in 2009.",
        "quote": "If you really want something, you have to be willing to sacrifice for it.",
        "ethnicity": "Hispanic",
        "gender": "Male",
        "challenges": "Grew up in poverty, working in fields, and learning English as a second language",
        "advice": "Your humble beginnings don't define your future. Hard work and education can take you to space.",
        "what_students_learn": "Aerospace engineering and how determination overcomes any obstacle"
    },
    {
        "name": "Kimberly Bryant",
        "career": "computer_science_engineer",
        "title": "Founder of Black Girls CODE",
        "background": "Electrical engineer who founded Black Girls CODE to teach programming to young girls of color.",
        "quote": "We need to show girls that technology is for them.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "Felt isolated as one of few Black women in tech and wanted to change that",
        "advice": "Use your skills to lift others up. Creating opportunities for others amplifies your impact.",
        "what_students_learn": "Software development, tech education, and community building"
    },
    {
        "name": "Dr. Ayanna Howard",
        "career": "biomedical_engineer",
        "title": "Roboticist & AI Expert",
        "background": "Develops robots for healthcare and rehabilitation. Former NASA researcher now creating assistive technologies.",
        "quote": "Robots can help people live better lives.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "Breaking into robotics as a Black woman and proving the value of human-centered design",
        "advice": "Use technology to help people. The most meaningful work solves human problems.",
        "what_students_learn": "Robotics, AI in healthcare, and assistive technology design"
    },
    {
        "name": "Reshma Saujani",
        "career": "computer_science_engineer",
        "title": "Founder of Girls Who Code",
        "background": "Lawyer turned tech advocate who founded Girls Who Code to close the gender gap in technology.",
        "quote": "Teach girls bravery, not perfection.",
        "ethnicity": "Asian American",
        "gender": "Female",
        "challenges": "Saw the lack of women in tech and decided to create systemic change",
        "advice": "Don't wait for permission to make a difference. Start where you are with what you have.",
        "what_students_learn": "Coding, leadership, and how to advocate for diversity in STEM"
    },
    {
        "name": "Dr. Jessica Esquivel",
        "career": "biomedical_engineer",
        "title": "Pediatric Neurosurgeon",
        "background": "One of the few Hispanic female neurosurgeons in the US. Operates on children with brain and spine conditions.",
        "quote": "Representation in medicine saves lives.",
        "ethnicity": "Hispanic",
        "gender": "Female",
        "challenges": "Navigated medical school as a first-generation student from an immigrant family",
        "advice": "Your unique perspective is needed in medicine. Patients deserve doctors who understand them.",
        "what_students_learn": "Biomedical science, surgery, and compassionate healthcare"
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

        # Check if API key is available
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        use_ai = api_key and api_key != "your_api_key_here"

        if use_ai:
            # Use AI for matching
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
                # Fallback to rule-based matching
                result = rule_based_matching(data)
        else:
            # Use rule-based matching when no API key
            result = rule_based_matching(data)

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

def rule_based_matching(data):
    """Simple rule-based career matching when AI is not available"""
    interests = data.get('interests', [])
    subjects = data.get('subjects', [])
    skills = data.get('skills', [])

    # Score each career based on matches
    scores = {}

    for career_id, career in STEM_CAREERS.items():
        score = 0
        reasons = []

        # Match interests
        interest_matches = sum(1 for interest in interests if interest in career.get('skills', []))
        score += interest_matches * 10

        # Match subjects
        subject_matches = sum(1 for subject in subjects if subject in career.get('subjects', []))
        score += subject_matches * 15

        # Match skills
        skill_matches = sum(1 for skill in skills if skill in career.get('skills', []))
        score += skill_matches * 10

        # Specific matching logic
        if 'coding' in interests or 'computer_science' in subjects:
            if career_id in ['software_engineer', 'computer_science_engineer', 'cybersecurity_analyst']:
                score += 20
                reasons.append("Your interest in coding and computer science aligns perfectly with this field")

        if 'biology' in subjects or 'helping' in interests:
            if career_id == 'biomedical_engineer':
                score += 20
                reasons.append("Your passion for biology and helping others makes you ideal for healthcare technology")

        if 'design' in interests or 'building' in interests:
            if career_id == 'aerospace_engineer':
                score += 15
                reasons.append("Your creativity and love for building things fits aerospace engineering")

        if 'problem_solving' in interests:
            score += 5
            reasons.append("Your problem-solving skills are valuable in this field")

        scores[career_id] = {
            'score': min(score, 98),  # Cap at 98
            'reasons': reasons
        }

    # Get top 3 careers
    top_careers = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)[:3]

    matches = []
    for career_id, data_dict in top_careers:
        match_score = data_dict['score']
        reasons = data_dict['reasons'] if data_dict['reasons'] else [
            "Your interests and skills show great potential for this career"
        ]

        matches.append({
            "career_id": career_id,
            "match_score": match_score,
            "why_good_fit": " ".join(reasons) + ". This career offers excellent opportunities for growth and making a real impact in the world.",
            "next_steps": f"Start by learning the fundamentals, join relevant clubs or online communities, and work on beginner projects to build your skills."
        })

    return {
        "matches": matches,
        "overall_message": f"Based on your interests in {', '.join(interests[:3])}, you have amazing potential in STEM! These careers align with your passions and can lead to a fulfilling future. Remember, every expert started as a beginner - your journey starts now!"
    }

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"].lower()

        # Simple demo chatbot responses (no AI needed for now)
        responses = {
            "hello": "Hi there! 👋 I'm your STEM Career Guide! Ask me anything about STEM careers, what classes to take, or how to get started!",
            "hi": "Hello! 👋 I'm here to help you explore STEM careers! What would you like to know?",
            "help": "I can help you with:\n• Finding STEM careers that fit you\n• What classes you should take\n• Whether you can do STEM (yes you can!)\n• Project ideas to get started\n\nWhat interests you?",
            "math": "Being 'bad at math' doesn't mean you can't do STEM! 💪 Many successful STEM professionals struggled with math at first. The key is practice and finding the right learning style. Plus, many STEM fields focus more on creativity and problem-solving than pure math. Would you like to know which STEM careers use less heavy math?",
            "career": "Great question! There are so many exciting STEM careers! 🚀 Based on your interests, I'd recommend taking our quiz to find your perfect match. We have careers in:\n• Software Engineering\n• Biomedical Engineering\n• Cybersecurity\n• Aerospace Engineering\n• And more!\n\nWhat are you passionate about?",
            "class": "For STEM careers, here are some key classes:\n📚 Essential: Math, Science, Computer Science\n💡 Helpful: Physics, Chemistry, Biology\n🎨 Bonus: Design, Statistics, Engineering\n\nStart with what interests you most! Which field are you curious about?",
            "project": "Here are some beginner-friendly STEM projects:\n• Build a personal website 💻\n• Create a simple robot 🤖\n• Design a mobile app 📱\n• Build a model rocket 🚀\n• Make a heart rate monitor ❤️\n\nPick something that excites you and start small!",
            "woman": "Absolutely! Women are making incredible contributions to STEM! 👩‍🔬 Check out our Role Models section to meet inspiring women like:\n• Dr. Mae Jemison (First Black woman in space)\n• Grace Hopper (Computer programming pioneer)\n• Ellen Ochoa (First Hispanic woman astronaut)\n\nYou belong in STEM!",
            "hispanic": "Yes! Hispanic and Latino students are thriving in STEM! 🌟 Check out role models like Ellen Ochoa, José Hernández, and Dr. Jessica Esquivel. Your cultural perspective is valuable and needed in STEM fields!",
            "first": "Being a first-generation college student in STEM is challenging but absolutely possible! 💪 Many successful STEM professionals were first-gen students. Look for mentors, join support groups, and remember: your unique perspective is an asset!",
            "start": "Getting started in STEM is exciting! Here's what to do:\n1. Explore different fields (take our quiz!)\n2. Start a small project in your area of interest\n3. Join a club or online community\n4. Find a mentor or role model\n5. Keep learning and stay curious!\n\nWhat field interests you most?",
        }

        # Find matching response
        response_text = None
        for keyword, response in responses.items():
            if keyword in user_message:
                response_text = response
                break

        # Default response
        if not response_text:
            response_text = "That's a great question! 🤔 I'm here to help you explore STEM careers. Try asking about:\n• What STEM career fits me?\n• What classes should I take?\n• Can I do STEM if I'm bad at math?\n• What projects should I try?\n• Are there role models like me?\n\nOr take our quiz to find your perfect STEM career match!"

        return jsonify({"response": response_text})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
