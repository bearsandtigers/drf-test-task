**REST API imitating cloud instances transition.**

*Dependencies*:
Python 3.6
django
djangorestframework
django-rest-swagger
requests

To run:
1. cd drf
2. ./manage.py makemigrations app && ./manage.py migrate
3. ./manage.py runserver

To run tests (not full-fledged, just an example):
`./manage.py test`

To test API with requests:
`./tester.py` (from the repo root directory)
