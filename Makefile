
report: pep8-report pylint-report

pep8-report:
	echo "Checking code against PEP8"
	pep8 --max-line-length 120 -r marketing > pep8.log || exit 0
	rm -rf ${tmpdir}

pylint-report:
	echo "Analyzing code with pylint"
	pylint --output-format=parseable --rcfile=.pylintrc marketing tests/*.py > pylint.log || exit 0
