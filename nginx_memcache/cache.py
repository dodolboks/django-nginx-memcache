import hashlib

from django.conf import settings
from django.core.cache import get_cache


CACHE_NGINX_DEFAULT_COOKIE = 'pv'
CACHE_TIME = getattr(settings, 'CACHE_NGINX_TIME', 3600 * 24)
CACHE_ALIAS = getattr(settings, 'CACHE_NGINX_ALIAS', 'default')
nginx_cache = get_cache(CACHE_ALIAS)


def cache_response(request, response,
                    cache_timeout=CACHE_TIME):
    """Cache this response for the web server to grab next time."""
    if request.is_mobile:
       nama_key = '%s&mobile' % request.get_full_path()
    else:
       nama_key = '%s&desktop' % request.get_full_path()

    cache_key = get_cache_key(nama_key)
    nginx_cache.set(cache_key, response._get_content(), cache_timeout)


def get_cache_key(request_path):
    """Use the request path and page version to get cache key."""
    raw_key = u'%s' % (request_path)
    return hashlib.md5(raw_key).hexdigest()


def invalidate_from_request(request):
    """Delete cache key for this request and page version."""
    invalidate(request.get_full_path())


def invalidate(request_path):
    """Delete cache key for this request path and page version."""
    cache_key = get_cache_key(request_path)
    nginx_cache.delete(cache_key)
