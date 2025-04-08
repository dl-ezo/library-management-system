set -e

echo "Building frontend..."
cd frontend
npm install
npm run build

echo "Copying frontend build to static directory..."
rm -rf ../static
mkdir -p ../static
cp -r dist/* ../static/

echo "Build completed successfully!"
