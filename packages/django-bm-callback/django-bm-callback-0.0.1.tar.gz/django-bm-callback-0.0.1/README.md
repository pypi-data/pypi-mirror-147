Django callback app.

### Installation

Install with pip:

```
pip install django-bm-callback

```

Add `callback` to `INSTALLED_APPS`

Add url `path('callback/', include('callback.urls')),`

Add admin item `ChildItem(model='callback.callback')`

Add js script `modal.js`
