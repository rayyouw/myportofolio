# Fix compatibility for Python 3.14+ with Django's BaseContext.__copy__
try:
    from copy import copy
    import django.template.context as _django_context

    def _basecontext_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    def _context_copy(self):
        duplicate = _basecontext_copy(self)
        duplicate.render_context = copy(self.render_context)
        return duplicate

    _django_context.BaseContext.__copy__ = _basecontext_copy
    _django_context.Context.__copy__ = _context_copy
except Exception:
    pass
