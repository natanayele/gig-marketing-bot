#!/bin/bash

# === USAGE ===
# Save this as `setup_webhook.sh`, make it executable: chmod +x setup_webhook.sh
# Then run: ./setup_webhook.sh <your-heroku-app-name>

APP_NAME=$1
if [ -z "$APP_NAME" ]; then
  echo "❌ Please provide your Heroku app name."
  echo "Usage: ./setup_webhook.sh your-heroku-app-name"
  exit 1
fi

# Construct the expected Heroku URL
HEROKU_URL="https://$APP_NAME.herokuapp.com"

# Set the HEROKU_URL config var in Heroku
heroku config:set HEROKU_URL=$HEROKU_URL --app $APP_NAME

if [ $? -eq 0 ]; then
  echo "✅ HEROKU_URL has been set to $HEROKU_URL for $APP_NAME"
else
  echo "❌ Failed to set HEROKU_URL. Please check your Heroku CLI authentication."
  exit 1
fi
