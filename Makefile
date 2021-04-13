lint:
	flake8

test:
	python mysite/manage.py test polls

serve-local:
	python mysite/manage.py runserver

migrate:
	python mysite/manage.py makemigrations
	python mysite/manage.py migrate

archive_name = "EdAider backend test task code.zip"
archive:
	git archive -o ${archive_name} HEAD
	zip --delete ${archive_name} "CHECKLIST.md"
