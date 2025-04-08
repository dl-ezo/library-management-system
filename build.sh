set -e

echo "Building frontend..."
cd frontend
npm install
npm run build

echo "Copying frontend build to backend static directory..."
rm -rf ../backend/static
mkdir -p ../backend/static
cp -r dist/* ../backend/static/

echo "Build completed successfully!"
