# Git Commands for Your Repository

## Repository
**URL**: https://github.com/noreenkmuthoni-collab/gear.git

## Quick Push Commands

Once Git is installed, run these commands in order:

```bash
# 1. Initialize Git (if not already done)
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: Cold Email Automation AI - Full working system with YT/IG/TikTok channel collection, AI analysis, lead collection, and email automation"

# 4. Add remote repository
git remote add origin https://github.com/noreenkmuthoni-collab/gear.git

# 5. Set main branch
git branch -M main

# 6. Push to GitHub
git push -u origin main
```

## Using the Scripts

### Option 1: PowerShell Script
```powershell
.\push_to_github.ps1
```

### Option 2: Batch Script
```cmd
push_to_github.bat
```

## If Git is Not Installed

1. **Install Git for Windows**: [Download here](https://git-scm.com/download/win)
2. **Or use GitHub Desktop**: [Download here](https://desktop.github.com/)

### Using GitHub Desktop (Easier)

1. Download and install GitHub Desktop
2. Sign in with your GitHub account
3. File → Add Local Repository
4. Select this folder: `C:\Users\VVS\Pictures\T`
5. Click "Publish repository"
6. Repository name: `gear`
7. Owner: `noreenkmuthoni-collab`
8. Click "Publish Repository"

## Authentication

When pushing, you may need to authenticate:

- **HTTPS**: Use GitHub Personal Access Token (not password)
  - Create token: https://github.com/settings/tokens
  - Select scope: `repo`
  
- **SSH**: Use SSH keys (more secure)
  - Setup guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Files Excluded (by .gitignore)

These files will NOT be pushed:
- `.env` - Contains API keys
- `credentials.json` - Gmail API credentials  
- `token.json` - Gmail API token
- `__pycache__/` - Python cache
- `venv/` - Virtual environment

## After Initial Push

For future updates:

```bash
git add .
git commit -m "Update: description of changes"
git push
```

## Troubleshooting

### "fatal: not a git repository"
Run `git init` first

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/noreenkmuthoni-collab/gear.git
```

### Authentication errors
- Use GitHub Desktop for easier authentication
- Or set up Personal Access Token: https://github.com/settings/tokens

