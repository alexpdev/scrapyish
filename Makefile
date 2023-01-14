
build: clean # build wheel and sdist
	python -m build --sdist


release: build # upload to twine
	twine upload dist/*

clean: # clean directory
	rm -rfv build
	rm -rfv dist
	rm -rfv *.egg-info
	rm -rfv .tox/
	rm -fvr -- *'/__pycache__'
	rm -rfv .eggs/
	rm -rfv .pytest_cache
	rm -rfv htmlcov/
	rm -rfv .coverage

push: clean # push to repo
	git add .
	git commit -m "$m pushing"
	git push
