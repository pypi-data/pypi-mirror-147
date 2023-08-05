import errno
import json
import os
import pytest
import random
import shutil

from falcon import API, testing, __version__ as FALCONVERSION
import falcon.asgi
from falcon_caching import Cache, AsyncCache
from falcon_caching.cache import SUPPORTED_HASH_FUNCTIONS

try:
    __import__("pytest_xprocess")
    from xprocess import ProcessStarter
except ImportError:

    @pytest.fixture(scope="session")
    def xprocess():
        pytest.skip("pytest-xprocess not installed.")

# what is the Falcon main version (eg 2 or 3, etc)
FALCONVERSION_MAIN = int(FALCONVERSION.split('.')[0])

# accepted success rate
# see https://stackoverflow.com/questions/47726778/pytest-allow-failure-rate?rq=1
ACCEPTABLE_FAILURE_RATE = 99

# the different cache_types that will be tested
CACHE_TYPES = [
    'simple',
    'filesystem',
    'redis',
    'redissentinel',
    'uwsgi',
    'memcached',
    'gaememcached',
    'saslmemcached',
    'spreadsaslmemcached',
]

# the different cache_types that will be tested
ASYNC_CACHE_TYPES = [
    'simple',
    'filesystem',
    'redis',
    'redissentinel',
    #'uwsgi',
    'memcached',
    'gaememcached',
    #'saslmemcached',
    #'spreadsaslmemcached',
]

# what eviction strategies we will be testing
EVICTION_STRATEGIES = [
    'time-based',
    'rest-based',
    'rest-and-time-based'
]

# cache-busting methods
# eg which HTTP methods are busting the cache in 'rest-based'
# and 'rest-and-time-based' eviction strategy
CACHE_BUSTING_METHODS = [
    'POST',
    'PUT',
    'PATCH',
    'DELETE'
]

# we want to test the pruning, so we set the threshold low
# instead of the default 500
CACHE_THRESHOLD = 5

# which port the Redis server will be listening on
# which is started by xprocess
REDIS_PORT = 63799

# to test expiring cache, how long the cache expires
CACHE_EXPIRES = 1


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    """ What final test success rate is acceptable
    see https://stackoverflow.com/questions/47726778/pytest-allow-failure-rate?rq=1
    """
    if exitstatus != pytest.ExitCode.TESTS_FAILED:
        return
    failure_rate = (100.0 * session.testsfailed) / session.testscollected
    if failure_rate <= ACCEPTABLE_FAILURE_RATE:
        session.exitstatus = 0


# parametrized fixture to create caches with different types (eg backends)
@pytest.fixture(params=CACHE_TYPES)
def caches(request, tmp_path, redis_server, redis_sentinel_server, memcache_server):
    """ Time-based cache parametrized to generate a cache
    for each cache_type (eg backend)
    """
    if request.param == 'redissentinel' and os.getenv('TRAVIS', 'no') == 'yes':
        pytest.skip("Unfortunately on Travis Redis Sentinel currently can't be installed")

    # uwsgi tests should only run if running under uwsgi
    if request.param == 'uwsgi':
        try:
            import uwsgi
        except ImportError:
            pytest.skip("uWSGI could not be imported, are you running under uWSGI?")
            return None

    # build a dict of caches for each eviction strategy
    caches = {
        eviction_strategy:
            Cache(
                config={
                    'CACHE_EVICTION_STRATEGY': eviction_strategy,
                    'CACHE_TYPE': request.param,
                    'CACHE_THRESHOLD': CACHE_THRESHOLD,
                    'CACHE_DIR': tmp_path if request.param == 'filesystem' else None,
                    'CACHE_REDIS_PORT': REDIS_PORT
                }
            )
        for eviction_strategy in EVICTION_STRATEGIES
    }
    return caches


# parametrized fixture to create caches with different types (eg backends)
@pytest.fixture(params=ASYNC_CACHE_TYPES)
def async_caches(request, tmp_path, redis_server, redis_sentinel_server, memcache_server):
    """ Time-based cache parametrized to generate a cache
    for each cache_type (eg backend)
    """
    if request.param == 'redissentinel' and os.getenv('TRAVIS', 'no') == 'yes':
        pytest.skip("Unfortunately on Travis Redis Sentinel currently can't be installed")

    # build a dict of caches for each eviction strategy
    caches = {
        eviction_strategy:
            AsyncCache(
                config={
                    'CACHE_EVICTION_STRATEGY': eviction_strategy,
                    'CACHE_TYPE': request.param,
                    'CACHE_THRESHOLD': CACHE_THRESHOLD,
                    'CACHE_DIR': tmp_path if request.param == 'filesystem' else None,
                    'CACHE_REDIS_PORT': REDIS_PORT
                }
            )
        for eviction_strategy in EVICTION_STRATEGIES
    }
    return caches


@pytest.fixture()
def cache_time_based(caches):
    """ Returns a cache instance, which can directly be used in
    the test_cache_backends.py to test the various cache backends
    """
    return caches['time-based'].cache


@pytest.fixture()
def async_cache_time_based(async_caches):
    """ Returns a cache instance, which can directly be used in
    the test_cache_backends.py to test the various cache backends
    """
    return async_caches['time-based'].cache


@pytest.fixture(scope="module")
def redis_server(xprocess):
    try:
        import redis
    except ImportError:
        pytest.skip("Python package 'redis' is not installed.")

    class Starter(ProcessStarter):
        pattern = "[Rr]eady to accept connections"
        args = ["redis-server", "--port", REDIS_PORT]

    try:
        xprocess.ensure("redis_server", Starter)
    except IOError as e:
        # xprocess raises FileNotFoundError
        if e.errno == errno.ENOENT:
            pytest.skip("Redis is not installed.")
        else:
            raise

    yield
    xprocess.getinfo("redis_server").terminate()


@pytest.fixture(scope="module")
def redis_sentinel_server(xprocess, redis_server):
    # on Travis there is no redis-sentinel, so we need to skip this,
    # but can't use pytest.skip() as that would bubble up to all tests
    if os.getenv('TRAVIS', 'no') == 'yes':
        yield
    else:
        try:
            import redis
        except ImportError:
            pytest.skip("Python package 'redis' is not installed.")

        # copy the sentinel_original.conf to sentinel.conf, as sentinel
        # will modify it
        shutil.copy("tests/sentinel_original.conf", "tests/sentinel.conf")

        class Starter(ProcessStarter):
            pattern = "monitor master mymaster"
            args = ["redis-sentinel", f"{os.getcwd()}/tests/sentinel.conf"]

        try:
            xprocess.ensure("redis_sentinel_server", Starter)
        except IOError as e:
            # xprocess raises FileNotFoundError
            if e.errno == errno.ENOENT:
                pytest.skip("Redis Sentinel is not installed.")
            else:
                raise

        yield
        xprocess.getinfo("redis_sentinel_server").terminate()


@pytest.fixture(scope="module")
def memcache_server(xprocess):
    try:
        import pylibmc as memcache
    except ImportError:
        try:
            from google.appengine.api import memcache
        except ImportError:
            try:
                import memcache
            except ImportError:
                pytest.skip(
                    "Python package for memcache is not installed. Need one of "
                    "pylibmc', 'google.appengine', or 'memcache'."
                )

    class Starter(ProcessStarter):
        pattern = ""
        args = ["memcached", "-vv"]

    try:
        xprocess.ensure("memcached", Starter)
    except IOError as e:
        # xprocess raises FileNotFoundError
        if e.errno == errno.ENOENT:
            pytest.skip("Memcached is not installed.")
        else:
            raise

    yield
    xprocess.getinfo("memcached").terminate()


@pytest.fixture(params=EVICTION_STRATEGIES)
def app(request, caches):
    """ Creates a Falcon app with the given cache instance to be used
    by functional tests
    """
    # get the cache for the given eviction strategy
    cache = caches[request.param]

    class CachedResource:
        """ A cached resource with long expiration and all the different methods """
        @cache.cached(timeout=60)
        def on_get(self, req, resp):
            if FALCONVERSION_MAIN < 3:
                resp.body = json.dumps({'num': random.randrange(0, 100000)})
            else:
                resp.text = json.dumps({'num': random.randrange(0, 100000)})

        @cache.cached(timeout=60)
        def on_post(self, req, resp):
            pass

        @cache.cached(timeout=60)
        def on_put(self, req, resp):
            pass

        @cache.cached(timeout=60)
        def on_patch(self, req, resp):
            pass

        @cache.cached(timeout=60)
        def on_delete(self, req, resp):
            pass

    class CachedResourceExpires:
        """ A cached resource with short expiration """
        @cache.cached(timeout=CACHE_EXPIRES)
        def on_get(self, req, resp):
            if FALCONVERSION_MAIN < 3:
                resp.body = json.dumps({'num': random.randrange(0, 100000)})
            else:
                resp.text = json.dumps({'num': random.randrange(0, 100000)})

        @cache.cached(timeout=CACHE_EXPIRES)
        def on_post(self, req, resp):
            pass

    @cache.cached(timeout=CACHE_EXPIRES)
    class ClassCachedResourceExpires:
        """ A cached resource which cached on the class level """
        def on_get(self, req, resp):
            if FALCONVERSION_MAIN < 3:
                resp.body = json.dumps({'num': random.randrange(0, 100000)})
            else:
                resp.text = json.dumps({'num': random.randrange(0, 100000)})

        def on_post(self, req, resp):
            pass

    app = API(middleware=cache.middleware)

    app.add_route('/randrange_cached', CachedResource())
    app.add_route('/randrange_cached_expires', CachedResourceExpires())
    app.add_route('/randrange_class_cached_expires', ClassCachedResourceExpires())

    return app


@pytest.fixture(params=EVICTION_STRATEGIES)
def async_app(request, async_caches):
    """ Creates a Falcon app with the given cache instance to be used
    by functional tests
    """
    # get the cache for the given eviction strategy
    cache = async_caches[request.param]

    class CachedResource:
        """ A cached resource with long expiration and all the different methods """
        @cache.cached(timeout=60)
        async def on_get(self, req, resp):
            if FALCONVERSION_MAIN < 3:
                resp.body = json.dumps({'num': random.randrange(0, 100000)})
            else:
                resp.text = json.dumps({'num': random.randrange(0, 100000)})

        @cache.cached(timeout=60)
        async def on_post(self, req, resp):
            pass

        @cache.cached(timeout=60)
        async def on_put(self, req, resp):
            pass

        @cache.cached(timeout=60)
        async def on_patch(self, req, resp):
            pass

        @cache.cached(timeout=60)
        async def on_delete(self, req, resp):
            pass

    class CachedResourceExpires:
        """ A cached resource with short expiration """
        @cache.cached(timeout=CACHE_EXPIRES)
        async def on_get(self, req, resp):
            if FALCONVERSION_MAIN < 3:
                resp.body = json.dumps({'num': random.randrange(0, 100000)})
            else:
                resp.text = json.dumps({'num': random.randrange(0, 100000)})

        @cache.cached(timeout=CACHE_EXPIRES)
        async def on_post(self, req, resp):
            pass

    @cache.cached(timeout=CACHE_EXPIRES)
    class ClassCachedResourceExpires:
        """ A cached resource which cached on the class level """
        async def on_get(self, req, resp):
            if FALCONVERSION_MAIN < 3:
                resp.body = json.dumps({'num': random.randrange(0, 100000)})
            else:
                resp.text = json.dumps({'num': random.randrange(0, 100000)})

        async def on_post(self, req, resp):
            pass

    app = falcon.asgi.App(middleware=cache.middleware)

    app.add_route('/randrange_cached', CachedResource())
    app.add_route('/randrange_cached_expires', CachedResourceExpires())
    app.add_route('/randrange_class_cached_expires', ClassCachedResourceExpires())

    return app


@pytest.fixture()
def client(app):
    """ Creates a Falcon test client
    """
    return testing.TestClient(app)


@pytest.fixture()
def async_client(async_app):
    """ Creates a Falcon test client
    """
    return testing.TestClient(async_app)


@pytest.fixture(
    params=[method for method in SUPPORTED_HASH_FUNCTIONS],
    ids=[method.__name__ for method in SUPPORTED_HASH_FUNCTIONS],
)
def hash_method(request):
    return request.param
