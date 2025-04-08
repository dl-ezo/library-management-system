set -e

echo "Moving backend files to root for Heroku deployment..."
cp -r backend/* .
touch app/__init__.py

echo "Installing Poetry dependencies..."
pip install poetry
poetry config virtualenvs.create false
poetry install --without dev --no-interaction --no-root

echo "Heroku post-build completed successfully!"
