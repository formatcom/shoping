## Como usar en local

Para usar esta proyecto, siga estos pasos:

1. virtualenv env
2. source env/bin/active
3. pip install -r requirements.txt
4. python manage migrate
5. createsuperuser
6. heroku login
7. heroku local
8. configurar en el /admin epayco

## Usuario de prueba
username: apps.co
password: testings

## Tarjetas de Credito de Pruebas

[Docs epayco/testing](https://docs.epayco.co/tools/testing)


## Estandar Webcheckout

[Docs epayco/standard_checkout](https://epayco.co/docs/standard_checkout/#introduction)


## Deployment en Heroku

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate
    $ heroku run python manage.py createsuperuser

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.


## License: MIT


## Further Reading

- [heroku-django-template](https://github.com/heroku/heroku-django-template)
- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
