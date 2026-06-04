# Setup Instructions

## How to Run the STEM Career Explorer

### 1. Install Dependencies (if not already done)
```bash
python -m pip install -r requirements.txt
```

### 2. Configure API Key (Optional - for AI-powered matching)

The app works in two modes:

**Mode 1: Rule-Based Matching (No API Key Required)**
- The app will automatically use a rule-based algorithm to match careers
- This works out of the box without any configuration
- Simply run the app and it will work!

**Mode 2: AI-Powered Matching (Requires API Key)**
- For more intelligent career matching using Claude AI
- Edit the `.env` file and replace `your_api_key_here` with your actual Anthropic API key
- Get an API key from: https://console.anthropic.com/

### 3. Run the App
```bash
python app.py
```

### 4. Open in Browser
Visit: http://127.0.0.1:5000

## Features That Now Work

✅ **Home Page** - All emojis replaced with bordered images
✅ **Career Quiz** - All quiz icons are now images with borders
✅ **Results Page** - Displays matched careers with images
✅ **Role Models Page** - All icons replaced with images
✅ **Career Matching** - Works with or without API key!

## Troubleshooting

**Problem:** Quiz doesn't return results

**Solution:** The app now has two fallback mechanisms:
1. If no API key is set, it uses rule-based matching
2. If API call fails, it falls back to rule-based matching

**Problem:** Images not loading

**Solution:** Make sure you have an internet connection (images are loaded from CDN)

## How the Career Matching Works

### Without API Key (Rule-Based):
- Scores each career based on interest, subject, and skill matches
- Uses weighted scoring: subjects (15 points), interests (10 points), skills (10 points)
- Special bonuses for specific combinations (e.g., coding + CS = software engineer)
- Returns top 3 matches with scores and explanations

### With API Key (AI-Powered):
- Uses Claude AI to analyze student profile
- Provides personalized explanations
- More nuanced matching based on goals and preferences
- Still has rule-based fallback if API fails

## Next Steps

1. Test the quiz with different combinations
2. Check that all images load properly
3. Try both with and without API key to see the difference
4. Customize the rule-based matching logic if needed (see `rule_based_matching()` function in app.py)
