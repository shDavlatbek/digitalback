import threading

from django.db.models.query import QuerySet
from django.db import models

_active_filter_state = threading.local()


class ActiveRecordMiddleware:
    """
    Middleware to automatically filter out inactive records from QuerySets.
    This should be added to settings.MIDDLEWARE after the standard Django middleware.
    Skips filtering for admin pages so that inactive records are visible in the admin.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Monkey patch QuerySet to automatically filter out inactive records
        original_init = QuerySet.__init__
        
        def _patched_queryset_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            # Skip filtering if we're in an admin request
            if getattr(_active_filter_state, 'skip_filter', False):
                return
            # Only apply to models with an is_active field
            model = self.model
            if hasattr(model, 'is_active'):
                # Check if there's already a filter for is_active
                has_is_active_filter = any(
                    q.lhs.field.name == 'is_active' 
                    for q in self.query.where.children 
                    if hasattr(q, 'lhs') and hasattr(q.lhs, 'field')
                )
                if not has_is_active_filter:
                    self.query = self.query.clone()
                    self.query.add_q(models.Q(is_active=True))
        
        QuerySet.__init__ = _patched_queryset_init
        
    def __call__(self, request):
        # Disable automatic is_active filtering for admin pages
        _active_filter_state.skip_filter = request.path.startswith('/admin/')
        try:
            response = self.get_response(request)
        finally:
            _active_filter_state.skip_filter = False
        return response