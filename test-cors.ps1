# Test CORS headers after deployment
$fqdn = az containerapp show --name ndt-backend --resource-group Neil-deGrasse-Tyson-Chatbot-RG --query properties.configuration.ingress.fqdn -o tsv

Write-Host "`n=== Testing CORS Headers ===" -ForegroundColor Cyan
Write-Host "Backend URL: https://$fqdn`n" -ForegroundColor Yellow

# Test 1: Health endpoint with Origin
Write-Host "Test 1: GET /api/healthz with Origin header" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "https://$fqdn/api/healthz" -Headers @{ Origin = "https://neil-degrasse-tyson-ai-chatbot.com" } -UseBasicParsing
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor White
    Write-Host "Access-Control-Allow-Origin: $($response.Headers['Access-Control-Allow-Origin'])" -ForegroundColor $(if ($response.Headers['Access-Control-Allow-Origin']) { 'Green' } else { 'Red' })
    Write-Host "Access-Control-Allow-Credentials: $($response.Headers['Access-Control-Allow-Credentials'])" -ForegroundColor White
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 2: Preflight OPTIONS for /api/chat
Write-Host "`nTest 2: OPTIONS /api/chat (preflight)" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "https://$fqdn/api/chat" -Method Options -Headers @{
        Origin = "https://neil-degrasse-tyson-ai-chatbot.com"
        "Access-Control-Request-Method" = "POST"
        "Access-Control-Request-Headers" = "content-type"
    } -UseBasicParsing
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor White
    Write-Host "Access-Control-Allow-Origin: $($response.Headers['Access-Control-Allow-Origin'])" -ForegroundColor $(if ($response.Headers['Access-Control-Allow-Origin']) { 'Green' } else { 'Red' })
    Write-Host "Access-Control-Allow-Methods: $($response.Headers['Access-Control-Allow-Methods'])" -ForegroundColor White
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 3: GET /api/sources with Origin
Write-Host "`nTest 3: GET /api/sources with Origin header" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "https://$fqdn/api/sources?indexed_only=1" -Headers @{ Origin = "https://neil-degrasse-tyson-ai-chatbot.com" } -UseBasicParsing
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor White
    Write-Host "Access-Control-Allow-Origin: $($response.Headers['Access-Control-Allow-Origin'])" -ForegroundColor $(if ($response.Headers['Access-Control-Allow-Origin']) { 'Green' } else { 'Red' })
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Sources count: $($data.Count)" -ForegroundColor White
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

# Test 4: Debug endpoint
Write-Host "`nTest 4: GET /api/debug/cors" -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "https://$fqdn/api/debug/cors"
    Write-Host "CORS Origins (parsed):" -ForegroundColor White
    $response.cors_origins | ForEach-Object { Write-Host "  - $_" -ForegroundColor Cyan }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host "`n=== Tests Complete ===" -ForegroundColor Cyan
