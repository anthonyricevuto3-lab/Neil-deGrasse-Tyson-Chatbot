# Azure Deployment Guide

## Prerequisites

1. **Azure CLI**: Install from https://aka.ms/azure-cli
2. **Azure Account**: Active subscription
3. **GitHub Secrets**: Configure in your repository

## Setup GitHub Secrets

### 1. Create Azure Service Principal

```bash
az ad sp create-for-rbac \
  --name "github-ndt-chatbot" \
  --role contributor \
  --scopes /subscriptions/<YOUR_SUBSCRIPTION_ID> \
  --sdk-auth
```

Copy the entire JSON output.

### 2. Add GitHub Secrets

Go to: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Add these secrets:

- **AZURE_CREDENTIALS**: Paste the JSON from step 1
- **OPENAI_API_KEY**: Your OpenAI API key

## Deployment Options

### Option 1: Azure Container Apps (Recommended for FastAPI)

**Pros:**
- Works with your existing Docker setup
- Auto-scaling
- Easy deployment from GitHub Actions
- $30-50/month for basic usage

**Deploy:**
```bash
# Push the workflow file
git add .github/workflows/azure-deploy.yml
git commit -m "Add Azure Container Apps deployment"
git push origin main

# Trigger deployment manually
# Go to GitHub Actions → "Deploy to Azure Container Apps" → "Run workflow"
```

The workflow will:
1. Create resource group and container environment
2. Deploy backend container (FastAPI)
3. Deploy frontend container (React/Vite)
4. Configure environment variables
5. Output the public URLs

**After deployment:**
- Backend API: `https://ndt-backend.{random}.eastus.azurecontainerapps.io`
- Frontend: `https://ndt-frontend.{random}.eastus.azurecontainerapps.io`

### Option 2: Azure Functions (Requires Code Changes)

**NOT RECOMMENDED** - Your app is FastAPI, not Azure Functions.

To use Azure Functions, you would need to:
1. Create `host.json` and `function.json` files
2. Rewrite FastAPI endpoints as Azure Functions
3. Change project structure significantly

## Cost Estimates

### Azure Container Apps
- **Backend**: 1 vCPU, 2GB RAM → ~$25/month
- **Frontend**: 0.5 vCPU, 1GB RAM → ~$12/month
- **Total**: ~$37/month + minimal ingress/egress costs

### Reduce Costs
```bash
# Scale to zero when idle (Consumption plan)
az containerapp update \
  --name ndt-backend \
  --resource-group ndt-chatbot-rg \
  --min-replicas 0 \
  --max-replicas 3
```

## Manual Deployment (Alternative)

If you prefer to deploy manually instead of using GitHub Actions:

```bash
# Login to Azure
az login

# Set variables
RESOURCE_GROUP="ndt-chatbot-rg"
LOCATION="eastus"
BACKEND_IMAGE="ghcr.io/anthonyricevuto3-lab/neil-degrasse-tyson-chatbot/backend:main"
FRONTEND_IMAGE="ghcr.io/anthonyricevuto3-lab/neil-degrasse-tyson-chatbot/frontend:main"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create container environment
az containerapp env create \
  --name ndt-env \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Deploy backend
az containerapp create \
  --name ndt-backend \
  --resource-group $RESOURCE_GROUP \
  --environment ndt-env \
  --image $BACKEND_IMAGE \
  --target-port 8000 \
  --ingress external \
  --env-vars OPENAI_API_KEY=<YOUR_KEY> \
  --cpu 1.0 \
  --memory 2.0Gi \
  --min-replicas 1 \
  --max-replicas 3

# Get backend URL
BACKEND_URL=$(az containerapp show \
  --name ndt-backend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

# Deploy frontend
az containerapp create \
  --name ndt-frontend \
  --resource-group $RESOURCE_GROUP \
  --environment ndt-env \
  --image $FRONTEND_IMAGE \
  --target-port 80 \
  --ingress external \
  --env-vars VITE_API_URL=https://$BACKEND_URL \
  --cpu 0.5 \
  --memory 1.0Gi \
  --min-replicas 1 \
  --max-replicas 2

# Get frontend URL
FRONTEND_URL=$(az containerapp show \
  --name ndt-frontend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo "🚀 Deployed!"
echo "Frontend: https://$FRONTEND_URL"
echo "Backend: https://$BACKEND_URL"
```

## Monitoring

View logs:
```bash
# Backend logs
az containerapp logs show \
  --name ndt-backend \
  --resource-group ndt-chatbot-rg \
  --follow

# Frontend logs
az containerapp logs show \
  --name ndt-frontend \
  --resource-group ndt-chatbot-rg \
  --follow
```

## Cleanup

Delete everything:
```bash
az group delete --name ndt-chatbot-rg --yes --no-wait
```

## Troubleshooting

### Issue: "Cannot find required host.json"
**Solution**: You tried to deploy to Azure Functions. Use Azure Container Apps instead (this guide).

### Issue: Docker build fails on "storage/" not found
**Solution**: Already fixed in latest commit. The storage directory is created during build.

### Issue: OpenAI API errors
**Solution**: Verify `OPENAI_API_KEY` secret is set correctly in GitHub or Azure.

### Issue: CORS errors in frontend
**Solution**: Update backend to allow frontend origin:
```python
# backend/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ndt-frontend.*.azurecontainerapps.io"],
    # ...
)
```

## Next Steps

1. **Set up GitHub secrets** (AZURE_CREDENTIALS, OPENAI_API_KEY)
2. **Push workflow file** to trigger deployment
3. **Test the deployed app** using the URLs from GitHub Actions output
4. **Set up custom domain** (optional)
5. **Configure monitoring** with Application Insights (optional)
