# Setup Guide - Cold Email Automation AI

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GMAIL_APP_PASSWORD=your_gmail_app_password_here
```

### 3. Get API Keys

#### YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key to `.env` file

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to "API Keys" section
4. Create a new API key
5. Copy the key to `.env` file

#### Gmail App Password (for SMTP)
1. Go to [Google Account](https://myaccount.google.com/)
2. Enable 2-Step Verification
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate a new app password for "Mail"
5. Copy the 16-character password to `.env` file as `GMAIL_APP_PASSWORD`

### 4. Gmail API Setup (Optional - Recommended)

For Gmail API (more reliable than SMTP):

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Gmail API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Application type: "Desktop app"
6. Download the credentials JSON file
7. Save it as `credentials.json` in the root directory
8. On first run, the app will open a browser for authentication
9. After authentication, `token.json` will be created automatically

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Email Configuration

The system is configured to send emails from **maxxichorea@gmail.com**. Make sure:

- The email account exists and is accessible
- Either Gmail API credentials are set up OR Gmail App Password is configured
- For Gmail API: `credentials.json` is in the root directory
- For SMTP: `GMAIL_APP_PASSWORD` is set in `.env` file

## Usage

### Full Automation Mode

1. Open `http://localhost:5000` in your browser
2. Enter a search query (e.g., "tech reviews", "gaming", "vlogs")
3. Select platforms (YouTube, Instagram, TikTok)
4. Click "Run Full Automation"
5. The system will:
   - Collect channels from selected platforms
   - Analyze their last posts using AI
   - Filter channels that can hire editors
   - Extract email addresses
   - Send personalized cold emails

### Step-by-Step Mode

You can also run each step individually:
1. Collect Channels
2. Analyze Channels
3. Collect Leads
4. Send Emails

## Troubleshooting

### Gmail API Not Working
- Make sure `credentials.json` is in the root directory
- Delete `token.json` and re-authenticate
- Check that Gmail API is enabled in Google Cloud Console

### SMTP Not Working
- Make sure `GMAIL_APP_PASSWORD` is set in `.env` file
- Verify 2-Step Verification is enabled on the Gmail account
- Check that the app password is correct (16 characters)

### No Channels Found
- Verify YouTube API key is correct and has quota
- Check API keys in `.env` file
- Some platforms may require additional authentication

### No Emails Found
- Many channels don't publicly display email addresses
- The system will try to generate email addresses based on usernames
- Check the lead collection results in the UI

## Notes

- The system uses AI to analyze channel content and determine if they can hire editors
- Email sending requires either Gmail API or SMTP authentication
- Make sure to comply with anti-spam laws (CAN-SPAM Act, GDPR, etc.)
- Use responsibly and ethically
- Test with small batches first

## Theme

The application uses a black and pink color scheme:
- Primary: #FF1493 (Deep Pink)
- Secondary: #000000 (Black)
- Accent: #FF69B4 (Hot Pink)
- Background: #1a1a1a (Dark Gray)

