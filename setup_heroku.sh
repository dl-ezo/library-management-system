
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

echo "Creating backend Heroku app under team dartslive..."
heroku create lib-mgmt-dl-ezo --team dartslive || echo "Backend app may already exist, continuing..."

echo "Adding PostgreSQL addon..."
heroku addons:create heroku-postgresql:essential-0 -a lib-mgmt-dl-ezo || echo "PostgreSQL addon may already exist, continuing..."

echo "Setting backend environment variables..."
heroku config:set PYTHON_VERSION=3.10.0 -a lib-mgmt-dl-ezo

echo "Creating frontend Heroku app under team dartslive..."
heroku create lib-mgmt-dl-ezo-frontend --team dartslive || echo "Frontend app may already exist, continuing..."

echo "Setting frontend environment variables..."
heroku config:set VITE_API_URL=https://lib-mgmt-dl-ezo.herokuapp.com -a lib-mgmt-dl-ezo-frontend

echo "Heroku setup completed successfully!"
echo ""
echo "To deploy backend:"
echo "1. cd backend"
echo "2. git init"
echo "3. heroku git:remote -a lib-mgmt-dl-ezo"
echo "4. git add ."
echo "5. git commit -m 'Deploy backend to Heroku'"
echo "6. git push heroku main"
echo ""
echo "To deploy frontend:"
echo "1. cd frontend"
echo "2. npm run build"
echo "3. cd .."
echo "4. heroku buildpacks:set heroku/nodejs -a lib-mgmt-dl-ezo-frontend"
echo "5. git subtree push --prefix frontend heroku main"
echo ""
echo "Or use the GitHub Actions workflow for automatic deployment."
