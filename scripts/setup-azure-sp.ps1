# Azure Service Principal Setup Script for GitHub Actions
# Run this in PowerShell

Write-Host "🔧 Azure Service Principal Setup for GitHub Actions" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
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

# Login to Azure
Write-Host "📝 Logging into Azure..." -ForegroundColor Cyan
az login

# Get subscription ID
Write-Host ""
Write-Host "📋 Getting subscription information..." -ForegroundColor Cyan
$subscriptionId = az account show --query id --output tsv
$subscriptionName = az account show --query name --output tsv

Write-Host "✅ Using subscription:" -ForegroundColor Green
Write-Host "   Name: $subscriptionName" -ForegroundColor White
Write-Host "   ID: $subscriptionId" -ForegroundColor White
Write-Host ""

# Confirm with user
$confirmation = Read-Host "Is this the correct subscription? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "❌ Cancelled. Please select the correct subscription using:" -ForegroundColor Red
    Write-Host "   az account set --subscription <SUBSCRIPTION_ID>" -ForegroundColor Yellow
    exit 1
}

# Create service principal
Write-Host ""
Write-Host "🔐 Creating service principal..." -ForegroundColor Cyan
$timestamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$spOutput = az ad sp create-for-rbac `
  --name "github-ndt-chatbot-$timestamp" `
  --role contributor `
  --scopes "/subscriptions/$subscriptionId" `
  --sdk-auth

Write-Host ""
Write-Host "✅ Service principal created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "COPY THIS JSON TO GITHUB SECRETS" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host $spOutput -ForegroundColor White
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Copy the JSON above (entire block)" -ForegroundColor White
Write-Host ""
Write-Host "2. Go to your GitHub repository:" -ForegroundColor White
Write-Host "   https://github.com/anthonyricevuto3-lab/Neil-deGrasse-Tyson-Chatbot/settings/secrets/actions" -ForegroundColor Blue
Write-Host ""
Write-Host "3. Click 'New repository secret'" -ForegroundColor White
Write-Host ""
Write-Host "4. Create two secrets:" -ForegroundColor White
Write-Host "   - Name: AZURE_CREDENTIALS" -ForegroundColor Yellow
Write-Host "     Value: [Paste the JSON above]" -ForegroundColor White
Write-Host ""
Write-Host "   - Name: OPENAI_API_KEY" -ForegroundColor Yellow
Write-Host "     Value: [Your OpenAI API key]" -ForegroundColor White
Write-Host ""
Write-Host "5. Go to Actions tab and run 'Deploy to Azure Container Apps'" -ForegroundColor White
Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green

# Copy to clipboard if possible
try {
    $spOutput | Set-Clipboard
    Write-Host ""
    Write-Host "📋 JSON has been copied to your clipboard!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "💡 Tip: Manually select and copy the JSON above" -ForegroundColor Yellow
}
