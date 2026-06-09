"""
SeeMe in STEM - Flask Web Application
======================================
This application helps students discover STEM careers through:
- AI-powered career matching based on interests and skills
- Diverse role models from various backgrounds
- Interactive chatbot for STEM questions
- Resources for summer camps, scholarships, and competitions
"""

# Import required libraries
from flask import Flask, render_template, request, jsonify, session
import os
import json
from dotenv import load_dotenv
from datetime import timedelta
import boto3

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Sessions last 2 hours

# Initialize AWS Bedrock client for chatbot functionality
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

# =============================================================================
# STEM CAREERS DATABASE
# =============================================================================
# Contains 17+ STEM careers with detailed information including:
# - Job descriptions, salary ranges, and growth projections
# - Required skills and education
# - Day-in-the-life examples
# - Beginner projects and next steps
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
    },
    "data_scientist": {
        "title": "Data Scientist",
        "description": "Analyze complex data to help organizations make better decisions and predictions",
        "skills": ["statistics", "programming", "critical thinking", "communication"],
        "subjects": ["mathematics", "statistics", "computer science"],
        "salary_range": "$85,000 - $160,000+",
        "avg_salary": "$120,000",
        "growth": "Very High (36% projected growth)",
        "education": "Bachelor's in Data Science, Statistics, or Computer Science",
        "impact": "Help solve real-world problems in healthcare, climate change, education, and social justice",
        "day_in_life": "Clean and analyze data, create visualizations, build predictive models, present findings to stakeholders",
        "beginner_projects": ["Analyze a dataset from Kaggle", "Create data visualizations", "Build a simple prediction model"],
        "next_steps": ["Learn Python and SQL", "Study statistics and probability", "Practice with real datasets online"]
    },
    "environmental_scientist": {
        "title": "Environmental Scientist",
        "description": "Protect the planet by studying environmental problems and developing solutions",
        "skills": ["research", "problem-solving", "passion for nature", "communication"],
        "subjects": ["biology", "chemistry", "earth science", "environmental studies"],
        "salary_range": "$50,000 - $95,000",
        "avg_salary": "$73,000",
        "growth": "High (8% projected growth)",
        "education": "Bachelor's in Environmental Science or related field",
        "impact": "Fight climate change, protect ecosystems, and create a sustainable future",
        "day_in_life": "Collect environmental samples, analyze pollution levels, research conservation methods, advise policymakers",
        "beginner_projects": ["Test water quality in local streams", "Start a recycling program", "Create a school garden"],
        "next_steps": ["Join environmental clubs", "Study ecology and earth science", "Volunteer for conservation projects"]
    },
    "mechanical_engineer": {
        "title": "Mechanical Engineer",
        "description": "Design and build machines, robots, engines, and mechanical systems",
        "skills": ["design", "problem-solving", "mathematics", "hands-on skills"],
        "subjects": ["physics", "mathematics", "engineering"],
        "salary_range": "$70,000 - $125,000",
        "avg_salary": "$92,000",
        "growth": "Moderate (10% projected growth)",
        "education": "Bachelor's in Mechanical Engineering",
        "impact": "Create innovative machines that improve daily life, from medical devices to renewable energy systems",
        "day_in_life": "Design mechanical systems, run simulations, test prototypes, work on manufacturing processes",
        "beginner_projects": ["Build a simple robot", "Design 3D-printed objects", "Create a Rube Goldberg machine"],
        "next_steps": ["Learn CAD software", "Join robotics or engineering clubs", "Experiment with building and tinkering"]
    },
    "ux_designer": {
        "title": "UX/UI Designer (Tech)",
        "description": "Design user-friendly apps, websites, and digital experiences that people love",
        "skills": ["creativity", "empathy", "problem-solving", "visual design"],
        "subjects": ["design", "psychology", "computer science"],
        "salary_range": "$70,000 - $140,000+",
        "avg_salary": "$95,000",
        "growth": "Very High (23% projected growth)",
        "education": "Bachelor's in UX Design, Graphic Design, or Computer Science",
        "impact": "Make technology accessible and enjoyable for everyone, from apps to websites",
        "day_in_life": "Research user needs, create wireframes and prototypes, test designs, collaborate with developers",
        "beginner_projects": ["Redesign your favorite app", "Create website mockups", "Conduct user interviews"],
        "next_steps": ["Learn design tools like Figma", "Study user psychology", "Build a design portfolio"]
    },
    "chemical_engineer": {
        "title": "Chemical Engineer",
        "description": "Use chemistry to solve problems and create new products, from medicines to clean energy",
        "skills": ["chemistry", "problem-solving", "mathematics", "attention to detail"],
        "subjects": ["chemistry", "mathematics", "physics", "biology"],
        "salary_range": "$75,000 - $135,000",
        "avg_salary": "$105,000",
        "growth": "Moderate (9% projected growth)",
        "education": "Bachelor's in Chemical Engineering",
        "impact": "Develop life-saving medicines, sustainable materials, and clean energy solutions",
        "day_in_life": "Design chemical processes, test new materials, optimize production, ensure safety standards",
        "beginner_projects": ["Conduct chemistry experiments", "Research sustainable materials", "Create eco-friendly products"],
        "next_steps": ["Excel in chemistry and math", "Join science clubs", "Learn about chemical processes"]
    },
    "robotics_engineer": {
        "title": "Robotics Engineer",
        "description": "Design and build robots that can help people, explore dangerous places, or automate tasks",
        "skills": ["engineering", "programming", "creativity", "problem-solving"],
        "subjects": ["computer science", "mathematics", "physics", "engineering"],
        "salary_range": "$75,000 - $150,000+",
        "avg_salary": "$100,000",
        "growth": "Very High (28% projected growth)",
        "education": "Bachelor's in Robotics, Mechanical, or Electrical Engineering",
        "impact": "Create robots for healthcare, disaster response, space exploration, and everyday assistance",
        "day_in_life": "Design robot mechanics, program AI behaviors, test prototypes, integrate sensors and systems",
        "beginner_projects": ["Build a line-following robot", "Program a robot arm", "Join FIRST Robotics"],
        "next_steps": ["Learn Arduino or Raspberry Pi", "Join robotics clubs", "Study programming and mechanics"]
    },
    "network_engineer": {
        "title": "Network/Cloud Engineer",
        "description": "Build and maintain the internet infrastructure and cloud systems that connect the world",
        "skills": ["technical skills", "problem-solving", "attention to detail", "communication"],
        "subjects": ["computer science", "networking", "mathematics"],
        "salary_range": "$70,000 - $145,000+",
        "avg_salary": "$105,000",
        "growth": "High (15% projected growth)",
        "education": "Bachelor's in Computer Science, IT, or related field",
        "impact": "Keep the internet running and help businesses scale their digital infrastructure",
        "day_in_life": "Design network systems, troubleshoot connectivity issues, implement security, manage cloud infrastructure",
        "beginner_projects": ["Set up a home network", "Learn about cloud platforms", "Build a simple server"],
        "next_steps": ["Learn networking basics", "Study cloud platforms like AWS", "Get certifications like CompTIA Network+"]
    },
    "bioinformatics_specialist": {
        "title": "Bioinformatics Specialist",
        "description": "Combine biology, computer science, and data analysis to solve medical mysteries",
        "skills": ["biology", "programming", "data analysis", "research"],
        "subjects": ["biology", "computer science", "mathematics", "chemistry"],
        "salary_range": "$70,000 - $130,000",
        "avg_salary": "$95,000",
        "growth": "Very High (20% projected growth)",
        "education": "Bachelor's in Bioinformatics, Biology, or Computer Science",
        "impact": "Advance personalized medicine, fight diseases, and decode the mysteries of DNA",
        "day_in_life": "Analyze genetic data, develop algorithms for DNA sequencing, collaborate with biologists and doctors",
        "beginner_projects": ["Explore DNA databases", "Learn Python for biology", "Analyze genetic data"],
        "next_steps": ["Study biology and programming", "Learn about genetics", "Explore bioinformatics tools"]
    },
    "game_developer": {
        "title": "Game Developer",
        "description": "Create video games that entertain, educate, and inspire millions of players",
        "skills": ["programming", "creativity", "storytelling", "problem-solving"],
        "subjects": ["computer science", "mathematics", "design"],
        "salary_range": "$60,000 - $140,000+",
        "avg_salary": "$90,000",
        "growth": "High (16% projected growth)",
        "education": "Bachelor's in Computer Science, Game Design, or related field",
        "impact": "Create immersive experiences, educational games, and entertainment for people worldwide",
        "day_in_life": "Write game code, design game mechanics, create graphics and animations, test gameplay",
        "beginner_projects": ["Make a simple game in Unity", "Create a text-based adventure", "Design game levels"],
        "next_steps": ["Learn game engines like Unity or Unreal", "Study programming and game design", "Join game jams"]
    },
    "electrical_engineer": {
        "title": "Electrical Engineer",
        "description": "Design electrical systems, circuits, and devices that power our modern world",
        "skills": ["mathematics", "problem-solving", "technical skills", "innovation"],
        "subjects": ["physics", "mathematics", "engineering"],
        "salary_range": "$70,000 - $135,000",
        "avg_salary": "$100,000",
        "growth": "Moderate (7% projected growth)",
        "education": "Bachelor's in Electrical Engineering",
        "impact": "Develop renewable energy systems, smart devices, and electrical innovations",
        "day_in_life": "Design circuits, test electrical systems, develop power solutions, work on electronics",
        "beginner_projects": ["Build simple circuits", "Create LED projects", "Experiment with Arduino"],
        "next_steps": ["Learn about circuits and electricity", "Join engineering clubs", "Experiment with electronics kits"]
    },
    "marine_biologist": {
        "title": "Marine Biologist",
        "description": "Study ocean life and ecosystems to protect our seas and discover new species",
        "skills": ["biology", "research", "passion for nature", "diving/swimming"],
        "subjects": ["biology", "chemistry", "environmental science"],
        "salary_range": "$45,000 - $90,000",
        "avg_salary": "$65,000",
        "growth": "Moderate (5% projected growth)",
        "education": "Bachelor's in Marine Biology or Biology",
        "impact": "Protect ocean ecosystems, discover new species, and fight climate change",
        "day_in_life": "Conduct underwater research, study marine species, analyze ocean data, advocate for conservation",
        "beginner_projects": ["Visit aquariums and ask questions", "Research ocean conservation", "Join beach cleanup efforts"],
        "next_steps": ["Study biology and ecology", "Learn to scuba dive", "Join marine conservation groups"]
    },
    "ai_ml_engineer": {
        "title": "AI/Machine Learning Engineer",
        "description": "Build intelligent systems that can learn, adapt, and solve complex problems",
        "skills": ["programming", "mathematics", "problem-solving", "creativity"],
        "subjects": ["computer science", "mathematics", "statistics"],
        "salary_range": "$100,000 - $200,000+",
        "avg_salary": "$145,000",
        "growth": "Very High (40% projected growth)",
        "education": "Bachelor's in Computer Science, AI, or related field",
        "impact": "Create AI that can diagnose diseases, fight climate change, and improve daily life",
        "day_in_life": "Train machine learning models, develop AI algorithms, analyze data, deploy intelligent systems",
        "beginner_projects": ["Build a chatbot", "Train a simple neural network", "Create an image classifier"],
        "next_steps": ["Learn Python and TensorFlow", "Study machine learning basics", "Practice on Kaggle competitions"]
    }
}

# =============================================================================
# ROLE MODELS DATABASE
# =============================================================================
# Features 12+ inspiring STEM professionals from diverse backgrounds
# Each role model includes their story, challenges overcome, and advice for students
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
    },
    {
        "name": "Dr. Chien-Shiung Wu",
        "career": "aerospace_engineer",
        "title": "Experimental Physicist",
        "background": "Chinese-American physicist who made major contributions to nuclear physics. Known as the 'First Lady of Physics' and 'Queen of Nuclear Research.'",
        "quote": "It is the courage to continue that counts.",
        "ethnicity": "Asian American",
        "gender": "Female",
        "challenges": "Faced gender and racial discrimination in 1940s-1960s science, was overlooked for Nobel Prize despite groundbreaking work",
        "advice": "Excellence speaks for itself. Keep pushing forward even when recognition doesn't come immediately.",
        "what_students_learn": "Experimental physics, persistence in research, and the importance of rigorous scientific method"
    },
    {
        "name": "Jerry Yang",
        "career": "software_engineer",
        "title": "Co-founder of Yahoo!",
        "background": "Taiwanese-American entrepreneur who co-founded Yahoo!, one of the pioneers of the early internet era.",
        "quote": "The Internet is about giving people choice and control.",
        "ethnicity": "Asian American",
        "gender": "Male",
        "challenges": "Immigrated to the US at age 10 speaking no English, built one of the world's largest tech companies",
        "advice": "Innovation comes from seeing problems from a different angle. Your immigrant perspective is valuable.",
        "what_students_learn": "Entrepreneurship, software engineering, and building products that millions use"
    },
    {
        "name": "Dr. Shirley Ann Jackson",
        "career": "computer_science_engineer",
        "title": "Physicist & Former NRC Chair",
        "background": "First African American woman to earn a PhD from MIT. Her research enabled caller ID, call waiting, and fiber optic cables.",
        "quote": "The way to bring about change is to be proactive and not reactive.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "One of very few Black students at MIT in the 1960s, faced isolation and discrimination",
        "advice": "Excellence and preparation are your best tools. Your work will speak louder than prejudice.",
        "what_students_learn": "Theoretical physics, telecommunications technology, and leadership in STEM policy"
    },
    {
        "name": "Min Kao",
        "career": "electrical_engineer",
        "title": "Co-founder of Garmin",
        "background": "Taiwanese-American electrical engineer who co-founded Garmin, revolutionizing GPS navigation technology.",
        "quote": "Innovation requires taking risks and learning from failure.",
        "ethnicity": "Asian American",
        "gender": "Male",
        "challenges": "Immigrated with limited resources, built a multi-billion dollar company from scratch",
        "advice": "Combine technical skills with business acumen. Solve real problems people face every day.",
        "what_students_learn": "Electrical engineering, GPS technology, and tech entrepreneurship"
    },
    {
        "name": "Dr. Kizzmekia Corbett",
        "career": "biomedical_engineer",
        "title": "Viral Immunologist",
        "background": "African American scientist who was one of the lead scientists developing the Moderna COVID-19 vaccine.",
        "quote": "You can do anything you want to do. It's just about finding your purpose.",
        "ethnicity": "African American",
        "gender": "Female",
        "challenges": "Grew up in a low-income area, became one of the world's leading vaccine researchers",
        "advice": "Don't let where you come from limit where you're going. Science needs diverse voices.",
        "what_students_learn": "Immunology, vaccine development, and how STEM directly saves lives"
    },
    {
        "name": "Lisa Su",
        "career": "electrical_engineer",
        "title": "CEO of AMD",
        "background": "Taiwanese-American engineer who became CEO of AMD and transformed the semiconductor industry.",
        "quote": "It's about the challenge. It's about pushing the boundaries.",
        "ethnicity": "Asian American",
        "gender": "Female",
        "challenges": "Rose through male-dominated semiconductor industry, turned around a struggling company",
        "advice": "Technical excellence combined with strategic vision creates opportunities. Never stop learning.",
        "what_students_learn": "Electrical engineering, semiconductor design, and tech leadership"
    },
    {
        "name": "Emma González",
        "career": "environmental_scientist",
        "title": "Environmental Activist & Student Leader",
        "background": "Cuban-American activist who became a leading voice for environmental and social justice after surviving the Parkland shooting.",
        "quote": "Fight for your lives before it's someone else's job.",
        "ethnicity": "Hispanic",
        "gender": "Female",
        "challenges": "Turned personal tragedy into activism, faced intense public scrutiny as a young leader",
        "advice": "Your voice matters at any age. Use science and data to drive change.",
        "what_students_learn": "Environmental science, activism, and using STEM to solve social problems"
    },
    {
        "name": "Dr. Mario Molina",
        "career": "environmental_scientist",
        "title": "Nobel Prize-Winning Chemist",
        "background": "Mexican-American chemist who discovered the ozone hole and won the Nobel Prize in Chemistry.",
        "quote": "It is our responsibility to do what we can, to take action.",
        "ethnicity": "Hispanic",
        "gender": "Male",
        "challenges": "Had to convince the world that CFCs were destroying the ozone layer despite industry opposition",
        "advice": "Follow the science, even when it's unpopular. Environmental protection is everyone's responsibility.",
        "what_students_learn": "Chemistry, atmospheric science, and the power of scientific research to change policy"
    },
    {
        "name": "Francia Raisa",
        "career": "biomedical_engineer",
        "title": "Actress & Organ Donation Advocate",
        "background": "Honduran-Mexican-American actress who donated her kidney and became an advocate for organ donation awareness.",
        "quote": "I would do it again in a heartbeat.",
        "ethnicity": "Hispanic",
        "gender": "Female",
        "challenges": "Used her platform to raise awareness about the shortage of organ donors in Latino communities",
        "advice": "Science and medicine save lives. Consider how you can contribute to healthcare innovation.",
        "what_students_learn": "Biomedical engineering, organ transplant technology, and healthcare advocacy"
    },
    {
        "name": "Sally Ride",
        "career": "aerospace_engineer",
        "title": "First American Woman in Space",
        "background": "Physicist and astronaut who became the first American woman to fly in space aboard the Space Shuttle Challenger.",
        "quote": "You can't be what you can't see.",
        "ethnicity": "Caucasian",
        "gender": "Female",
        "challenges": "Faced intense media scrutiny and sexism as the first American woman in space",
        "advice": "Don't let anyone tell you that you can't do something because of your gender.",
        "what_students_learn": "Physics, space exploration, and breaking barriers"
    },
    {
        "name": "Bill Nye",
        "career": "mechanical_engineer",
        "title": "Science Educator & Engineer",
        "background": "Mechanical engineer who became 'Bill Nye the Science Guy,' inspiring millions to love science.",
        "quote": "Science is the key to our future.",
        "ethnicity": "Caucasian",
        "gender": "Male",
        "challenges": "Made science accessible and fun for everyone, fought climate change denial",
        "advice": "Never lose your curiosity. Science communication is just as important as science research.",
        "what_students_learn": "Mechanical engineering, science communication, and making STEM accessible"
    },
    {
        "name": "Jane Goodall",
        "career": "environmental_scientist",
        "title": "Primatologist & Conservationist",
        "background": "World's foremost expert on chimpanzees and a tireless advocate for environmental conservation.",
        "quote": "What you do makes a difference, and you have to decide what kind of difference you want to make.",
        "ethnicity": "Caucasian",
        "gender": "Female",
        "challenges": "Faced skepticism as a woman without formal training, revolutionized animal behavior research",
        "advice": "Passion and dedication can take you anywhere. You don't need to fit the traditional mold.",
        "what_students_learn": "Biology, animal behavior, conservation, and fieldwork"
    },
    {
        "name": "Alan Turing",
        "career": "computer_science_engineer",
        "title": "Father of Computer Science",
        "background": "British mathematician who cracked the Enigma code in WWII and laid the foundations for modern computing and AI.",
        "quote": "We can only see a short distance ahead, but we can see plenty there that needs to be done.",
        "ethnicity": "Caucasian",
        "gender": "Male",
        "challenges": "Persecuted for being gay despite saving millions of lives, posthumously pardoned",
        "advice": "Your personal identity doesn't diminish your contributions. Be true to yourself and your work.",
        "what_students_learn": "Computer science, cryptography, artificial intelligence, and computational theory"
    }
]

# =============================================================================
# PAGE ROUTES
# =============================================================================
# These routes handle displaying different pages of the website

@app.route("/")
def home():
    """Home page with hero, about section, features, and chatbot"""
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    """Interactive quiz to match students with STEM careers"""
    return render_template("quiz.html")

@app.route("/results")
def results():
    """Display quiz results with matched careers and role models"""
    return render_template("results.html")

@app.route("/careers")
def careers():
    """Browse all 17+ STEM career paths with detailed information"""
    return render_template("careers.html", careers=STEM_CAREERS)

@app.route("/role-models")
def role_models():
    """Meet inspiring STEM professionals from diverse backgrounds"""
    return render_template("role_models.html", role_models=ROLE_MODELS)

@app.route("/about")
def about():
    """Learn about the SeeMe in STEM project"""
    return render_template("about.html")

@app.route("/features")
def features():
    """Explore key features of the platform"""
    return render_template("features.html")

@app.route("/confidence")
def confidence():
    """Address common concerns and build confidence in STEM"""
    return render_template("confidence.html")

@app.route("/myths")
def myths():
    """Bust common STEM myths"""
    return render_template("myths.html")

@app.route("/opportunities")
def opportunities():
    """Find summer camps, scholarships, competitions, and resources"""
    return render_template("opportunities.html")

@app.route("/chat")
def chat_page():
    """Chatbot page for asking STEM questions"""
    return render_template("chat.html")

# =============================================================================
# API ENDPOINTS
# =============================================================================
# These routes handle data processing and AI interactions

@app.route("/api/match-careers", methods=["POST"])
def match_careers():
    """
    AI-powered career matching endpoint
    Takes student quiz responses and returns top 3 matching STEM careers
    Uses Claude AI for intelligent matching or falls back to rule-based matching
    """
    try:
        # Get quiz data from request
        data = request.get_json()

        # Check if AWS credentials are available for AI matching
        aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        use_ai = aws_access_key and aws_access_key != "your_aws_access_key_id_here"

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

            # Prepare request for AWS Bedrock
            request_body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })

            # Call AWS Bedrock
            response = bedrock_runtime.invoke_model(
                modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                body=request_body
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            reply = response_body['content'][0]['text']

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
    """
    Simple rule-based career matching when AI is not available
    Scores each career based on matching interests, subjects, and skills
    Returns top 3 careers with explanations
    """
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

@app.route("/api/mentor", methods=["POST"])
def mentor():
    """
    Career mentor chatbot endpoint powered by Claude via AWS Bedrock
    Provides detailed answers about specific STEM careers
    Includes information about classes, difficulty, skills, salary, and advice
    """
    try:
        # Get user's message and career context
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "Please send a message!"}), 400

        user_message = data["message"]
        career = data.get("career", "STEM professional")

        # Career-specific information
        career_info = STEM_CAREERS.get(
            next((k for k, v in STEM_CAREERS.items() if v["title"] == career), "software_engineer"),
            STEM_CAREERS["software_engineer"]
        )

        # Check if AWS credentials are available
        aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        use_ai = aws_access_key and aws_access_key != "your_aws_access_key_id_here"

        if use_ai:
            # Use Claude AI for intelligent, personalized responses
            prompt = f"""You are a friendly, encouraging STEM career mentor helping a student learn about becoming a {career}.

Career Information:
- Title: {career}
- Education Required: {career_info['education']}
- Key Skills: {', '.join(career_info['skills'])}
- Subjects to Study: {', '.join(career_info['subjects'])}
- Salary Range: {career_info['salary_range']}
- Job Growth: {career_info['growth']}
- Impact: {career_info['impact']}
- Beginner Projects: {', '.join(career_info.get('beginner_projects', []))}
- Next Steps: {', '.join(career_info.get('next_steps', []))}

Student's Question: {user_message}

Provide a helpful, encouraging response that:
- Directly answers their question with specific details from the career information above
- Is conversational and supportive (use "you" and "your")
- Keeps response to 2-4 short paragraphs
- Uses emojis sparingly (1-2 max) for personality
- Emphasizes that they CAN succeed in this career
- Provides actionable advice when relevant

Be authentic, enthusiastic, and specific. Focus on being helpful rather than just motivational."""

            # Prepare request for AWS Bedrock
            request_body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })

            # Call AWS Bedrock
            response = bedrock_runtime.invoke_model(
                modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                body=request_body
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text']

        else:
            # Fallback response if no AI available
            response_text = f"""I'm your {career} mentor! I can help you with:

• How many classes you need
• Whether {career} is hard
• What skills to develop
• How to get started
• Salary expectations
• College requirements
• Opportunities for women in STEM

Ask me anything about becoming a {career}! 🚀"""

        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Mentor ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"response": "Oops! Something went wrong. Please try again!"}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    General STEM chatbot endpoint powered by Claude via AWS Bedrock
    Responds to questions about STEM careers, resources, and getting started
    """
    try:
        # Get user's chat message
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"response": "Please send a message!"}), 400

        user_message = data["message"]

        # Check if AWS credentials are available
        aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        use_ai = aws_access_key and aws_access_key != "your_aws_access_key_id_here"

        if use_ai:
            # Use Claude AI for intelligent responses
            prompt = f"""You are a friendly and enthusiastic STEM Career Guide chatbot helping students explore STEM careers and opportunities. Your goal is to inspire, encourage, and provide helpful information about STEM education and careers.

Context about this platform:
- We help students discover STEM careers through career matching quizzes
- We feature 17+ STEM careers including Software Engineer, Biomedical Engineer, Cybersecurity Analyst, Aerospace Engineer, Data Scientist, Environmental Scientist, and more
- We showcase diverse role models like Dr. Mae Jemison, Grace Hopper, Katherine Johnson, Ellen Ochoa, and others
- We provide information about summer camps, scholarships, competitions, and free learning resources

Available resources we offer:
- Career Quiz: Matches students with ideal STEM careers
- Role Models Section: Inspiring STEM professionals from diverse backgrounds
- Opportunities Section: Summer camps (Girls Who Code, NASA programs, AI4ALL), scholarships (SWE, NSBE, HSF), competitions (FIRST Robotics, Google Science Fair)
- Free Learning: Khan Academy, Coursera, Code.org, MIT OpenCourseWare

User's message: {user_message}

Respond in a friendly, encouraging tone. Keep responses concise (2-4 short paragraphs). Use emojis sparingly to add personality. Focus on:
- Answering their specific question
- Being encouraging and positive
- Suggesting relevant resources from our platform when appropriate
- Inspiring confidence that they CAN succeed in STEM

If they ask about specific careers, classes, getting started, scholarships, camps, or role models, provide helpful specific information. Always be supportive and never dismissive."""

            # Prepare request for AWS Bedrock
            request_body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })

            # Call AWS Bedrock
            response = bedrock_runtime.invoke_model(
                modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
                body=request_body
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text']

        else:
            # Fallback response if no AI available
            response_text = "Hi! 👋 I'm your STEM Career Guide! I can help you explore STEM careers, find resources, and answer your questions. Try asking about:\n• What STEM career fits me?\n• What classes should I take?\n• Are there scholarships available?\n• What summer camps can I join?\n• Can I do STEM if I'm bad at math?\n\nWhat would you like to know?"

        # Return response with streaming flag for frontend
        return jsonify({"response": response_text, "stream": True})

    except Exception as e:
        print(f"Chat ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"response": "Oops! Something went wrong. Please try again!"}), 500

# =============================================================================
# RUN THE APPLICATION
# =============================================================================
if __name__ == "__main__":
    # Run Flask development server
    # Debug mode enabled for development (shows errors and auto-reloads)
    app.run(debug=True)
