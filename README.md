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
- AI-powered chatbot with word-by-word streaming responses
- Processing animation while AI generates responses
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
- **AI:** AWS Bedrock (Claude Sonnet 4.5) with rule-based fallback
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
# Create a .env file with the following content:
FLASK_SECRET_KEY=your-secret-key-change-in-production

# AWS Credentials for Bedrock (required for AI features)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
```

**⚠️ Important AWS Setup:**
- You need AWS Bedrock access to use AI-powered features
- Request Claude Sonnet 4.5 model access in AWS Bedrock Console
- See [AWS_BEDROCK_SETUP.md](./AWS_BEDROCK_SETUP.md) for detailed setup instructions
- *Note: The app works without AWS credentials using rule-based matching!*

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
5. **Chat with Guide** - Ask questions and get resources (with AI streaming!)
6. **Take Action** - Access camps, competitions, scholarships, and more

## 🆕 Recent Updates

### Chatbot Streaming Animation (Latest)
- Added professional processing animation with animated dots
- Implemented word-by-word streaming for AI responses
- Enhanced user experience similar to ChatGPT/Claude
- See [CHATBOT_STREAMING_UPDATE.md](./CHATBOT_STREAMING_UPDATE.md) for details

### AWS Bedrock Integration
- Migrated from Anthropic API to AWS Bedrock
- Uses Claude Sonnet 4.5 for AI-powered features
- Rule-based fallback when credentials not configured
- See [AWS_BEDROCK_SETUP.md](./AWS_BEDROCK_SETUP.md) for setup guide

## 🌍 Impact

By helping students see themselves in STEM careers early, we can:
- Close the diversity gap in STEM fields
- Unlock untapped potential in underrepresented communities
- Ensure the next generation of innovators reflects the world we live in

## 🔧 Troubleshooting

### AWS Bedrock Issues
- **"Could not connect to endpoint"** - Check your `AWS_DEFAULT_REGION` setting
- **"Access denied"** - Verify AWS credentials and IAM permissions for Bedrock
- **"Model not found"** - Request Claude model access in AWS Bedrock Console

### Chatbot Not Working
- The app automatically falls back to rule-based matching without AWS credentials
- Check terminal/console for error messages
- Ensure `.env` file is in the project root directory

### Environment Variables
- Never commit `.env` file to version control (it's in `.gitignore`)
- Make sure to replace placeholder values with actual credentials
- Restart the Flask app after changing `.env` file

For detailed AWS setup, see [AWS_BEDROCK_SETUP.md](./AWS_BEDROCK_SETUP.md)

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
