# 🌟 SeeMe in STEM - Find Your Future

**AI-powered STEM career matching platform connecting students with personalized career paths and diverse role models**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)

## 🎯 The Problem

- **70%** of girls lose interest in STEM by middle school
- **Only 28%** of the STEM workforce are women
- **5%** of tech workers are Black or Latinx women

Too many talented students give up on STEM careers because they don't see people like themselves succeeding in these fields, don't know where to start, or face barriers that feel impossible to overcome.

## 💡 Our Solution

**SeeMe in STEM** uses AI to match students with personalized STEM career paths based on their unique interests and skills. But we go beyond just career suggestions — we connect students with diverse role models, bust common myths, and provide actionable resources to turn dreams into reality.

## ✨ Features

### 🎯 Smart Career Matching
- Interactive quiz analyzing interests, skills, and goals
- AI-powered personalized career recommendations
- Detailed career information including salary, growth prospects, and impact

### 👥 Diverse Role Models
- 12+ inspiring STEM professionals from all backgrounds
- Real stories of overcoming challenges
- Advice and mentorship from people who've walked the path

### 💬 STEM Career Chatbot
- Ask questions about STEM careers, classes, and getting started
- Get guidance on scholarships, summer camps, and competitions
- Bust common myths and build confidence

### 🚀 Actionable Resources
- Summer camps and programs
- Competitions and challenges
- Scholarships and financial aid
- Free learning resources

### 🎨 Beautiful, Responsive Design
- Sophisticated cream/purple/gold color palette
- Mobile-friendly interface
- Engaging animations and interactions

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI:** AWS Bedrock (Claude) with rule-based fallback
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Deployment:** Render/Vercel compatible

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jenneighh/HACKATHON-2026.git
cd HACKATHON-2026
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your AWS credentials
# Copy .env.example to .env and fill in your credentials
cp .env.example .env
```

Then edit `.env` and add:
```
FLASK_SECRET_KEY=your-secret-key-change-in-production
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
```

*Note: You'll receive AWS credentials via email. The app works with limited features without AWS credentials.*

4. Run the application:
```bash
python app.py
```

5. Open your browser to `http://localhost:5000`

## 🎓 Available STEM Careers

- **Software Engineer** - Design and develop innovative applications
- **Biomedical Engineer** - Create life-saving healthcare technologies
- **Cybersecurity Analyst** - Protect systems from cyber threats
- **Computer Science Engineer** - Build the future of computing
- **Aerospace Engineer** - Design aircraft and spacecraft

## 🌟 Featured Role Models

- **Dr. Mae Jemison** - First African American woman in space
- **Grace Hopper** - Computer programming pioneer
- **Katherine Johnson** - NASA mathematician (Hidden Figures)
- **Ellen Ochoa** - First Hispanic woman astronaut
- **Fei-Fei Li** - AI researcher and ethics pioneer
- And 7 more inspiring professionals!

## 📁 Project Structure

```
HACKATHON-2026/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Homepage with About section
│   ├── quiz.html         # Interactive career quiz
│   ├── results.html      # Personalized results page
│   ├── careers.html      # Career exploration
│   └── role_models.html  # Role model profiles
├── static/               # Static assets (CSS, JS, images)
├── requirements.txt      # Python dependencies
└── README.md            # You are here!
```

## 🎮 How to Use

1. **Homepage** - Learn about the problem and our mission
2. **Take the Quiz** - Answer questions about your interests and skills
3. **Get Matched** - Receive personalized STEM career recommendations
4. **Explore Role Models** - Meet inspiring professionals who look like you
5. **Chat with Guide** - Ask questions and get resources
6. **Take Action** - Access camps, competitions, scholarships, and more

## 🌍 Impact

By helping students see themselves in STEM careers early, we can:
- Close the diversity gap in STEM fields
- Unlock untapped potential in underrepresented communities
- Ensure the next generation of innovators reflects the world we live in

## 🤝 Contributing

This project was created for a hackathon, but contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Add more role models
- Improve the quiz algorithm
- Enhance the UI/UX

## 📜 License

MIT License - feel free to use this project for educational purposes!

## 👏 Acknowledgments

- Built with ❤️ for students who need to see themselves in STEM
- Inspired by real stories of STEM professionals who overcame barriers
- Special thanks to organizations like Girls Who Code, Black Girls CODE, and NSBE

## 📧 Contact

Have questions or feedback? Feel free to reach out!

---

**Made with 💜 by Jenny for Hackathon 2026**

*"If you can see it, you can be it."* - Dr. Aprille Ericsson
