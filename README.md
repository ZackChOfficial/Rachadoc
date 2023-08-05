# Rachadoc

**Rachadoc** is a Patient Management System designed to help clinics and hospitals easily manage patient information and appointment scheduling.

## Features

- [x] ***Patient profiles*** Register new patients, edit and update patient information
- [x] ***Appointment scheduling*** Schedule patient appointments and send reminders
- [x] ***Patient history*** Description of feature 3 and how it works
- [x] ***Secure access*** Role based access for doctors, clinic staff and administrators
- [ ] ***Reporting*** Custom reports on patient data, appointments, billing etc.
- [ ] ***Billing*** Generate invoices, process payments and insurance claims

## Screenshots

TODO

## Demo

TODO

## Tech Stack

**Backend**

- Django
- DRF (*Django Rest Framework*)
- Celery
- Channels (*websockets*)
- Redis
- Postgres
- Pytest

**Frontend**

TODO: link frontend Repo

## Setup

Brief instructions on how to get the project running locally:

1. Clone the repo
2. Install dependencies
3. Configure environment variables
    add `.env` file inside `core/settings` with the following variables
    ```python
    client_id=X
    client_secret=X

    REDIS_URL=X
    CELERY_BROKER_URL=X
    CELERY_RESULT_BACKEND=X

    CELERY_BROKER_TRANSPORT_URL=X
    CELERY_RESULT_TRANSPORT_BACKEND=X

    # django-anymail
    SENDINBLUE_KEY=X

    # s3
    AWS_ACCESS_KEY_ID=X
    AWS_SECRET_ACCESS_KEY=X
    AWS_STORAGE_BUCKET_NAME=X
    AWS_S3_REGION_NAME=X
    AWS_USE_S3=False

    POSTGRES_USER=X
    POSTGRES_DB=X
    POSTGRES_PASSWORD=X
    ```
4. Database
    ```python
    # create db
    create database rachadoc with owner = rachadoc encoding = 'UTF8';
    ALTER ROLE rachadoc  SUPERUSER;

    # Enabling PostGIS
    CREATE EXTENSION postgis;
    ```

## Contributors ##

Frontend: [Anas](https://github.com/anasch132)

## Licence ##
[MIT](https://choosealicense.com/licenses/mit) License.