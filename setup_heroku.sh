

echo "Setting up Heroku deployment for Company Library Management System"

if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI not found. Please install it first."
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "Logging in to Heroku..."
if [ -z "$HEROKU_API_KEY" ]; then
    echo "HEROKU_API_KEY environment variable not set."
    echo "Please set it with: export HEROKU_API_KEY=your_api_key"
    exit 1
fi

echo "Creating Heroku app under team dartslive..."
heroku create lib-mgmt-dl-ezo --team dartslive || echo "App may already exist, continuing..."

echo "Adding PostgreSQL addon..."
heroku addons:create heroku-postgresql:essential-0 -a lib-mgmt-dl-ezo || echo "PostgreSQL addon may already exist, continuing..."

echo "Setting environment variables..."
heroku config:set PYTHON_VERSION=3.10.0 -a lib-mgmt-dl-ezo

echo "Heroku setup completed successfully!"
echo "To deploy, run: git push heroku main"
echo "Or use the GitHub Actions workflow for automatic deployment."
