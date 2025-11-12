# Deployment to Your Existing Azure Resources

## Current Resources in West US

You have already provisioned:
- ✅ App Service Plan: `ASP-NeildeGrasseTysonChatbotRG-b379`
- ✅ Storage Account: `ndtchatbotstorage`
- ✅ Function App: `Neil-deGrasse-Tyson-Chatbot-FA`
- ✅ Static Web App: `Neil-deGrasse-Tyson-Chatbot-WA`
- ✅ Application Insights: `Neil-deGrasse-Tyson-Chatbot-FA`
- ✅ Azure OpenAI: `Neil-deGrasse-Tyson-Chatbot-FA-openai-9fc8`
- ✅ Search Service: `neil-degrasse-tyson-chatbot-fa-search-a673`
- ✅ Managed Identity: `Neil-deGrasse-Ty-id-8836`

## Deployment Strategy

### Option 1: Use Static Web App + App Service (Recommended)

**Frontend** → Static Web App: `Neil-deGrasse-Tyson-Chatbot-WA`
**Backend** → Create new App Service (FastAPI) on your App Service Plan

### Option 2: Convert to Azure Functions

Convert your FastAPI app to Azure Functions (requires code restructuring)

---

## Quick Deploy - Option 1 (Recommended)

### Step 1: Deploy Backend to App Service

```bash
# Create a Web App for the backend
az webapp create \
  --name ndt-backend-api \
  --resource-group Neil-deGrasse-Tyson-Chatbot-RG \
  --plan ASP-NeildeGrasseTysonChatbotRG-b379 \
  --runtime "PYTHON:3.11" \
  --deployment-container-image-name ghcr.io/anthonyricevuto3-lab/neil-degrasse-tyson-chatbot/backend:main

# Configure environment variables
az webapp config appsettings set \
  --name ndt-backend-api \
  --resource-group Neil-deGrasse-Tyson-Chatbot-RG \
  --settings \
    OPENAI_API_KEY="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" \
    WEBSITES_PORT=8000

# Get backend URL
az webapp show --name ndt-backend-api --resource-group Neil-deGrasse-Tyson-Chatbot-RG --query defaultHostName -o tsv
```

### Step 2: Deploy Frontend to Static Web App

The Static Web App is already created. We'll connect it to your GitHub repo:

```bash
# Get deployment token
az staticwebapp secrets list \
  --name Neil-deGrasse-Tyson-Chatbot-WA \
  --resource-group Neil-deGrasse-Tyson-Chatbot-RG \
  --query properties.apiKey -o tsv
```

Then add this as a GitHub secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`

---

## I'll Create the Deployment Workflows

Let me create automated GitHub Actions workflows that deploy to your existing resources.
