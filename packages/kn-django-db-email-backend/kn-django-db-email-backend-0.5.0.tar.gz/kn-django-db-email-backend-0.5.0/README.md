Django DB Email Backend
=======================

Django email backend for storing messages to a database. This is intended to be used in developement in cases where you
want to test sending emails, but don't want to send real emails and don't have access to the console output (such as on
a remote server).

To install:

```sh
pip install django-db-email-backend
```

In settings.py:

```python
INSTALLED_APPS += ['db_email_backend']
EMAIL_BACKEND = 'db_email_backend.backend.DBEmailBackend'
# or
# EMAIL_BACKEND = 'db_email_backend.backend.SMTPDBEmailBackend'
```
