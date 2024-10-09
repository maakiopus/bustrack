#!/bin/bash

# SSH connection details
SERVER_USER="dmons"
SERVER_ADM="maaki"
SERVER_IP="geebo"
APP_DIR="/app/webdash"

# Local paths
LOCAL_APP_DIR="."

# Deploy application
echo "Deploying application..."
rsync -avz --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.venv' \
    $LOCAL_APP_DIR/* $SERVER_USER@$SERVER_IP:$APP_DIR/

# SSH and update packages 
ssh $SERVER_USER@$SERVER_IP << 'EOF'
    cd $APP_DIR
    source .venv/bin/activate
    poetry install
    echo "Done Updating"
EOF

# Restart
ssh $SERVER_ADM@$SERVER_IP << 'EOF'
    sudo supervisorctl restart bus30tracker
    echo "Done Deploying"
EOF
