#!/bin/bash

# Deploy to AKS Script
echo "🚀 Deploying Inventory Management System to AKS..."

# Configuration
RESOURCE_GROUP="inventory-rg-sea"
AKS_CLUSTER="inventory-aks"
NAMESPACE="inventory-system"
IMAGE_NAME="faizanazam/inventory-management:latest"

# Step 1: Connect to AKS
echo "📡 Connecting to AKS cluster..."
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER

# Step 2: Apply secrets and config
echo "🔐 Applying secrets and configuration..."
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/

# Step 3: Update deployment with latest image
echo "🔄 Updating deployment with latest image..."
kubectl set image deployment/inventory-app inventory-app=$IMAGE_NAME -n $NAMESPACE

# Step 4: Wait for rollout to complete
echo "⏳ Waiting for deployment to complete..."
kubectl rollout status deployment/inventory-app -n $NAMESPACE --timeout=300s

# Step 5: Get service information
echo "📊 Getting service information..."
kubectl get pods -n $NAMESPACE
kubectl get services -n $NAMESPACE

# Step 6: Get public IP
echo "🌐 Getting public IP..."
PUBLIC_IP=$(kubectl get service inventory-app-service -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "✅ Application deployed successfully!"
echo "🔗 Access your application at: http://$PUBLIC_IP"

# Step 7: Test health endpoint
echo "🏥 Testing health endpoint..."
if curl -f http://$PUBLIC_IP/health > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed - application may still be starting"
fi

echo "🎉 Deployment complete!"