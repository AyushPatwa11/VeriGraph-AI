# VeriGraph Backend - Deployment Guide

## Production Deployment Options

### Option 1: Linux Server with Gunicorn + Nginx

#### Step 1: Server Setup

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    nginx \
    supervisor \
    git

# Create application user
sudo useradd -m -s /bin/bash verigraph

# Create application directory
sudo mkdir -p /home/verigraph/app
sudo chown -R verigraph:verigraph /home/verigraph/app
```

#### Step 2: Application Setup

```bash
# Switch to application user
sudo su - verigraph

# Clone repository
git clone <repo-url> /home/verigraph/app
cd /home/verigraph/app/backend

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn redis

# Set environment variables
cat > .env << EOF
FLASK_ENV=production
DEVICE=cuda  # or cpu
CACHE_TYPE=redis
REDIS_HOST=localhost
REDIS_PORT=6379
LOG_LEVEL=INFO
EOF
```

#### Step 3: Gunicorn Configuration

```bash
# Create supervisor config
sudo tee /etc/supervisor/conf.d/verigraph.conf << EOF
[program:verigraph]
user=verigraph
directory=/home/verigraph/app/backend
environment=PATH=/home/verigraph/app/backend/venv/bin
command=/home/verigraph/app/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 --timeout 120 wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/verigraph.err.log
stdout_logfile=/var/log/verigraph.out.log

[program:verigraph-worker]
user=verigraph
directory=/home/verigraph/app/backend
environment=PATH=/home/verigraph/app/backend/venv/bin
command=/home/verigraph/app/backend/venv/bin/celery -A app.celery worker --loglevel=info
autostart=true
autorestart=true
stderr_logfile=/var/log/verigraph-worker.err.log
stdout_logfile=/var/log/verigraph-worker.out.log
EOF

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start verigraph
```

#### Step 4: Nginx Configuration

```bash
# Create Nginx config
sudo tee /etc/nginx/sites-available/verigraph << 'EOF'
upstream verigraph_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";

    # Logging
    access_log /var/log/nginx/verigraph_access.log;
    error_log /var/log/nginx/verigraph_error.log;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # Proxy settings
    location / {
        proxy_pass http://verigraph_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/verigraph /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --ngx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Option 2: Docker Swarm Deployment

#### Step 1: Initialize Swarm

```bash
# On manager node
docker swarm init

# Get join token for workers
docker swarm join-token worker
```

#### Step 2: Create Stack File

```bash
cat > /home/verigraph/stack.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: verigraph-backend:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DEVICE=cuda
      - CACHE_TYPE=redis
      - REDIS_HOST=redis
    networks:
      - verigraph-net

  redis:
    image: redis:7-alpine
    deploy:
      placement:
        constraints: [node.role == manager]
    volumes:
      - redis-data:/data
    networks:
      - verigraph-net
    command: redis-server --appendonly yes

  nginx:
    image: nginx:latest
    deploy:
      replicas: 2
      ports:
        - target: 80
          published: 80
          mode: host
        - target: 443
          published: 443
          mode: host
    volumes:
      - /etc/nginx/conf.d:/etc/nginx/conf.d:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    networks:
      - verigraph-net

volumes:
  redis-data:

networks:
  verigraph-net:
    driver: overlay
EOF

# Deploy stack
docker stack deploy -c /home/verigraph/stack.yml verigraph
```

### Option 3: Kubernetes Deployment

#### Step 1: Create Namespace and Secrets

```bash
kubectl create namespace verigraph

# Create secrets
kubectl create secret generic verigraph-config \
  --from-literal=FLASK_ENV=production \
  --from-literal=DEVICE=cuda \
  -n verigraph
```

#### Step 2: Create Deployment

```bash
cat > verigraph-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: verigraph-backend
  namespace: verigraph

spec:
  replicas: 3
  selector:
    matchLabels:
      app: verigraph-backend

  template:
    metadata:
      labels:
        app: verigraph-backend

    spec:
      containers:
      - name: backend
        image: verigraph-backend:latest
        imagePullPolicy: Always

        ports:
        - containerPort: 5000
          name: http

        env:
        - name: FLASK_ENV
          value: production
        - name: DEVICE
          value: cuda
        - name: CACHE_TYPE
          value: redis
        - name: REDIS_HOST
          value: verigraph-redis

        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
            nvidia.com/gpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
            nvidia.com/gpu: "1"

        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5

      imagePullSecrets:
      - name: docker-secret
EOF

kubectl apply -f verigraph-deployment.yaml
```

#### Step 3: Create Service

```bash
cat > verigraph-service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: verigraph-service
  namespace: verigraph

spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
    protocol: TCP
  selector:
    app: verigraph-backend
EOF

kubectl apply -f verigraph-service.yaml
```

#### Step 4: Create Ingress

```bash
cat > verigraph-ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: verigraph-ingress
  namespace: verigraph
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod

spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - your-domain.com
    secretName: verigraph-tls

  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: verigraph-service
            port:
              number: 80
EOF

kubectl apply -f verigraph-ingress.yaml
```

## Monitoring & Logging

### Application Monitoring

```bash
# Check application status
curl https://your-domain.com/health

# View metrics
curl https://your-domain.com/api/metrics

# Check logs
sudo tail -f /var/log/verigraph.out.log
```

### System Monitoring Setup

```bash
# Install Prometheus
docker pull prom/prometheus:latest

# Install Grafana
docker pull grafana/grafana:latest

# Configure scrape targets for verigraph metrics
```

### Logging Stack

```bash
# ELK Stack (Elasticsearch, Logstash, Kibana)
docker-compose -f docker-compose.logging.yml up

# or use centralized logging service
# - CloudWatch (AWS)
# - Stackdriver (Google Cloud)
# - Splunk
```

## Performance Optimization

### Database Optimization

```bash
# PostgreSQL (if using)
sudo -u postgres psql << EOF
CREATE INDEX idx_verification_query ON verifications(query);
CREATE INDEX idx_verification_timestamp ON verifications(timestamp);
EOF
```

### Cache Optimization

```bash
# Redis optimization in production
Redis memory policy: allkeys-lru
Maxmemory: 2gb
```

### Model Optimization

```bash
# Use quantized models for reduced memory
export QUANTIZE_MODELS=true

# Use distilled models for faster inference
export VERIFICATION_MODEL=cross-encoder/qnli-distilroberta-base
```

## Scaling Strategies

### Horizontal Scaling

1. **Load Balancing**: Use Nginx or cloud load balancer
2. **Database Sharding**: Shard by query hash
3. **Cache Distribution**: Use Redis Cluster
4. **Model Caching**: Distribute model cache across nodes

### Vertical Scaling

1. **Increase GPU count**
2. **Increase RAM**
3. **Use multi-GPU inference**
4. **Optimize batch size**

## Security Hardening

### API Security

```bash
# Rate limiting
pip install Flask-Limiter

# CORS configuration
CORS_ORIGINS=["https://yourdomain.com"]

# API authentication
pip install Flask-JWT-Extended
```

### Infrastructure Security

```bash
# Firewall rules
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# SSH hardening
- Disable root login
- Configure SSH keys only
- Change default SSH port
```

## Backup & Recovery

```bash
# Database backup
pg_dump verigraph > verigraph_backup.sql

# Redis persistence
# Enabled in docker-compose

# Automated backups
0 2 * * * /home/verigraph/backup.sh
```

## Troubleshooting

### High Latency

```bash
# Check inference time
curl https://your-domain.com/api/metrics | grep inference_ms

# Increase workers
gunicorn --workers 8

# Use GPU
export DEVICE=cuda
```

### Out of Memory

```bash
# Check memory
free -h

# Reduce batch size
export BATCH_SIZE=8

# Enable memory optimization
export QUANTIZE_MODELS=true
```

### Database Issues

```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Check Redis
redis-cli ping

# Restart services
docker-compose restart postgres redis
```

## Deployment Checklist

- [ ] Server security hardened
- [ ] SSL certificates installed
- [ ] Application configured for production
- [ ] Database backup configured
- [ ] Monitoring and alerts set up
- [ ] Auto-scaling configured
- [ ] Load balancing configured
- [ ] Logging aggregation configured
- [ ] Database replicated (if needed)
- [ ] Disaster recovery plan ready

---

**For additional support, check the README.md and documentation**
