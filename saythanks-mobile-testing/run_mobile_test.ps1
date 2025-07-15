# run_mobile_tests.ps1 (simplified)
Write-Host "🚀 Starting SayThanks.io Mobile Testing with Docker..." -ForegroundColor Green

# Clean up any existing containers
Write-Host "Cleaning up existing containers..." -ForegroundColor Yellow
docker-compose down --volumes --remove-orphans

# Build and start all services
Write-Host "Building and starting test environment..." -ForegroundColor Yellow
docker-compose up --build test-runner

# Check if tests completed successfully
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "✅ All tests completed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Some tests failed. Check reports/ for details." -ForegroundColor Red
}

# Show reports location
Write-Host '📊 Test reports generated in: .\reports\' -ForegroundColor Cyan
Write-Host "   - summary_report.html (Main report)" -ForegroundColor White
Write-Host "   - test_summary.json (JSON data)" -ForegroundColor White
Write-Host "   - Individual test suite HTML reports" -ForegroundColor White

# Cleanup
Write-Host "Cleaning up containers..." -ForegroundColor Yellow
docker-compose down

exit $exitCode