VERSION=0.1.3

# 1. Build package

rm -rf build
python setup.py build_plugin

# 2. Clean files

cd build
find . -name *.pyc -exec rm -rf {} \;
find . -name *.map -exec rm -rf {} \;
find . -name .DS_Store -exec rm -rf {} \;

# 3. Create package

mv plugin ftrack-connect-cinema-4d-$VERSION
zip -r ftrack-connect-cinema-4d-$VERSION.zip ftrack-connect-cinema-4d-$VERSION


cd ..
