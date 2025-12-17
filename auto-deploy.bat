@echo off
echo 🚀 Auto-deploying latest image to AKS...

REM Configuration
set NAMESPACE=inventory-system
set IMAGE_NAME=faizanazam/inventory-management:latest

REM Connect to AKS (assumes you're already logged in)
echo 📡 Connecting to AKS...
az aks get-credentials --resource-group inventory-rg-sea --name inventory-aks

REM Update deployment
echo 🔄 Updating deployment with latest image...
kubectl set image deployment/inventory-app inventory-app=%IMAGE_NAME% -n %NAMESPACE%

REM Wait for rollout
echo ⏳ Waiting for deployment...
kubectl rollout status deployment/inventory-app -n %NAMESPACE% --timeout=300s

REM Verify
echo ✅ Deployment complete!
kubectl get pods -n %NAMESPACE%

REM Test application
echo 🧪 Testing application...
curl -f http://4.144.249.110/health
if %errorlevel% equ 0 (
    echo ✅ Application is healthy!
    echo 🌐 Access at: http://4.144.249.110
) else (
    echo ⚠️ Application may still be starting...
)

echo 🎉 Auto-deployment finished!
pause