# CSRF for Django-API
- CSRF prevents an attacker from tricking a user into performing an action they don't intend to. It's about protecting the server from unauthorized actions initiated by a logged-in user.

CSRF are related to forms and we have {% csrf_token %} when creating templated forms but because with a dedicated React front-end setup this protection isn't inherently available.

We can allow specific cross-domain request from our frontend by setting: `CSRF_TRUSTED_ORIGINS` at the bottom of the `settings.py`

```python
CSRF_TRUSTED_ORIGINS = ['localhost:3000']
```