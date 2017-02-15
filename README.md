# origin-tech-test
This was written in python3

**To run it:**

`$ git clone git@github.com:danyilmaz/origin-tech-test.git`

`$ mkvirtualenv -p python3 danyilmaz-techtest-origin`

`$ cd origin-tech-test`

`$ pip install -r requirements.txt`

`$ ./manage.py migrate`

`$ ./manage.py createsuperuser`


You may want to create more than one user so as to test a user's ability to edit/delete tasks created by a different user.

Tests can be run with `$ ./manage.py test tasks`



**Areas that should be improved:**

Test coverage is patchy at best, the models are well tested, but too much logic happens in the views.

This logic should be moved to somewhere else for ease of testing and for separation of concerns.

The styling is very basic. Forms should be re-written using floppyforms or crispyforms,
or hand crafted with classes on each element.

User registration is missing entirely
