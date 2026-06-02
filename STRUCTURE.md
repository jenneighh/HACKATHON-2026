# STEM Career Explorer - Project Structure

## File Organization

```
Hackathon-2026/
│
├── 📄 app.py                    # Main Flask application (backend logic)
│   ├── Routes (pages)
│   ├── STEM_CAREERS database
│   ├── ROLE_MODELS database
│   └── AI matching logic
│
├── 📁 templates/                # HTML pages (frontend)
│   ├── index.html              # Homepage with hero section
│   ├── quiz.html               # Interactive career quiz
│   ├── results.html            # AI-matched career results
│   ├── careers.html            # All careers directory
│   └── role_models.html        # Role models showcase
│
├── 🔐 .env                      # Environment variables (AWS keys)
├── 📋 requirements.txt          # Python dependencies
├── 📖 README.md                 # Full documentation
├── 🚀 QUICKSTART.md             # Quick start guide
└── 📊 STRUCTURE.md              # This file
```

## User Flow

```
┌─────────────┐
│   Homepage  │  Student lands here
│  index.html │
└──────┬──────┘
       │ Click "Start Your Journey"
       ↓
┌─────────────┐
│    Quiz     │  Interactive questionnaire
│  quiz.html  │  Selects interests, skills, subjects
└──────┬──────┘
       │ Submit form → API call to /api/match-careers
       │ Claude AI analyzes responses
       ↓
┌─────────────┐
│   Results   │  Personalized career matches
│results.html │  Top 3 careers with role models
└──────┬──────┘
       │
       ├──→ Browse all careers (careers.html)
       └──→ Meet role models (role_models.html)
```

## Data Flow

```
Frontend (HTML/JS)
      ↓
   POST /api/match-careers
      ↓
Flask Backend (app.py)
      ↓
Claude AI via AWS Bedrock
      ↓
JSON Response with matches
      ↓
Enhanced with career data + role models
      ↓
Frontend displays results
```

## Key Components

### Backend (app.py)

**Databases:**
- `STEM_CAREERS` - 8+ career profiles with details
- `ROLE_MODELS` - 8+ diverse STEM professionals

**Routes:**
- `GET /` - Serve homepage
- `GET /quiz` - Serve quiz page
- `GET /results` - Serve results page
- `GET /careers` - Serve careers directory
- `GET /role-models` - Serve role models page
- `POST /api/match-careers` - AI career matching
- `POST /api/chat` - AI chat (future feature)

**AI Logic:**
- Takes student profile from quiz
- Sends to Claude with career database
- Parses AI response
- Enhances with full career info
- Adds relevant role models
- Returns to frontend

### Frontend (templates/*.html)

Each page includes:
- Responsive navigation bar
- Custom CSS styling
- JavaScript for interactivity
- Gradient purple theme
- Mobile-friendly design

**index.html:**
- Hero section with CTA
- Features overview
- Statistics
- Animations

**quiz.html:**
- 5 question sections
- Multi-select cards
- Progress bar
- Form validation
- Loading state

**results.html:**
- Career match cards
- Match percentages
- "Why it fits" explanations
- Next steps guidance
- Role model cards
- Action buttons

**careers.html:**
- Grid of all careers
- Detailed info cards
- Skills tags
- CTA to take quiz

**role_models.html:**
- Grid of role models
- Quotes and backgrounds
- Ethnicity/gender tags
- Inspiring design

## Technology Stack

```
┌──────────────────────────────────┐
│         Frontend                 │
│  HTML5 + CSS3 + JavaScript       │
│  (No frameworks - pure vanilla)  │
└──────────────────────────────────┘
              ↕
┌──────────────────────────────────┐
│         Backend                  │
│       Flask (Python)             │
│  - Routing                       │
│  - Session management            │
│  - API endpoints                 │
└──────────────────────────────────┘
              ↕
┌──────────────────────────────────┐
│         AI Layer                 │
│  Claude 4.5 via AWS Bedrock      │
│  - Career matching               │
│  - Personalized recommendations  │
└──────────────────────────────────┘
```

## Customization Points

1. **Colors/Theme**: Edit CSS in each HTML file
2. **Careers**: Add to `STEM_CAREERS` dict in app.py
3. **Role Models**: Add to `ROLE_MODELS` list in app.py
4. **Quiz Questions**: Edit quiz.html question sections
5. **AI Prompts**: Modify prompts in app.py API routes
6. **Navigation**: Update navbar in all HTML files

## Database Structure

### STEM_CAREERS
```python
{
    "career_id": {
        "title": "Career Name",
        "description": "What they do",
        "skills": ["skill1", "skill2"],
        "subjects": ["subject1"],
        "salary_range": "$XX-$YY",
        "growth": "X% growth",
        "education": "Required degree"
    }
}
```

### ROLE_MODELS
```python
[
    {
        "name": "Full Name",
        "career": "career_id",
        "title": "Professional title",
        "background": "Their story",
        "quote": "Inspiring words",
        "ethnicity": "Background",
        "gender": "Gender"
    }
]
```

## Future Expansion Ideas

- 💾 Add database (SQLite/PostgreSQL)
- 👤 User accounts and profiles
- 📸 Role model photos/videos
- 📊 Analytics dashboard
- 🔗 Share results feature
- 💬 Live chat with AI counselor
- 🎓 Scholarship recommendations
- 🏢 Internship listings
- 📱 Mobile app version

---

Need help? Check README.md or QUICKSTART.md!
