#!/bin/bash
# set env DEV to false
build() {
    echo "Building package..."
    export DEV=false

    # Clean up previous builds
    rm -rf dist/

    # Build the package
    python3 -m build
    
    export DEV=true
    echo "Build complete..."
}

# Function to upload to TestPyPI
push_test() {
    echo "Uploading to TestPyPI..."
    python3 -m twine upload --repository testpypi dist/* --verbose
}

# Function to upload to PyPI
push_prod() {
    echo "Uploading to PyPI..."
    python3 -m twine upload dist/* --verbose
}

# Handle command line arguments
case "$1" in
    "test")
        build
        push_test
        ;;
    "prod")
        build
        push_prod
        ;;
    *)
        echo "Uploading to both TestPyPI and PyPI..."
        build
        push_test
        push_prod
        ;;
esac
