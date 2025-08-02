# JAEGIS-OS Docker Configuration

**Complete Docker deployment setup for the JAEGIS-OS ecosystem**

This directory contains comprehensive Docker configurations for deploying the entire JAEGIS-OS ecosystem in containerized environments. The setup includes multi-container orchestration, service discovery, load balancing, and production-ready configurations.

## 🐳 Docker Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        NGINX[NGINX<br/>Reverse Proxy<br/>Port 80/443]
    end
    
    subgraph "Web Layer"
        WEBOS[Web OS Desktop<br/>React 18<br/>Port 3000]
    end
    
    subgraph "API Gateway"
        GATEWAY[API Gateway<br/>Service Router<br/>Port 8000]
    end
    
    subgraph "Core Services"
        NLDS[N.L.D.S.<br/>Port 8000]
        SCRIPT[S.C.R.I.P.T.<br/>Port 8080]
        ATLAS[A.T.L.A.S.<br/>Port 8081]
        HELM[H.E.L.M.<br/>Port 8082]
        MASTR[M.A.S.T.R.<br/>Port 8083]
        ASCEND[A.S.C.E.N.D.<br/>Port 8084]
        CORI[C.O.R.I.<br/>Port 8085]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Multi-Database)]
        REDIS[(Redis<br/>Caching)]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus<br/>Metrics]
        GRAF[Grafana<br/>Visualization]
    end
    
    NGINX --> WEBOS
    NGINX --> GATEWAY
    
    GATEWAY --> NLDS
    GATEWAY --> SCRIPT
    GATEWAY --> ATLAS
    GATEWAY --> HELM
    GATEWAY --> MASTR
    GATEWAY --> ASCEND
    GATEWAY --> CORI
    
    NLDS --> PG
    SCRIPT --> PG
    ATLAS --> PG
    HELM --> PG
    MASTR --> PG
    ASCEND --> PG
    CORI --> PG
    
    NLDS --> REDIS
    SCRIPT --> REDIS
    ATLAS --> REDIS
    HELM --> REDIS
    MASTR --> REDIS
    ASCEND --> REDIS
    CORI --> REDIS
    
    HELM --> PROM
    PROM --> GRAF
```

## 📁 Docker Structure

```
docker/
├── README.md                    # This file - Docker documentation
├── Dockerfile                   # Main application Dockerfile
├── docker-compose.yml           # Development environment
├── docker-compose.prod.yml      # Production environment
├── docker-compose.test.yml      # Testing environment
├── nginx/                       # NGINX configuration
│   ├── nginx.conf              # Main NGINX config
│   ├── default.conf            # Default site config
│   ├── ssl.conf                # SSL configuration
│   └── upstream.conf           # Upstream definitions
├── services/                    # Individual service Dockerfiles
│   ├── nlds/                   # N.L.D.S. service
│   ├── script/                 # S.C.R.I.P.T. service
│   ├── atlas/                  # A.T.L.A.S. service
│   ├── helm/                   # H.E.L.M. service
│   ├── mastr/                  # M.A.S.T.R. service
│   ├── ascend/                 # A.S.C.E.N.D. service
│   └── cori/                   # C.O.R.I. service
├── web-os/                      # Web OS Desktop Docker config
│   ├── Dockerfile              # Web OS Dockerfile
│   ├── nginx.conf              # Web OS NGINX config
│   └── entrypoint.sh           # Container entrypoint
├── monitoring/                  # Monitoring stack
│   ├── prometheus/             # Prometheus configuration
│   ├── grafana/                # Grafana configuration
│   └── alertmanager/           # Alert manager setup
├── init-scripts/                # Initialization scripts
│   ├── init-database.sql       # Database initialization
│   ├── init-redis.sh           # Redis initialization
│   └── wait-for-it.sh          # Service dependency waiting
├── healthchecks/                # Health check scripts
│   ├── postgres-healthcheck.sh # PostgreSQL health check
│   ├── redis-healthcheck.sh    # Redis health check
│   └── service-healthcheck.sh  # Service health check
└── .dockerignore                # Docker ignore file
```

## 🚀 Quick Start

### Development Environment
```bash
# Clone repository
git clone https://github.com/usemanusai/JAEGIS-OS.git
cd JAEGIS-OS

# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Access Web OS
open http://localhost:3000
```

### Production Environment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Monitor deployment
docker-compose -f docker-compose.prod.yml ps
```

## 📋 Main Dockerfile

```dockerfile
# Dockerfile - Multi-stage build for JAEGIS-OS
FROM node:18-alpine AS web-builder

# Set working directory
WORKDIR /app

# Copy Web OS source
COPY src/web-os-desktop/package*.json ./
RUN npm ci --only=production

COPY src/web-os-desktop/ ./
RUN npm run build

# Production stage
FROM node:18-alpine AS production

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    postgresql-client \
    redis \
    curl \
    bash

# Create app user
RUN addgroup -g 1001 -S jaegis && \
    adduser -S jaegis -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY requirements.txt ./

# Install dependencies
RUN npm ci --only=production && \
    pip3 install -r requirements.txt

# Copy application source
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Copy built Web OS
COPY --from=web-builder /app/dist ./src/web-os-desktop/dist/

# Copy Docker utilities
COPY docker/init-scripts/ ./init-scripts/
COPY docker/healthchecks/ ./healthchecks/

# Make scripts executable
RUN chmod +x scripts/**/*.sh && \
    chmod +x init-scripts/*.sh && \
    chmod +x healthchecks/*.sh

# Change ownership
RUN chown -R jaegis:jaegis /app

# Switch to app user
USER jaegis

# Expose ports
EXPOSE 3000 8000 8080 8081 8082 8083 8084 8085

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ./healthchecks/service-healthcheck.sh

# Default command
CMD ["npm", "start"]
```

## 🔧 Docker Compose Configuration

### Development Environment
```yaml
# docker-compose.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: jaegis-postgres
    environment:
      POSTGRES_DB: jaegis
      POSTGRES_USER: jaegis
      POSTGRES_PASSWORD: jaegis_password
      POSTGRES_MULTIPLE_DATABASES: nlds,script,atlas,helm,mastr,ascend,cori
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/init-scripts/init-database.sql:/docker-entrypoint-initdb.d/init-database.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jaegis -d jaegis"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - jaegis-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: jaegis-redis
    command: redis-server --appendonly yes --requirepass redis_password
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - jaegis-network

  # N.L.D.S. Service
  nlds:
    build:
      context: .
      dockerfile: docker/services/nlds/Dockerfile
    container_name: jaegis-nlds
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/nlds
      - REDIS_URL=redis://:redis_password@redis:6379/0
      - JWT_SECRET=nlds_jwt_secret
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # S.C.R.I.P.T. Service
  script:
    build:
      context: .
      dockerfile: docker/services/script/Dockerfile
    container_name: jaegis-script
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/script
      - REDIS_URL=redis://:redis_password@redis:6379/1
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # A.T.L.A.S. Service
  atlas:
    build:
      context: .
      dockerfile: docker/services/atlas/Dockerfile
    container_name: jaegis-atlas
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/atlas
      - REDIS_URL=redis://:redis_password@redis:6379/2
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    ports:
      - "8081:8081"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # H.E.L.M. Service
  helm:
    build:
      context: .
      dockerfile: docker/services/helm/Dockerfile
    container_name: jaegis-helm
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/helm
      - REDIS_URL=redis://:redis_password@redis:6379/3
    ports:
      - "8082:8082"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8082/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # M.A.S.T.R. Service
  mastr:
    build:
      context: .
      dockerfile: docker/services/mastr/Dockerfile
    container_name: jaegis-mastr
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/mastr
      - REDIS_URL=redis://:redis_password@redis:6379/4
    ports:
      - "8083:8083"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8083/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # A.S.C.E.N.D. Service
  ascend:
    build:
      context: .
      dockerfile: docker/services/ascend/Dockerfile
    container_name: jaegis-ascend
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/ascend
      - REDIS_URL=redis://:redis_password@redis:6379/5
    ports:
      - "8084:8084"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8084/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # C.O.R.I. Service
  cori:
    build:
      context: .
      dockerfile: docker/services/cori/Dockerfile
    container_name: jaegis-cori
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://jaegis:jaegis_password@postgres:5432/cori
      - REDIS_URL=redis://:redis_password@redis:6379/6
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    ports:
      - "8085:8085"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8085/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # Web OS Desktop
  web-os:
    build:
      context: .
      dockerfile: docker/web-os/Dockerfile
    container_name: jaegis-web-os
    environment:
      - NODE_ENV=development
      - REACT_APP_API_BASE_URL=http://localhost:8000
      - REACT_APP_NLDS_URL=http://nlds:8000
      - REACT_APP_SCRIPT_URL=http://script:8080
      - REACT_APP_ATLAS_URL=http://atlas:8081
      - REACT_APP_HELM_URL=http://helm:8082
      - REACT_APP_MASTR_URL=http://mastr:8083
      - REACT_APP_ASCEND_URL=http://ascend:8084
      - REACT_APP_CORI_URL=http://cori:8085
    ports:
      - "3000:3000"
    depends_on:
      - nlds
      - script
      - atlas
      - helm
      - mastr
      - ascend
      - cori
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

  # NGINX Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: jaegis-nginx
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web-os
      - nlds
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  jaegis-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Production Environment
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Production PostgreSQL with replication
  postgres-primary:
    image: postgres:15-alpine
    container_name: jaegis-postgres-primary
    environment:
      POSTGRES_DB: jaegis
      POSTGRES_USER: jaegis
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_REPLICATION_USER: replicator
      POSTGRES_REPLICATION_PASSWORD: ${POSTGRES_REPLICATION_PASSWORD}
    volumes:
      - postgres_primary_data:/var/lib/postgresql/data
      - ./docker/init-scripts/init-database.sql:/docker-entrypoint-initdb.d/init-database.sql
      - ./docker/postgres/postgresql.conf:/etc/postgresql/postgresql.conf
      - ./docker/postgres/pg_hba.conf:/etc/postgresql/pg_hba.conf
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jaegis -d jaegis"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - jaegis-network
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'

  # Redis Cluster
  redis-master:
    image: redis:7-alpine
    container_name: jaegis-redis-master
    command: redis-server /etc/redis/redis.conf
    volumes:
      - redis_master_data:/data
      - ./docker/redis/redis-master.conf:/etc/redis/redis.conf
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - jaegis-network
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'

  # Production services with resource limits
  nlds:
    build:
      context: .
      dockerfile: docker/services/nlds/Dockerfile
      target: production
    container_name: jaegis-nlds-prod
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://jaegis:${POSTGRES_PASSWORD}@postgres-primary:5432/nlds
      - REDIS_URL=redis://redis-master:6379/0
      - JWT_SECRET=${JWT_SECRET}
      - REFRESH_SECRET=${REFRESH_SECRET}
    depends_on:
      postgres-primary:
        condition: service_healthy
      redis-master:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

  # Load balancer with SSL
  nginx:
    image: nginx:alpine
    container_name: jaegis-nginx-prod
    volumes:
      - ./docker/nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/ssl.conf:/etc/nginx/conf.d/ssl.conf
      - ./ssl/certs:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - nlds
      - web-os
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - jaegis-network
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.25'

  # Monitoring stack
  prometheus:
    image: prom/prometheus:latest
    container_name: jaegis-prometheus
    volumes:
      - ./docker/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - jaegis-network

  grafana:
    image: grafana/grafana:latest
    container_name: jaegis-grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./docker/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./docker/monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    networks:
      - jaegis-network

volumes:
  postgres_primary_data:
    driver: local
  redis_master_data:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local

networks:
  jaegis-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/16

# Production deployment configuration
deploy:
  replicas: 2
  update_config:
    parallelism: 1
    delay: 10s
    failure_action: rollback
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
```

## 🔧 NGINX Configuration

### Main NGINX Configuration
```nginx
# docker/nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;

    # Upstream definitions
    upstream web_os {
        least_conn;
        server web-os:3000 max_fails=3 fail_timeout=30s;
    }

    upstream api_gateway {
        least_conn;
        server nlds:8000 max_fails=3 fail_timeout=30s;
    }

    upstream services {
        least_conn;
        server script:8080 max_fails=3 fail_timeout=30s;
        server atlas:8081 max_fails=3 fail_timeout=30s;
        server helm:8082 max_fails=3 fail_timeout=30s;
        server mastr:8083 max_fails=3 fail_timeout=30s;
        server ascend:8084 max_fails=3 fail_timeout=30s;
        server cori:8085 max_fails=3 fail_timeout=30s;
    }

    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
}
```

### Default Site Configuration
```nginx
# docker/nginx/default.conf
server {
    listen 80;
    server_name localhost;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Web OS Desktop
    location / {
        proxy_pass http://web_os;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    # API Gateway
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://api_gateway;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # CORS headers
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
        add_header Access-Control-Expose-Headers "Content-Length,Content-Range" always;
        
        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Origin "*";
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain; charset=utf-8';
            add_header Content-Length 0;
            return 204;
        }
    }

    # Authentication endpoints with stricter rate limiting
    location /api/auth/ {
        limit_req zone=login burst=5 nodelay;
        
        proxy_pass http://api_gateway;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://api_gateway;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Static assets with caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://web_os;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }

    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

## 🔍 Health Checks

### Service Health Check Script
```bash
#!/bin/bash
# docker/healthchecks/service-healthcheck.sh

set -e

# Configuration
SERVICES=(
    "nlds:8000"
    "script:8080"
    "atlas:8081"
    "helm:8082"
    "mastr:8083"
    "ascend:8084"
    "cori:8085"
)

TIMEOUT=10
RETRIES=3

# Check individual service
check_service() {
    local service_name=$1
    local service_port=$2
    local url="http://localhost:$service_port/health"
    
    for i in $(seq 1 $RETRIES); do
        if curl -f -s --max-time $TIMEOUT "$url" > /dev/null 2>&1; then
            echo "✅ $service_name - Healthy"
            return 0
        fi
        
        if [ $i -lt $RETRIES ]; then
            echo "⚠️  $service_name - Retry $i/$RETRIES"
            sleep 2
        fi
    done
    
    echo "❌ $service_name - Unhealthy"
    return 1
}

# Main health check
main() {
    echo "🏥 JAEGIS-OS Health Check"
    echo "========================"
    
    failed_checks=0
    
    for service_info in "${SERVICES[@]}"; do
        IFS=':' read -r service_name service_port <<< "$service_info"
        if ! check_service "$service_name" "$service_port"; then
            ((failed_checks++))
        fi
    done
    
    if [ $failed_checks -eq 0 ]; then
        echo "🎉 All services healthy!"
        exit 0
    else
        echo "⚠️  $failed_checks service(s) unhealthy"
        exit 1
    fi
}

main "$@"
```

## 📊 Monitoring Configuration

### Prometheus Configuration
```yaml
# docker/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  # JAEGIS Services
  - job_name: 'jaegis-services'
    static_configs:
      - targets:
        - 'nlds:8000'
        - 'script:8080'
        - 'atlas:8081'
        - 'helm:8082'
        - 'mastr:8083'
        - 'ascend:8084'
        - 'cori:8085'
    metrics_path: '/metrics'
    scrape_interval: 30s

  # Web OS Desktop
  - job_name: 'web-os'
    static_configs:
      - targets: ['web-os:3000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  # Infrastructure
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    metrics_path: '/metrics'
    scrape_interval: 30s

  # NGINX
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
    metrics_path: '/metrics'
    scrape_interval: 30s

  # Node Exporter
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
    scrape_interval: 30s
```

## 🚀 Deployment Commands

### Development Deployment
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale nlds=2 --scale cori=2

# Stop environment
docker-compose down

# Clean up
docker-compose down -v --remove-orphans
```

### Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Update services
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Monitor deployment
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f

# Backup data
docker-compose -f docker-compose.prod.yml exec postgres-primary pg_dump -U jaegis jaegis > backup.sql

# Restore data
docker-compose -f docker-compose.prod.yml exec -T postgres-primary psql -U jaegis jaegis < backup.sql
```

### Testing Environment
```bash
# Run tests in containers
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Run specific test suite
docker-compose -f docker-compose.test.yml run --rm test-runner npm run test:integration

# Clean up test environment
docker-compose -f docker-compose.test.yml down -v
```

## 🔧 Environment Variables

### Required Environment Variables
```bash
# Database
POSTGRES_PASSWORD=secure_postgres_password
POSTGRES_REPLICATION_PASSWORD=secure_replication_password

# Authentication
JWT_SECRET=your_jwt_secret_key_here
REFRESH_SECRET=your_refresh_token_secret_here

# External Services
GITHUB_TOKEN=your_github_token
OPENROUTER_API_KEY=your_openrouter_api_key

# Monitoring
GRAFANA_PASSWORD=secure_grafana_password

# SSL (for production)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### Environment File Example
```bash
# .env.docker
NODE_ENV=production
JAEGIS_DEBUG=false
JAEGIS_LOG_LEVEL=info

# Database Configuration
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://jaegis:your_secure_password@postgres:5432/jaegis

# Redis Configuration
REDIS_PASSWORD=your_redis_password
REDIS_URL=redis://:your_redis_password@redis:6379

# Security
JWT_SECRET=your_jwt_secret_key_minimum_32_characters
REFRESH_SECRET=your_refresh_secret_key_minimum_32_characters

# External APIs
GITHUB_TOKEN=ghp_your_github_personal_access_token
OPENROUTER_API_KEY=sk-or-your_openrouter_api_key

# Monitoring
GRAFANA_PASSWORD=your_grafana_admin_password
PROMETHEUS_RETENTION=30d

# SSL Configuration (Production)
SSL_CERT_PATH=/etc/nginx/ssl/fullchain.pem
SSL_KEY_PATH=/etc/nginx/ssl/privkey.pem
DOMAIN_NAME=jaegis.yourdomain.com
```

## 🔒 Security Configuration

### Docker Security Best Practices
```dockerfile
# Security-focused Dockerfile example
FROM node:18-alpine AS base

# Create non-root user
RUN addgroup -g 1001 -S jaegis && \
    adduser -S jaegis -u 1001

# Install security updates
RUN apk update && apk upgrade && \
    apk add --no-cache dumb-init

# Set working directory
WORKDIR /app

# Copy and install dependencies as root
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Copy application code
COPY --chown=jaegis:jaegis . .

# Switch to non-root user
USER jaegis

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["npm", "start"]
```

## 📚 Troubleshooting

### Common Issues

1. **Services not starting**
   ```bash
   # Check service logs
   docker-compose logs service-name
   
   # Check resource usage
   docker stats
   
   # Restart specific service
   docker-compose restart service-name
   ```

2. **Database connection issues**
   ```bash
   # Check database health
   docker-compose exec postgres pg_isready -U jaegis
   
   # Connect to database
   docker-compose exec postgres psql -U jaegis -d jaegis
   ```

3. **Network connectivity issues**
   ```bash
   # Check network
   docker network ls
   docker network inspect jaegis-os_jaegis-network
   
   # Test connectivity
   docker-compose exec nlds ping postgres
   ```

## 📄 License

This Docker configuration is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**JAEGIS-OS Docker** - Containerized deployment for the AI-powered operating system.