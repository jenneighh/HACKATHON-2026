# AWS Bedrock Setup Guide

## What Changed

The chatbot has been updated to use **AWS Bedrock** instead of the direct Anthropic API. This allows you to use your AWS credentials to access Claude.

## Setup Steps

### 1. Install Dependencies

First, install the updated Python packages (now includes boto3 for AWS):

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Open the `.env` file and add your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_actual_access_key_id
AWS_SECRET_ACCESS_KEY=your_actual_secret_access_key
AWS_DEFAULT_REGION=us-east-1
```

**Important:** Replace the placeholder values with your actual AWS credentials!

### 3. Enable Claude in AWS Bedrock

Before running the app, make sure you have:

1. **Enabled model access** in AWS Bedrock console
2. Go to AWS Console → Bedrock → Model access
3. Request access to **Claude Sonnet 4.5** model
4. Wait for approval (usually instant for most accounts)

### 4. Set the Correct Region

Make sure `AWS_DEFAULT_REGION` in your `.env` file matches where you have Bedrock enabled. Common regions:
- `us-east-1` (US East - N. Virginia)
- `us-west-2` (US West - Oregon)

### 5. Run the Application

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

## Testing the Chatbot

The AI-powered career matching will now use AWS Bedrock when:
1. You take the quiz at `/quiz`
2. The quiz results will use Claude via AWS Bedrock to match careers

If AWS credentials are not configured, the app will automatically fall back to rule-based matching (no AI).

## Troubleshooting

### Error: "Could not connect to the endpoint URL"
- Check your `AWS_DEFAULT_REGION` is correct
- Verify the region has Bedrock enabled

### Error: "Access denied"
- Verify your AWS Access Key ID and Secret Access Key are correct
- Check that your AWS IAM user has Bedrock permissions

### Error: "Model not found"
- Make sure you've requested access to Claude models in AWS Bedrock console
- Wait a few minutes for access to be granted

### Chatbot not responding with AI
- The app has a fallback to rule-based matching if AWS credentials are missing
- Check the terminal/console for error messages
- Verify your `.env` file is in the correct location

## Cost Note

AWS Bedrock charges per API call. Make sure you understand the pricing:
- https://aws.amazon.com/bedrock/pricing/

The app only makes API calls when users take the quiz, so costs should be minimal for testing.
