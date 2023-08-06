Django DB Email Backend
=======================

Initially, Django email backend for storing messages to a database. This is intended to be used in developement in cases where you
want to test sending emails, but don't want to send real emails and don't have access to the console output (such as on
a remote server).

As this KUWAITNET fork, package has been updated and introduced `SMTPDBEmailBackend` which is a mixture between SMTP and DB mail backend,
it writes to the database then send the email over smtp, if any errors happen while sending it is reflected in the email model.
Also Package is now production ready.

Access to Email message content is allowed only for super user as this might be a security hazard.

To install::

    pip install django-db-email-backend


In settings.py::

    INSTALLED_APPS += ['db_email_backend']
    EMAIL_BACKEND = 'db_email_backend.backend.DBEmailBackend'
    # or
    # EMAIL_BACKEND = 'db_email_backend.backend.SMTPDBEmailBackend'


