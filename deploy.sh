#!/usr/bin/env bash
set -euo pipefail

# Required tools:
# - Azure CLI (`az`)
# - GitHub CLI (`gh`)
# - git

# Update these values before running:
GITHUB_OWNER="<your-github-username-or-org>"
REPO_NAME="habit-streak-tracker"
AZURE_SUBSCRIPTION_ID="<your-azure-subscription-id>"
AZURE_RESOURCE_GROUP="habit-streak-rg"
AZURE_LOCATION="eastus2"
AZURE_STATIC_WEB_APP_NAME="habit-streak-tracker-app"
DESCRIPTION_PREFIX="Habit Streak Tracker live at"

# 1) Authenticate
az login
az account set --subscription "$AZURE_SUBSCRIPTION_ID"
gh auth login

# 2) Create GitHub repository (skip if already created)
gh repo create "$GITHUB_OWNER/$REPO_NAME" --public --source=. --remote=origin --push

# 3) Create Azure resource group
az group create \
  --name "$AZURE_RESOURCE_GROUP" \
  --location "$AZURE_LOCATION"

# 4) Create Azure Static Web App resource
az extension add --name staticwebapp --upgrade
az staticwebapp create \
  --name "$AZURE_STATIC_WEB_APP_NAME" \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --location "$AZURE_LOCATION" \
  --sku Free

# 5) Generate deployment token and store in GitHub Actions secret
DEPLOY_TOKEN="$(az staticwebapp secrets list \
  --name "$AZURE_STATIC_WEB_APP_NAME" \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --query properties.apiKey \
  -o tsv)"

gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN --repo "$GITHUB_OWNER/$REPO_NAME" --body "$DEPLOY_TOKEN"

# 6) Push code to trigger workflow
git branch -M main
git push -u origin main

# 7) Fetch live URL and update repository description
LIVE_HOSTNAME="$(az staticwebapp show \
  --name "$AZURE_STATIC_WEB_APP_NAME" \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --query defaultHostname \
  -o tsv)"

LIVE_URL="https://$LIVE_HOSTNAME"
gh repo edit "$GITHUB_OWNER/$REPO_NAME" --description "$DESCRIPTION_PREFIX $LIVE_URL"

echo "Deployment complete. Live URL: $LIVE_URL"
