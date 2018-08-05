clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info

install:
	python setup.py install

test:
	python -m unittest discover -s tests/ -p "*_test.py" -v

lint:
	pylint --load-plugins pylint_quotes aperture/

document:
	sphinx-apidoc -o docs/ aperture/ -e -M -F
	sphinx-build -a -b html docs/ docs/_build

dist:
	python setup.py sdist bdist_wheel

deploy-test:
	twine upload dist/* --config-file .pypirc -r testpypi

deploy-prod:
	twine upload dist/* --config-file .pypirc

