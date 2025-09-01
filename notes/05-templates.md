# Templates 
- To template we can do:
    - Have a `<app>/templates/<app>/index.html`
    - Have a project level template `<project>/templates/index.html`
To do the second templating we should edit the `<project>/settings.py`

```python
# project/settings.py
TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR / "templates"], # new
        ...
        },
    ]
```