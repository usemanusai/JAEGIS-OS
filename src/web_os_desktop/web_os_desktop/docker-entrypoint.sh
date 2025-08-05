#!/bin/sh
# Docker entrypoint script for JAEGIS Web OS

set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting JAEGIS Web OS container..."

# Environment variables with defaults
export REACT_APP_API_BASE_URL=${REACT_APP_API_BASE_URL:-"http://localhost:8000"}
export REACT_APP_SCRIPT_URL=${REACT_APP_SCRIPT_URL:-"http://localhost:8080"}
export REACT_APP_ATLAS_URL=${REACT_APP_ATLAS_URL:-"http://localhost:8081"}
export REACT_APP_HELM_URL=${REACT_APP_HELM_URL:-"http://localhost:8082"}
export REACT_APP_MASTR_URL=${REACT_APP_MASTR_URL:-"http://localhost:8083"}
export REACT_APP_ASCEND_URL=${REACT_APP_ASCEND_URL:-"http://localhost:8084"}
export REACT_APP_CORI_URL=${REACT_APP_CORI_URL:-"http://localhost:8085"}
export REACT_APP_COCKPIT_URL=${REACT_APP_COCKPIT_URL:-"http://localhost:8090"}

log "Environment configuration:"
log "  API Base URL: $REACT_APP_API_BASE_URL"
log "  S.C.R.I.P.T. URL: $REACT_APP_SCRIPT_URL"
log "  A.T.L.A.S. URL: $REACT_APP_ATLAS_URL"
log "  H.E.L.M. URL: $REACT_APP_HELM_URL"
log "  M.A.S.T.R. URL: $REACT_APP_MASTR_URL"
log "  A.S.C.E.N.D. URL: $REACT_APP_ASCEND_URL"
log "  C.O.R.I. URL: $REACT_APP_CORI_URL"
log "  Cockpit URL: $REACT_APP_COCKPIT_URL"

# Create runtime configuration file
cat > /usr/share/nginx/html/config.js << EOF
window.JAEGIS_CONFIG = {
  API_BASE_URL: '$REACT_APP_API_BASE_URL',
  SERVICES: {
    SCRIPT: '$REACT_APP_SCRIPT_URL',
    ATLAS: '$REACT_APP_ATLAS_URL',
    HELM: '$REACT_APP_HELM_URL',
    MASTR: '$REACT_APP_MASTR_URL',
    ASCEND: '$REACT_APP_ASCEND_URL',
    CORI: '$REACT_APP_CORI_URL',
    NLDS: '$REACT_APP_API_BASE_URL',
    COCKPIT: '$REACT_APP_COCKPIT_URL'
  },
  VERSION: '1.0.0',
  BUILD_TIME: '$(date -u +"%Y-%m-%dT%H:%M:%SZ")',
  ENVIRONMENT: '${NODE_ENV:-production}'
};
EOF

log "Runtime configuration created"

# Wait for core services to be available (optional health check)
if [ "${WAIT_FOR_SERVICES:-false}" = "true" ]; then
    log "Waiting for core services to be available..."
    
    services="$REACT_APP_API_BASE_URL $REACT_APP_SCRIPT_URL $REACT_APP_ATLAS_URL $REACT_APP_HELM_URL $REACT_APP_MASTR_URL $REACT_APP_ASCEND_URL $REACT_APP_CORI_URL $REACT_APP_COCKPIT_URL"
    
    for service in $services; do
        log "Checking $service..."
        timeout=30
        while [ $timeout -gt 0 ]; do
            if wget --quiet --tries=1 --timeout=3 --spider "$service/health" 2>/dev/null; then
                log "  ✅ $service is available"
                break
            else
                log "  ⏳ Waiting for $service... ($timeout seconds remaining)"
                sleep 2
                timeout=$((timeout - 2))
            fi
        done
        
        if [ $timeout -le 0 ]; then
            log "  ⚠️  Warning: $service is not responding, continuing anyway..."
        fi
    done
fi

# Validate nginx configuration
log "Validating nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    log "✅ Nginx configuration is valid"
else
    log "❌ Nginx configuration is invalid"
    exit 1
fi

# Create necessary directories
mkdir -p /var/log/nginx
mkdir -p /var/cache/nginx

# Set proper permissions
chown -R nginx:nginx /var/log/nginx
chown -R nginx:nginx /var/cache/nginx
chown -R nginx:nginx /usr/share/nginx/html

log "✅ JAEGIS Web OS is ready to start"

# Execute the main command
exec "$@"
