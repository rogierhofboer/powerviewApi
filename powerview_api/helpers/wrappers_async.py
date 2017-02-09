import asyncio
import json
import logging

lgr = logging.getLogger(__name__)


def async_api(cls):
    def get_wrapper(func):
        @asyncio.coroutine
        def wrapped(self, *args, **kwargs):
            url, params = func(self, *args, **kwargs)
            # session = self.session
            try:
                resp = yield from self.session.get(url, params=params)
            except Exception as ex:
                lgr.exception(ex)
                raise
            try:
                _json = yield from resp.json()
                yield from resp.release()
            except Exception as ex:
                lgr.exception(ex)
                resp.close()
                raise
            else:
                return self.process_response(_json)

        return wrapped

    def put_wrapper(func):
        @asyncio.coroutine
        def wrapped(self, *args, **kwargs):
            url, data = func(self, *args, **kwargs)
            try:
                data = json.dumps(data)
            except Exception as ex:
                lgr.exception(ex)
                raise
            try:
                resp = yield from self.session.put(url, data=data)
            except Exception as ex:
                lgr.exception(ex)
                raise
            try:
                _json = yield from resp.json()
                yield from resp.release()
            except Exception as ex:
                lgr.exception(ex)
                resp.close()
                raise
            else:
                return self.process_response(_json)

        return wrapped

    for name in dir(cls):
        func = getattr(cls, name)
        try:
            if getattr(func, 'get_method', False):
                setattr(cls, name, get_wrapper(func))

            elif getattr(func, 'put_method', False):
                setattr(cls, name, put_wrapper(func))
        except AttributeError:
            pass

    return cls
