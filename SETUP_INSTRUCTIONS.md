# Setup Instructions

## How to Run the STEM Career Explorer

### 1. Install Dependencies (if not already done)
```bash
python -m pip install -r requirements.txt
```

### 2. Configure AWS Bedrock (Optional - for AI-powered matching)

The app works in two modes:

**Mode 1: Rule-Based Matching (No AWS Required)**
- The app will automatically use a rule-based algorithm to match careers
- This works out of the box without any configuration
- Simply run the app and it will work!

**Mode 2: AI-Powered Matching (Requires AWS Bedrock)**
- For more intelligent career matching using Claude AI via AWS Bedrock
- Edit the `.env` file with your actual AWS credentials:
  ```env
  AWS_ACCESS_KEY_ID=your_aws_access_key_id
  AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
  AWS_DEFAULT_REGION=us-east-1
  ```
- See [AWS_BEDROCK_SETUP.md](./AWS_BEDROCK_SETUP.md) for detailed setup instructions
- You'll need to enable Claude Sonnet 4.5 access in AWS Bedrock Console

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
1. If no AWS credentials are set, it uses rule-based matching
2. If AWS Bedrock API call fails, it falls back to rule-based matching

**Problem:** Images not loading

**Solution:** Make sure you have an internet connection (images are loaded from CDN)

**Problem:** Chatbot shows processing animation but no response

**Solution:** Check your AWS credentials in `.env` file. The app will fall back to basic responses if AWS Bedrock is not configured.

## How the Career Matching Works

### Without AWS Credentials (Rule-Based):
- Scores each career based on interest, subject, and skill matches
- Uses weighted scoring: subjects (15 points), interests (10 points), skills (10 points)
- Special bonuses for specific combinations (e.g., coding + CS = software engineer)
- Returns top 3 matches with scores and explanations

### With AWS Bedrock (AI-Powered):
- Uses Claude AI via AWS Bedrock to analyze student profile
- Provides personalized explanations with word-by-word streaming animation
- More nuanced matching based on goals and preferences
- Still has rule-based fallback if API fails

## Next Steps

1. Test the quiz with different combinations
2. Check that all images load properly
3. Try both with and without AWS credentials to see the difference
4. Test the chatbot streaming animation feature
5. Customize the rule-based matching logic if needed (see `rule_based_matching()` function in app.py)

## New Features

✨ **Chatbot Streaming Animation:**
- The chatbot now shows a "AI is thinking" animation with bouncing dots
- Responses stream in word-by-word like ChatGPT
- See [CHATBOT_STREAMING_UPDATE.md](./CHATBOT_STREAMING_UPDATE.md) for details
