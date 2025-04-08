set -e

echo "Moving backend files to root for Heroku deployment..."
cp -r backend/* .
touch app/__init__.py

echo "Heroku post-build completed successfully!"
