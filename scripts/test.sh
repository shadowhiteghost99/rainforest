#!/bin/bash

case "$1" in
	"dev")
		REPORT="term-missing"
		COVERAGE_THRESH=85
		;;
	"ci")
		REPORT="term-missing"
		COVERAGE_THRESH=90
		;;
	"html")
		REPORT="html"
		COVERAGE_THRESH=0
		;;
	*)
		echo "Warning: Invalid or missing argument: defaulting to dev"
		REPORT="term-missing"
		COVERAGE_THRESH=85
		;;
esac


python3 -m pytest --cov=src --cov-fail-under=${COVERAGE_THRESH} --cov-report=${REPORT}
