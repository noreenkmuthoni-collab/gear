# Git Setup and Push Instructions

## Prerequisites

Make sure Git is installed on your system:
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)
- Or use GitHub Desktop: [desktop.github.com](https://desktop.github.com/)

## Step 1: Initialize Git Repository

Open terminal/PowerShell in the project directory and run:

```bash
git init
```

## Step 2: Add All Files

```bash
git add .
```

## Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Cold Email Automation AI - Full working system with YT/IG/TikTok channel collection, AI analysis, lead collection, and email automation"
```

## Step 4: Create GitHub Repository (if not exists)

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `cold-email-automation-ai` (or any name you prefer)
3. **Don't** initialize with README, .gitignore, or license (we already have these)

## Step 5: Add Remote Repository

Replace `YOUR_USERNAME` and `REPO_NAME` with your actual GitHub username and repository name:

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

Or if using SSH:
```bash
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
```

## Step 6: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

## Alternative: Quick Setup Script

Once Git is installed, you can run these commands in sequence:

```bash
# Initialize repository
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Cold Email Automation AI"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Important Notes

### Files Excluded by .gitignore:
- `.env` - Contains sensitive API keys
- `credentials.json` - Gmail API credentials
- `token.json` - Gmail API token
- `__pycache__/` - Python cache files
- `venv/` - Virtual environment

### Before Pushing:
1. ✅ Make sure `.env` file is NOT committed (it's in .gitignore)
2. ✅ Make sure `credentials.json` is NOT committed (it's in .gitignore)
3. ✅ Make sure `token.json` is NOT committed (it's in .gitignore)
4. ✅ Create a `.env.example` file if you want to show what variables are needed

## Troubleshooting

### If you get "fatal: not a git repository"
Run `git init` first

### If you get "fatal: remote origin already exists"
Remove it first:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### If you get authentication errors
- Use GitHub Desktop for easier authentication
- Or set up SSH keys: [GitHub SSH Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### If you need to update after changes
```bash
git add .
git commit -m "Update: your change description"
git push
```

## Repository Structure

Your repository will include:
- ✅ All Python source files
- ✅ HTML templates
- ✅ Documentation (README, SETUP_GUIDE, etc.)
- ✅ Requirements.txt
- ✅ .gitignore
- ❌ .env (excluded - contains secrets)
- ❌ credentials.json (excluded - contains secrets)
- ❌ token.json (excluded - contains secrets)

