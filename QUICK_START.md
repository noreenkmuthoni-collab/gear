# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure `.env` File
Create a `.env` file with:
```env
YOUTUBE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GMAIL_APP_PASSWORD=your_app_password_here
```

### Step 3: Run the Application
```bash
python run.py
```

Or:
```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

## 📧 Email Configuration

The system is configured to send emails from **maxxichorea@gmail.com**.

**Two ways to send emails:**

1. **Gmail API** (Recommended)
   - Download `credentials.json` from Google Cloud Console
   - Place it in the root directory
   - Authenticate on first run

2. **SMTP Fallback**
   - Set `GMAIL_APP_PASSWORD` in `.env` file
   - Get app password from [Google Account](https://myaccount.google.com/apppasswords)

## 🎨 Theme

The application uses a **Black & Pink** color scheme:
- Primary: #FF1493 (Deep Pink)
- Secondary: #000000 (Black)
- Accent: #FF69B4 (Hot Pink)

## 🔧 How It Works

1. **Collect Channels**: Searches YouTube, Instagram, TikTok for channels
2. **Analyze Posts**: Uses AI to analyze last posts and determine if they can hire editors
3. **Extract Emails**: Finds email addresses from channel descriptions and pages
4. **Send Emails**: Sends personalized cold emails with black & pink theme

## 📝 Full Automation

Click "Run Full Automation" to:
- ✅ Collect channels from all platforms
- ✅ Analyze posts using AI
- ✅ Filter channels that can hire editors
- ✅ Extract email addresses
- ✅ Send personalized cold emails

## ⚠️ Important Notes

- Make sure to comply with anti-spam laws (CAN-SPAM Act, GDPR)
- Test with small batches first
- Use responsibly and ethically
- Some channels may not have public email addresses

## 🆘 Need Help?

- See `README.md` for detailed documentation
- See `SETUP_GUIDE.md` for step-by-step setup instructions
- Check the troubleshooting section in README.md

