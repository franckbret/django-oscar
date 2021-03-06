from django.conf.urls import patterns
from oscar.core.loading import feature_hidden


class Application(object):
    name = None
    hidable_feature_name = None

    def __init__(self, app_name=None, **kwargs):
        self.app_name = app_name
        # Set all kwargs as object attributes
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_urls(self):
        """
        Return the url patterns for this app, MUST be implemented in the
        subclass
        """
        return patterns('')

    def post_process_urls(self, urlpatterns):
        """
        Customise URL patterns.

        By default, this only allows custom decorators to be specified, but you
        could override this method to do anything you want.
        """
        # Test if this the URLs in the Application instance should be
        # available.  If the feature is hidden then we don't include the URLs.
        if feature_hidden(self.hidable_feature_name):
            return patterns('')

        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                self.post_process_urls(pattern.url_patterns)
            if not hasattr(pattern, '_callback'):
                continue
            # Look for a custom decorator
            decorator = self.get_url_decorator(pattern)
            if decorator:
                # Nasty way of modifying a RegexURLPattern
                pattern._callback = decorator(pattern._callback)
        return urlpatterns

    def get_url_decorator(self, url_name):
        """
        Return the appropriate decorator for the view function with the passed
        URL name
        """
        return None

    @property
    def urls(self):
        # We set the application and instance namespace here
        return self.get_urls(), self.app_name, self.name
