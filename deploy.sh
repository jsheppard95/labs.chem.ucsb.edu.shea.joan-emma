#!/bin/bash
set -euo pipefail

# Load credentials
if [[ -f .env ]]; then
    source .env
else
    echo "Error: .env file not found."
    exit 1
fi

# Check required vars
: "${HOST:?Need to set HOST in .env}"
: "${USER:?Need to set USER in .env}"
: "${PASS:?Need to set PASS in .env}"
: "${REMOTE_DIR:?Need to set REMOTE_DIR in .env}"
: "${LOCAL_DIR:?Need to set LOCAL_DIR in .env}"

# Deploy with lftp
lftp -u "$USER","$PASS" sftp://"$HOST" <<EOF
mirror -R --only-newer --parallel=4 --delete --verbose \
  --exclude-glob .git/ \
  --exclude-glob '*.tmp' \
  "$LOCAL_DIR" "$REMOTE_DIR"
bye
EOF
