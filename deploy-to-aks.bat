@echo off
REM Deploy to AKS Script for Windows
echo 🚀 Deploying Inventory Management System to AKS...

REM Configuration
set RESOURCE_GROUP=inventory-rg-sea
set AKS_CLUSTER=inventory-aks
set NAMESPACE=inventory-system
set IMAGE_NAME=faizanazam/inventory-management:latest

REM Step 1: Connect to AKS
echo 📡 Connecting to AKS cluster...
az aks get-credentials --resource-group %RESOURCE_GROUP% --name %AKS_CLUSTER%

REM Step 2: Apply secrets and config
echo 🔐 Applying secrets and configuration...
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/

REM Step 3: Update deployment with latest image
echo 🔄 Updating deployment with latest image...
kubectl set image deployment/inventory-app inventory-app=%IMAGE_NAME% -n %NAMESPACE%

REM Step 4: Wait for rollout to complete
echo ⏳ Waiting for deployment to complete...
kubectl rollout status deployment/inventory-app -n %NAMESPACE% --timeout=300s

REM Step 5: Get service information
echo 📊 Getting service information...
kubectl get pods -n %NAMESPACE%
kubectl get services -n %NAMESPACE%

REM Step 6: Get public IP
echo 🌐 Getting public IP...
for /f "tokens=*" %%i in ('kubectl get service inventory-app-service -n %NAMESPACE% -o jsonpath="{.status.loadBalancer.ingress[0].ip}"') do set PUBLIC_IP=%%i
echo ✅ Application deployed successfully!
echo 🔗 Access your application at: http://%PUBLIC_IP%

REM Step 7: Test health endpoint
echo 🏥 Testing health endpoint...
curl -f http://%PUBLIC_IP%/health
if %errorlevel% equ 0 (
    echo ✅ Health check passed!
) else (
    echo ⚠️  Health check failed - application may still be starting
)

echo 🎉 Deployment complete!
pause