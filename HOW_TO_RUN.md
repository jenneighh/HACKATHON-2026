# 🚀 How to Run Your STEM Career Explorer Website

## Step 1: Install Python Dependencies

Open your terminal (Command Prompt or PowerShell) and navigate to your project folder:

```bash
cd C:\Users\jenny\hackathon\Hackathon-2026
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

## Step 2: Run the Flask Server

Start the Flask application:

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

## Step 3: Open the Website in Your Browser

Open your web browser (Chrome, Firefox, Edge, etc.) and go to:

```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

## 🎉 That's it! Your website is now running!

---

## Quick Tips:

- **Keep the terminal window open** while using the website. If you close it, the website will stop working.
- To **stop the server**, press `Ctrl + C` in the terminal.
- To **restart** after making changes, stop the server and run `python app.py` again.
- For the **hackathon presentation**, you can show the website on your laptop by going to `http://localhost:5000`

---

## Troubleshooting:

**Problem**: "pip is not recognized"
- **Solution**: Make sure Python is installed. Try `python -m pip install -r requirements.txt` instead.

**Problem**: Port 5000 is already in use
- **Solution**: Change the port by editing the last line of `app.py` to: `app.run(debug=True, port=5001)` then go to `http://localhost:5001`

**Problem**: The chatbot isn't responding
- **Solution**: That's okay! The chatbot works with simple keyword matching (no AI API needed for the demo). Just type keywords like "hello", "math", "career", "help", etc.

---

## For Your Presentation:

1. Start the server before your presentation
2. Open the website in your browser
3. Show each feature:
   - Home page with chatbot
   - Take the quiz
   - See your "Future You" results
   - Browse all careers
   - Meet role models and use shadow/mentor buttons
   - Demonstrate the STEM news section

Good luck! 🌟
