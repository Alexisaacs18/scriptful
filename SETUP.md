# 🚀 Scriptful GitHub Repository Setup Guide

This guide will walk you through the complete process of setting up Scriptful in a GitHub repository.

## 📋 Prerequisites

- GitHub account
- Git installed on your local machine
- GitHub CLI (optional but recommended)
- All Scriptful services running locally

## 🎯 Step-by-Step Setup

### 1. **Prepare Your Local Project**

First, ensure your project is clean and ready:

```bash
# Navigate to your Scriptful project directory
cd /path/to/your/Script_Full

# Remove any temporary files or logs
rm -rf logs/*.log
rm -rf __pycache__
rm -rf node_modules
rm -rf .env
```

### 2. **Create a New GitHub Repository**

#### Option A: Using GitHub Web Interface
1. Go to [GitHub.com](https://github.com)
2. Click the "+" icon → "New repository"
3. Repository name: `scriptful`
4. Description: `AI-powered movie script generator with OpenAI integration`
5. Make it **Public** (recommended for open source)
6. **Don't** initialize with README, .gitignore, or license (we'll add our own)
7. Click "Create repository"

#### Option B: Using GitHub CLI
```bash
gh repo create scriptful --public --description "AI-powered movie script generator with OpenAI integration"
```

### 3. **Initialize Git and Add Files**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Scriptful AI Movie Script Generator

- AI service with OpenAI integration
- Node.js backend API
- React frontend with modern UI
- Comprehensive training data (29+ screenplay files)
- Standalone HTML interface
- Docker support
- Complete documentation"

# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/scriptful.git

# Push to main branch
git branch -M main
git push -u origin main
```

### 4. **Set Up Branch Protection (Recommended)**

1. Go to your repository → Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

### 5. **Create Development Workflow**

```bash
# Create and switch to develop branch
git checkout -b develop

# Push develop branch
git push -u origin develop

# Switch back to main
git checkout main
```

### 6. **Set Up GitHub Actions**

The CI/CD pipeline is already configured in `.github/workflows/ci.yml`. It will:
- Test backend with multiple Node.js versions
- Test frontend with multiple Node.js versions  
- Test AI service with multiple Python versions
- Run security audits
- Deploy previews for pull requests

### 7. **Configure Repository Settings**

#### Repository Settings
1. **General**: Enable Issues, Wikis, Discussions
2. **Pages**: Set up GitHub Pages if desired
3. **Security**: Enable Dependabot alerts
4. **Actions**: Ensure Actions are enabled

#### Environment Variables (if deploying)
1. Go to Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DEPLOY_KEY`: SSH key for deployment
   - `ENVIRONMENT`: production/staging

### 8. **Create Project Structure**

```bash
# Create project board
gh project create --title "Scriptful Development" --format board

# Create initial issues
gh issue create --title "Setup CI/CD Pipeline" --body "Configure GitHub Actions for automated testing and deployment"
gh issue create --title "Add Unit Tests" --body "Implement comprehensive test coverage for all services"
gh issue create --title "Documentation" --body "Create user guides and API documentation"
gh issue create --title "Performance Optimization" --body "Optimize AI service response times and frontend performance"
```

### 9. **Set Up Dependabot**

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/ai-service"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  # Node.js dependencies
  - package-ecosystem: "npm"
    directory: "/backend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 10. **Create Release Strategy**

```bash
# Create first release
gh release create v1.0.0 --title "Scriptful v1.0.0" --notes "
## 🎉 Initial Release

### Features
- AI-powered script generation
- Modern chatbot interface
- Comprehensive training data
- Multi-service architecture

### Technical
- Python Flask AI service
- Node.js Express backend
- React frontend with Vite
- Docker containerization
- GitHub Actions CI/CD

### Getting Started
See README.md for installation and usage instructions.
"
```

## 🔧 Post-Setup Tasks

### 1. **Update Documentation**
- Update README.md with your GitHub username
- Add contribution guidelines
- Create issue templates

### 2. **Set Up Monitoring**
- Enable GitHub Insights
- Set up repository analytics
- Configure notifications

### 3. **Community Setup**
- Create discussion categories
- Set up issue templates
- Enable project wiki

## 📊 Repository Health Checklist

- [ ] README.md is comprehensive
- [ ] .gitignore covers all file types
- [ ] LICENSE file is present
- [ ] CI/CD pipeline is working
- [ ] Branch protection is enabled
- [ ] Dependabot is configured
- [ ] Issues and discussions are enabled
- [ ] Security scanning is active
- [ ] Documentation is up to date

## 🚨 Important Notes

### **Security Considerations**
- **Never commit API keys** - use environment variables
- **Review training data** - ensure no copyrighted material
- **Enable security scanning** - GitHub Advanced Security if available

### **Legal Considerations**
- **Training data**: Ensure you have rights to use screenplay content
- **OpenAI usage**: Review OpenAI's terms of service
- **Licensing**: MIT License allows commercial use

### **Performance Considerations**
- **Large files**: Consider Git LFS for training data
- **Dependencies**: Regular security updates via Dependabot
- **CI/CD**: Optimize workflow execution time

## 🎯 Next Steps

1. **Share your repository** with the community
2. **Accept contributions** from other developers
3. **Monitor and maintain** the project
4. **Plan future features** based on user feedback
5. **Scale the application** as it grows

## 📞 Support

If you encounter issues during setup:
- Check GitHub's documentation
- Review the CI/CD logs
- Create an issue in the repository
- Ask the community for help

---

**Happy coding! 🎬✨**
