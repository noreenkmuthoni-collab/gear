# Cold Email Automation AI

A full-featured cold email automation system that collects channels from YouTube, Instagram, and TikTok, analyzes their content, identifies potential clients who can hire editors, collects leads, and sends automated cold emails.

## Features

- **Multi-Platform Channel Collection**: Collects channels from YouTube, Instagram, and TikTok
- **AI-Powered Analysis**: Analyzes channel posts to determine if they can hire editors
- **Lead Collection**: Automatically extracts and collects email addresses from channels
- **Email Automation**: Sends personalized cold emails with black and pink theme
- **Beautiful UI**: Modern web interface with black and pink color scheme

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the root directory:

```env
YOUTUBE_API_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key
GMAIL_APP_PASSWORD=your_gmail_app_password
```

**Get API Keys:**
- **YouTube API**: [Google Cloud Console](https://console.cloud.google.com/) → Enable YouTube Data API v3 → Create API Key
- **OpenAI API**: [OpenAI Platform](https://platform.openai.com/) → API Keys → Create new key
- **Gmail App Password**: [Google Account](https://myaccount.google.com/apppasswords) → Enable 2-Step Verification → Generate App Password

### 3. Gmail API Setup (Optional - Recommended)

For more reliable email sending, set up Gmail API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials and save as `credentials.json` in the root directory
6. The first time you run the app, it will open a browser for authentication and create `token.json`

**Note**: If Gmail API is not set up, the system will use SMTP with the App Password from `.env` file.

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Manual Step-by-Step

1. **Collect Channels**: Enter a search query and select platforms, then click "Collect Channels"
2. **Analyze Channels**: The system will automatically analyze channels for editor hiring potential
3. **Collect Leads**: Extract email addresses from eligible channels
4. **Send Emails**: Send cold emails to collected leads

### Full Automation

Click "Run Full Automation" to perform all steps automatically:
- Collect channels
- Analyze posts
- Filter eligible channels
- Collect leads
- Send emails

## Email Configuration

The system uses `maxxichorea@gmail.com` to send emails. You can configure email sending in two ways:

**Option 1: Gmail API (Recommended)**
- Set up `credentials.json` as described above
- More reliable and secure
- Handles authentication automatically

**Option 2: SMTP Fallback**
- Set `GMAIL_APP_PASSWORD` in `.env` file
- Requires 2-Step Verification enabled on Gmail account
- Get app password from [Google Account](https://myaccount.google.com/apppasswords)

The system will automatically use Gmail API if available, otherwise fall back to SMTP.

## Theme

The application uses a black and pink color scheme:
- Primary: #FF1493 (Pink)
- Secondary: #000000 (Black)
- Accent: #FF69B4 (Hot Pink)

## Notes

- Some APIs (Instagram, TikTok) may require additional setup or authentication
- Email sending requires Gmail API credentials
- Make sure to comply with anti-spam laws and email regulations
- Use responsibly and ethically

## Troubleshooting

- **Gmail API errors**: Make sure `credentials.json` is in the root directory
- **API key errors**: Verify all API keys in `.env` file
- **No emails found**: Some channels may not have public email addresses
- **Authentication issues**: Delete `token.json` and re-authenticate

## License

This project is for educational and business purposes.
