#!/bin/bash
# Azure Service Principal Setup Script for GitHub Actions

set -e

echo "🔧 Azure Service Principal Setup for GitHub Actions"
echo "=================================================="
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed."
    echo "Install from: https://aka.ms/azure-cli"
    exit 1
fi

echo "✅ Azure CLI is installed"
echo ""

# Login to Azure
echo "📝 Logging into Azure..."
az login

# Get subscription ID
echo ""
echo "📋 Getting subscription information..."
SUBSCRIPTION_ID=$(az account show --query id --output tsv)
SUBSCRIPTION_NAME=$(az account show --query name --output tsv)

echo "✅ Using subscription:"
echo "   Name: $SUBSCRIPTION_NAME"
echo "   ID: $SUBSCRIPTION_ID"
echo ""

# Confirm with user
read -p "Is this the correct subscription? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled. Please select the correct subscription using:"
    echo "   az account set --subscription <SUBSCRIPTION_ID>"
    exit 1
fi

# Create service principal
echo ""
echo "🔐 Creating service principal..."
SP_OUTPUT=$(az ad sp create-for-rbac \
  --name "github-ndt-chatbot-$(date +%s)" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID \
  --sdk-auth)

echo ""
echo "✅ Service principal created successfully!"
echo ""
echo "=================================================="
echo "COPY THIS JSON TO GITHUB SECRETS"
echo "=================================================="
echo ""
echo "$SP_OUTPUT"
echo ""
echo "=================================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Copy the JSON above (entire block)"
echo ""
echo "2. Go to your GitHub repository:"
echo "   https://github.com/anthonyricevuto3-lab/Neil-deGrasse-Tyson-Chatbot/settings/secrets/actions"
echo ""
echo "3. Click 'New repository secret'"
echo ""
echo "4. Create two secrets:"
echo "   - Name: AZURE_CREDENTIALS"
echo "     Value: [Paste the JSON above]"
echo ""
echo "   - Name: OPENAI_API_KEY"
echo "     Value: [Your OpenAI API key]"
echo ""
echo "5. Go to Actions tab and run 'Deploy to Azure Container Apps'"
echo ""
echo "✅ Setup complete!"
