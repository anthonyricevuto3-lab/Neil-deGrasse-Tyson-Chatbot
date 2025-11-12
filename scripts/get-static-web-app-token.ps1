# Get Static Web App Deployment Token

Write-Host "🔑 Getting Static Web App Deployment Token..." -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed." -ForegroundColor Red
    Write-Host "Install from: https://aka.ms/azure-cli" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Login
Write-Host "📝 Please login to Azure..." -ForegroundColor Cyan
az login

Write-Host ""
Write-Host "🔐 Retrieving Static Web App API token..." -ForegroundColor Cyan

$token = az staticwebapp secrets list `
  --name "Neil-deGrasse-Tyson-Chatbot-WA" `
  --resource-group "Neil-deGrasse-Tyson-Chatbot-RG" `
  --query "properties.apiKey" `
  --output tsv

if ($token) {
    Write-Host ""
    Write-Host "✅ Token retrieved successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "COPY THIS TOKEN TO GITHUB SECRETS" -ForegroundColor Yellow
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host $token -ForegroundColor White
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Copy the token above" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Go to GitHub repository secrets:" -ForegroundColor White
    Write-Host "   https://github.com/anthonyricevuto3-lab/Neil-deGrasse-Tyson-Chatbot/settings/secrets/actions" -ForegroundColor Blue
    Write-Host ""
    Write-Host "3. Add new secret:" -ForegroundColor White
    Write-Host "   - Name: AZURE_STATIC_WEB_APPS_API_TOKEN" -ForegroundColor Yellow
    Write-Host "     Value: [Paste the token above]" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Run the 'Deploy to Existing Azure Resources' workflow" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    
    # Try to copy to clipboard
    try {
        $token | Set-Clipboard
        Write-Host ""
        Write-Host "📋 Token has been copied to your clipboard!" -ForegroundColor Green
    } catch {
        Write-Host ""
        Write-Host "💡 Tip: Manually copy the token above" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "❌ Failed to retrieve token" -ForegroundColor Red
    Write-Host "Make sure you have access to the resource group" -ForegroundColor Yellow
}
