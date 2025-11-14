#!/bin/bash

# Solis Cloud Home Assistant Integration Setup Script
# This script will initialize the git repository, commit all files,
# create a GitHub repository, push the code, and create the first release.

set -e  # Exit on error

echo "=========================================="
echo "Solis Cloud Integration Setup"
echo "=========================================="
echo ""

# Configuration
REPO_NAME="solis-cloud-homeassistant"
GITHUB_USERNAME="danvaly"
VERSION="1.0.8"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to the repository directory
cd "$(dirname "$0")"

echo -e "${YELLOW}Step 1: Initializing Git repository...${NC}"
git init
echo -e "${GREEN}Git repository initialized.${NC}"
echo ""

echo -e "${YELLOW}Step 2: Adding all files to Git...${NC}"
git add .
echo -e "${GREEN}All files staged.${NC}"
echo ""

echo -e "${YELLOW}Step 3: Creating initial commit...${NC}"
git commit -m "Initial commit: Solis Cloud integration v${VERSION}

- Complete Home Assistant integration for Solis Cloud
- Support for power and energy monitoring
- Config flow for easy setup
- HACS compatible
- GitHub Actions for validation"
echo -e "${GREEN}Initial commit created.${NC}"
echo ""

echo -e "${YELLOW}Step 4: Creating main branch...${NC}"
git branch -M main
echo -e "${GREEN}Main branch created.${NC}"
echo ""

echo -e "${YELLOW}Step 5: Checking if GitHub CLI is installed...${NC}"
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI (gh) is not installed.${NC}"
    echo "Please install it from: https://cli.github.com/"
    echo ""
    echo "After installing, run: gh auth login"
    echo "Then run this script again."
    exit 1
fi
echo -e "${GREEN}GitHub CLI is installed.${NC}"
echo ""

echo -e "${YELLOW}Step 6: Checking GitHub authentication...${NC}"
if ! gh auth status &> /dev/null; then
    echo -e "${RED}You are not authenticated with GitHub CLI.${NC}"
    echo "Please run: gh auth login"
    echo "Then run this script again."
    exit 1
fi
echo -e "${GREEN}GitHub authentication verified.${NC}"
echo ""

echo -e "${YELLOW}Step 7: Creating GitHub repository...${NC}"
if gh repo view ${GITHUB_USERNAME}/${REPO_NAME} &> /dev/null; then
    echo -e "${YELLOW}Repository already exists. Skipping creation.${NC}"
else
    gh repo create ${REPO_NAME} --public --source=. --description="Home Assistant integration for Solis Cloud solar inverter monitoring" --remote=origin
    echo -e "${GREEN}GitHub repository created.${NC}"
fi
echo ""

echo -e "${YELLOW}Step 8: Pushing to GitHub...${NC}"
git push -u origin main
echo -e "${GREEN}Code pushed to GitHub.${NC}"
echo ""

echo -e "${YELLOW}Step 9: Creating release v${VERSION}...${NC}"
git tag -a "v${VERSION}" -m "Release version ${VERSION}

Features:
- Complete Solis Cloud integration
- Real-time power monitoring
- Energy tracking (daily, monthly, yearly, total)
- Inverter status monitoring
- Config flow for easy setup
- HACS compatible

Installation:
- Install via HACS as custom repository
- Configure with your Solis Cloud API credentials"

git push origin "v${VERSION}"

gh release create "v${VERSION}" \
    --title "v${VERSION} - Initial Release" \
    --notes "## Solis Cloud Integration v${VERSION}

### Features
- Real-time monitoring of Solis solar inverters
- Energy production tracking (today, month, year, total)
- Current power output monitoring
- Inverter status monitoring
- Automatic data updates every 5 minutes
- Easy configuration through Home Assistant UI

### Installation
Install via HACS by adding this repository as a custom integration:
\`https://github.com/${GITHUB_USERNAME}/${REPO_NAME}\`

### Configuration
You'll need your Solis Cloud API credentials:
- API Key ID
- API Secret
- Username

See the [README](https://github.com/${GITHUB_USERNAME}/${REPO_NAME}#readme) for detailed instructions.

### Requirements
- Home Assistant 2023.1.0 or newer
- Solis Cloud account with API access"

echo -e "${GREEN}Release v${VERSION} created.${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Your integration is now published!"
echo ""
echo "Repository URL: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo "Release URL: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}/releases/tag/v${VERSION}"
echo ""
echo "Next steps:"
echo "1. Add this repository to HACS as a custom integration"
echo "2. Install the integration through HACS"
echo "3. Configure it in Home Assistant with your API credentials"
echo ""
echo "To add to HACS:"
echo "   HACS > Integrations > ... (menu) > Custom repositories"
echo "   Repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo "   Category: Integration"
echo ""
