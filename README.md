# koodous
Koodous Secure Microservice + dockerfile

example running command:
> python manage.py runserver


example web-request using httpie:
\nlookup hash ===== >>  >http -f 127.0.0.1:8000/api/scan key='tpu6#=xx8(p1akq%o#ss%=dg98q1h0orxcgn5=&gss2+0a0=dr' hash='5c6005941a32fed7a874836ddd8eca87e48f085a'
\nlookup anything ====> >http -f 127.0.0.1:8000/api/scan key='tpu6#=xx8(p1akq%o#ss%=dg98q1h0orxcgn5=&gss2+0a0=dr' search='domain'
