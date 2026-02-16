(venv) jessec@debian:~/Documentos/proyectofinal$ python manage.py test userYC
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.E
======================================================================
ERROR: test_create_user_hashes_password_and_sets_fields (userYC.tests.UserManagerTests.test_create_user_hashes_password_and_sets_fields)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jessec/Documentos/proyectofinal/userYC/tests.py", line 17, in test_create_user_hashes_password_and_sets_fields
    u.full_clean()  # validate the model instance
    ~~~~~~~~~~~~^^
  File "/home/jessec/Documentos/proyectofinal/venv/lib/python3.13/site-packages/django/db/models/base.py", line 1712, in full_clean
    raise ValidationError(errors)
django.core.exceptions.ValidationError: {'phone': ['The phone number entered is not valid.']}

----------------------------------------------------------------------
Ran 2 tests in 1.709s

FAILED (errors=1)
Destroying test database for alias 'default'...


(venv) jessec@debian:~/Documentos/proyectofinal$ python manage.py test userYC
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 2.294s

OK
Destroying test database for alias 'default'...

---------------------------------
TEST DE INTEGRACION
(venv) jessec@debian:~/Documentos/proyectofinal$ python manage.py test userYC.test_integration
/home/jessec/Documentos/proyectofinal/userYC/serializer.py:43: SyntaxWarning: invalid escape sequence '\]'
  email=re.search('^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$',value_email)
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
FFF
======================================================================
FAIL: test_register_invalid_phone_returns_400 (userYC.test_integration.UserRegistrationIntegrationTests.test_register_invalid_phone_returns_400)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jessec/Documentos/proyectofinal/userYC/test_integration.py", line 61, in test_register_invalid_phone_returns_400
    self.assertIn("phone", response.data)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'phone' not found in {'error': "{'first_name': {'first name': ErrorDetail(string='invalid name', code='invalid')}, 'phone': [ErrorDetail(string='The phone number entered is not valid.', code='invalid')], 'confirmation_password': [ErrorDetail(string='This field is required.', code='required')]}"}

======================================================================
FAIL: test_register_serializer_raises_transaction_error_returns_500 (userYC.test_integration.UserRegistrationIntegrationTests.test_register_serializer_raises_transaction_error_returns_500)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jessec/Documentos/proyectofinal/userYC/test_integration.py", line 78, in test_register_serializer_raises_transaction_error_returns_500
    self.assertEqual(response.status_code, 500)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 400 != 500

======================================================================
FAIL: test_register_success_returns_201 (userYC.test_integration.UserRegistrationIntegrationTests.test_register_success_returns_201)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/jessec/Documentos/proyectofinal/userYC/test_integration.py", line 42, in test_register_success_returns_201
    self.assertEqual(response.status_code, 201)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 400 != 201

----------------------------------------------------------------------
Ran 3 tests in 0.048s

FAILED (failures=3)
Destroying test database for alias 'default'...
(venv) jessec@debian:~/Documentos/proyectofinal$ python manage.py test userYC.test_integration
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.636s

OK
Destroying test database for alias 'default'...
-------------------------------
TEST  AUDITORIA PROFUNDA