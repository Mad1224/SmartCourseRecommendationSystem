# Git Push Guide - Smart Course Recommendation System

## Step 1: Add all your changes
```bash
git add .
```

## Step 2: Commit your changes
```bash
git commit -m "Add Smart Course Recommendation System with 106 courses from 6 IIUM Kulliyyahs"
```

## Step 3: Setup remote repository (if not already done)

### Option A: If you already have a GitHub repository
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Option B: Create new repository on GitHub first
1. Go to https://github.com
2. Click "New repository"
3. Name it (e.g., "SmartCourseRecommendationSystem")
4. Don't initialize with README (you already have code)
5. Copy the repository URL
6. Run:
```bash
git remote add origin YOUR_REPO_URL
```

## Step 4: Push to GitHub
```bash
# First time push (set upstream)
git push -u origin main

# Or if your branch is named master
git push -u origin master

# For subsequent pushes
git push
```

## Quick Commands (Copy & Paste)

```bash
# Navigate to your project
cd c:\Users\mafla\OneDrive\Documents\SmartCourseRecommendationSystem

# Add all files
git add .

# Commit
git commit -m "Complete implementation: Backend API, ML recommendation engine, Flutter frontend, 106 courses from 6 IIUM kulliyyahs"

# Check if remote exists
git remote -v

# If no remote, add one (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/SmartCourseRecommendationSystem.git

# Push
git push -u origin main
```

## If you get errors:

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Error: "remote origin already exists"
```bash
# Remove old remote and add new one
git remote remove origin
git remote add origin YOUR_NEW_URL
```

### Error: "src refspec main does not match any"
```bash
# Your branch might be named master
git push -u origin master
```

## Verify your push
After pushing, go to your GitHub repository URL and refresh the page. You should see all your files!

## What will be pushed:
✓ Backend Python code (API, ML engine, routes)
✓ Frontend Flutter code (screens, services, models)
✓ Configuration files
✓ Course data (106 courses CSV)
✓ Documentation and guides
✓ Requirements files

## What will NOT be pushed (in .gitignore):
✗ __pycache__ folders
✗ .env files
✗ build outputs
✗ node_modules
✗ Virtual environments
✗ Database files
✗ Model artifacts
