# PowerShell script to push code to GitHub
# Repository: https://github.com/noreenkmuthoni-collab/gear.git

Write-Host "🚀 Preparing to push to GitHub..." -ForegroundColor Cyan
Write-Host "Repository: https://github.com/noreenkmuthoni-collab/gear.git" -ForegroundColor Yellow
Write-Host ""

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or use GitHub Desktop: https://desktop.github.com/" -ForegroundColor Yellow
    exit 1
}

# Initialize git if not already initialized
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Cyan
    git init
} else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

# Add all files
Write-Host "📝 Adding files..." -ForegroundColor Cyan
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Committing changes..." -ForegroundColor Cyan
    git commit -m "Initial commit: Cold Email Automation AI - Full working system with YT/IG/TikTok channel collection, AI analysis, lead collection, and email automation"
} else {
    Write-Host "⚠️  No changes to commit" -ForegroundColor Yellow
}

# Check if remote already exists
$remoteExists = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Cyan
    git remote add origin https://github.com/noreenkmuthoni-collab/gear.git
} else {
    Write-Host "✅ Remote already configured: $remoteExists" -ForegroundColor Green
    Write-Host "🔄 Updating remote URL..." -ForegroundColor Cyan
    git remote set-url origin https://github.com/noreenkmuthoni-collab/gear.git
}

# Set main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Cyan
git branch -M main

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "You may be prompted for credentials..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Repository: https://github.com/noreenkmuthoni-collab/gear" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Check your credentials and try again." -ForegroundColor Red
    Write-Host "You may need to authenticate with GitHub." -ForegroundColor Yellow
}

