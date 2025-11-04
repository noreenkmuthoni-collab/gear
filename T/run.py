#!/usr/bin/env python3
"""
Quick start script for Cold Email Automation AI
"""
import sys
import os

# Check if .env file exists
if not os.path.exists('.env'):
    print("⚠️  WARNING: .env file not found!")
    print("Please create a .env file with the following variables:")
    print("  - YOUTUBE_API_KEY")
    print("  - OPENAI_API_KEY")
    print("  - GMAIL_APP_PASSWORD (optional if using Gmail API)")
    print("\nSee README.md or SETUP_GUIDE.md for more details.")
    response = input("\nContinue anyway? (y/n): ")
    if response.lower() != 'y':
        sys.exit(1)

# Check if credentials.json exists (optional for Gmail API)
if not os.path.exists('credentials.json'):
    print("⚠️  NOTE: credentials.json not found.")
    print("The system will use SMTP fallback for email sending.")
    print("Make sure GMAIL_APP_PASSWORD is set in .env file.")
    print("\nTo use Gmail API instead, set up credentials.json (see README.md)")

# Run the Flask app
from app import app

if __name__ == '__main__':
    print("\n🚀 Starting Cold Email Automation AI...")
    print("📧 Email sender: maxxichorea@gmail.com")
    print("🎨 Theme: Black & Pink")
    print("🌐 Server running at http://localhost:5000")
    print("\nPress CTRL+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

