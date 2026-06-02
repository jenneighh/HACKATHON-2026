# Quick Start Guide 🚀

## Run the App (3 steps)

1. **Install dependencies** (first time only):
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   python app.py
   ```

3. **Open in browser**:
   ```
   http://localhost:5000
   ```

That's it! 🎉

## What You'll See

1. **Homepage** - Beautiful landing page with features overview
2. **Career Quiz** - Interactive questionnaire with emojis and animations
3. **Results Page** - AI-generated career matches with role models
4. **Careers Directory** - Browse all 8+ STEM careers
5. **Role Models** - Meet diverse STEM professionals

## Making Changes

### Change Colors
Each HTML file has CSS at the top. Find these lines and change the hex codes:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add More Careers
Open `app.py` and find the `STEM_CAREERS` dictionary around line 22. Add your new career following the same format!

### Add More Role Models
Open `app.py` and find the `ROLE_MODELS` list around line 75. Add new role models in the same format!

### Modify Quiz Questions
Open `templates/quiz.html` and edit the question sections. Each option is a card you can add/remove/edit.

## Need Help?

- Check `README.md` for detailed documentation
- Look at the terminal for error messages
- Make sure your `.env` file has valid AWS credentials

## Tips for Demo

1. **Test the full flow**: Home → Quiz → Results → Browse Careers → Role Models
2. **Show diversity**: Point out the diverse role models feature
3. **Explain AI**: Mention how Claude analyzes responses for personalized matches
4. **Highlight design**: The modern UI is student-friendly
5. **Mention scalability**: Easy to add more careers and role models

## Common Issues

**"Module not found" error**: Run `pip install -r requirements.txt`

**"Port already in use"**: Another app is running on port 5000. Stop it or change the port in `app.py` (last line)

**AI not responding**: Check AWS credentials in `.env` file

Good luck with your hackathon! 🌟
