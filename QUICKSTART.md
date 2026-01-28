# Solar Sync - Quick Start Guide

## 🚀 Deploy on Minikube (5 minutes)

### Step 1: Start Minikube
```bash
minikube start --cpus=4 --memory=8192
minikube addons enable ingress
```

### Step 2: Build & Load Image
```bash
docker build -t solar-sync:latest .
minikube image load solar-sync:latest
```

### Step 3: Deploy
```bash
kubectl apply -f k8s/
```

### Step 4: Verify
```bash
kubectl get pods -l app=solar-sync
kubectl get svc
```

### Step 5: Access
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Update /etc/hosts
sudo bash -c "echo '$MINIKUBE_IP solar-sync.local' >> /etc/hosts"

# Test
curl http://solar-sync.local
```

---

## 🐳 Local Testing (Before Kubernetes)

```bash
# Terminal 1: Start mock server
export API_URL="http://localhost:8000/api/solar"
python3 << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(f"✓ Received: {self.rfile.read(int(self.headers['Content-Length']))}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"ok":true}')
    def log_message(self, *args): pass

HTTPServer(('localhost', 8000), Handler).serve_forever()
EOF

# Terminal 2: Run app
export API_URL="http://localhost:8000/api/solar"
python3 sync.py
```

Expected output:
```
Sync successful
```

---

## 🔍 Troubleshooting

### Pods not starting?
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Connection refused?
```bash
# Check service
kubectl get svc solar-sync-service

# Verify DNS
kubectl exec -it <pod-name> -- nslookup central-server
```

### Image pull failed?
```bash
# For Minikube
minikube image load solar-sync:latest

# For remote registry
docker push docker.io/yourusername/solar-sync:latest
```

---

## 📊 Monitoring

```bash
# Watch pods
kubectl get pods -l app=solar-sync -w

# View logs
kubectl logs -l app=solar-sync -f

# Get metrics
kubectl top pods -l app=solar-sync
```

---

## 🔐 Production Checklist

- [ ] Update API_URL in ConfigMap (k8s/deployment.yaml)
- [ ] Set Docker registry credentials in GitHub Actions
- [ ] Configure TLS certificates for ingress
- [ ] Set up kubeconfig secret in GitHub
- [ ] Enable monitoring/metrics collection
- [ ] Configure backup strategy
- [ ] Document recovery procedures

---

## 📈 Scaling

```bash
# Manual
kubectl scale deployment solar-sync --replicas=5

# Auto-scale
kubectl autoscale deployment solar-sync --min=2 --max=10 --cpu-percent=70
```

---

## 🛑 Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Stop Minikube
minikube stop
```

---

## 💡 For Cameroon Labs

### Bandwidth-optimized setup:
1. Use K3s instead of Minikube
2. Create local Docker registry (reduce image downloads)
3. Use Alpine images (89% smaller)
4. Implement local caching

### Network-resilient setup:
1. Already has 5-retry mechanism
2. Increase timeout if needed (sync.py line 13)
3. Add circuit breaker for failing endpoints
4. Consider request batching

### Minimal hardware:
```
CPU: 2 cores
RAM: 4GB
Disk: 20GB
```

---

## 📞 Support

For issues, check:
1. [DEVOPS_REPORT.md](DEVOPS_REPORT.md) - Comprehensive documentation
2. `kubectl describe pod <pod-name>` - Detailed pod info
3. `kubectl logs <pod-name>` - Application logs
4. `kubectl get events` - Kubernetes events

---

**Last Updated:** January 28, 2026
