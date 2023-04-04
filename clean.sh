
[[ -n $(find . -name "*.pyc") ]] && echo "Cleaning *.pyc files" && find . -name "*.pyc" -type f -delete

[[ -n $(find . -type d -name __pycache__) ]] && echo "removing __pycache__ folders" && rm -rf `find . -type d -name __pycache__`

[ -d .mypy_cache ] && echo "Deleting .mypy_cache directory" && rm -rf .mypy_cache

[ -d .pytest_cache ] && echo "Deleting .pytest_cache directory" && rm -rf .pytest_cache

[ -d htmlcov ] && echo "Deleting htmlcov directory" && rm -rf htmlcov

[ -d dist ] && echo "Deleting dist directory" && rm -rf dist

[ -d src/.pytest_cache ] && echo "Deleting src/.pytest_cache directory" && rm -rf src/.pytest_cache

[ -d src/*.egg-info ] && echo "Deleting src/*.egg-info directory" && rm -rf src/*.egg-info

[ -f .coverage ] && echo "Deleting .coverage file" && rm .coverage

[ -f coverage.xml ] && echo "Deleting coverage.xml file" && rm coverage.xml

