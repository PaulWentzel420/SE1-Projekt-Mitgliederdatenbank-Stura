# Tests
## Commands

python .\manage.py test --verbosity=2 --parallel --keepdb
python .\manage.py test --verbosity=3 --parallel --pattern="test_004*.py"

## Unterscheiden von Platformen
import platform
platform.system()
'Linux'
'Windows'

## HELP
https://docs.djangoproject.com/en/3.0/topics/testing/overview/


## TODO: Suchen nach einen Linter, der den Sourcecode automatisch nach PEP8 anpasst
PS C:\Users\Lukas Hirsch\Documents\StuRa-Mitgliederdatenbank\tests> autopep8 -i -r -a -a -a .


## TODOS
TODO:
    Admin und User unterscheiden
        + Button Add
        + Button Delete
        + Button Bearbeiten
