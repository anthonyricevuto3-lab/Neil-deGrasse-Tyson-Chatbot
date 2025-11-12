# Azure Deployment Setup Guide

## Quick Setup (5 minutes)

### Step 1: Create Azure Service Principal

Open a terminal and run:

```bash
# Login to Azure
az login

# Get your subscription ID
az account show --query id --output tsv

# Create service principal (replace <SUBSCRIPTION_ID> with your actual ID)
az ad sp create-for-rbac \
  --name "github-ndt-chatbot" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID> \
  --sdk-auth
```

**Copy the entire JSON output** - you'll need it in the next step.

Example output:
```json
{
  "clientId": "xxxx-xxxx-xxxx-xxxx",
  "clientSecret": "xxxx-xxxx-xxxx-xxxx",
  "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
  "tenantId": "xxxx-xxxx-xxxx-xxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository: https://github.com/anthonyricevuto3-lab/Neil-deGrasse-Tyson-Chatbot

2. Click **Settings** → **Secrets and variables** → **Actions**

3. Click **New repository secret**

4. Add these two secrets:

   **Secret 1: AZURE_CREDENTIALS**
   - Name: `AZURE_CREDENTIALS`
   - Value: Paste the entire JSON from Step 1
   
   **Secret 2: OPENAI_API_KEY**
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key (starts with `sk-`)

### Step 3: Trigger Deployment

1. Go to **Actions** tab in your GitHub repository

2. Click on **"Deploy to Azure Container Apps"** workflow

3. Click **"Run workflow"** → **"Run workflow"**

4. Wait 5-10 minutes for deployment to complete

5. Check the workflow output for your deployed URLs:
   ```
   🚀 Frontend deployed to: https://ndt-frontend.{random}.eastus.azurecontainerapps.io
   🔗 Backend API: https://ndt-backend.{random}.eastus.azurecontainerapps.io
   ```

## Troubleshooting

### Error: "Login failed... Not all values are present"
**Solution**: Make sure you added the `AZURE_CREDENTIALS` secret with the complete JSON from Step 1.

### Error: "Unauthorized to perform action"
**Solution**: The service principal needs contributor role. Re-run the `az ad sp create-for-rbac` command with `--role contributor`.

### Error: "Subscription not found"
**Solution**: Make sure you're logged into the correct Azure account:
```bash
az account list --output table
az account set --subscription <SUBSCRIPTION_ID>
```

### Error: OpenAI API errors in logs
**Solution**: Verify the `OPENAI_API_KEY` secret is set correctly in GitHub.

## Cost Management

### Expected Monthly Cost
- Backend: ~$25/month (1 vCPU, 2GB RAM)
- Frontend: ~$12/month (0.5 vCPU, 1GB RAM)
- **Total: ~$37/month**

### Scale to Zero (Save money when not in use)
```bash
az containerapp update \
  --name ndt-backend \
  --resource-group ndt-chatbot-rg \
  --min-replicas 0 \
  --max-replicas 3
```

### Delete Everything
```bash
az group delete --name ndt-chatbot-rg --yes --no-wait
```

## Manual Deployment (Alternative)

If you prefer not to use GitHub Actions:

```bash
# 1. Login
az login

# 2. Set variables
RESOURCE_GROUP="ndt-chatbot-rg"
LOCATION="eastus"

# 3. Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# 4. Create container environment
az containerapp env create \
  --name ndt-env \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# 5. Deploy backend
az containerapp create \
  --name ndt-backend \
  --resource-group $RESOURCE_GROUP \
  --environment ndt-env \
  --image ghcr.io/anthonyricevuto3-lab/neil-degrasse-tyson-chatbot/backend:main \
  --target-port 8000 \
  --ingress external \
  --env-vars OPENAI_API_KEY=<YOUR_KEY> \
  --cpu 1.0 \
  --memory 2.0Gi

# 6. Get backend URL
BACKEND_URL=$(az containerapp show \
  --name ndt-backend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

# 7. Deploy frontend
az containerapp create \
  --name ndt-frontend \
  --resource-group $RESOURCE_GROUP \
  --environment ndt-env \
  --image ghcr.io/anthonyricevuto3-lab/neil-degrasse-tyson-chatbot/frontend:main \
  --target-port 80 \
  --ingress external \
  --env-vars VITE_API_URL=https://$BACKEND_URL \
  --cpu 0.5 \
  --memory 1.0Gi

# 8. Get frontend URL
FRONTEND_URL=$(az containerapp show \
  --name ndt-frontend \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv)

echo "🚀 Deployed!"
echo "Frontend: https://$FRONTEND_URL"
echo "Backend: https://$BACKEND_URL"
```

## Next Steps

After successful deployment:

1. **Test the app** - Visit the frontend URL and try chatting
2. **Monitor logs** - Check Azure Portal → Container Apps → Logs
3. **Set up custom domain** (optional)
4. **Configure auto-scaling** based on usage
5. **Enable Application Insights** for monitoring

## Support

- Azure Container Apps Docs: https://learn.microsoft.com/en-us/azure/container-apps/
- GitHub Actions Docs: https://docs.github.com/en/actions
- Issues: https://github.com/anthonyricevuto3-lab/Neil-deGrasse-Tyson-Chatbot/issues
