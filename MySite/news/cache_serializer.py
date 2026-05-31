
import json
import datetime
import decimal

from django.core.cache.backends.filebased import FileBasedCache
from django_redis.cache import RedisCache
from django_redis.serializers.json import JSONSerializer


class _ExtendedEncoder(json.JSONEncoder):


    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {'__type__': 'datetime', 'value': obj.isoformat()}
        if isinstance(obj, datetime.date):
            return {'__type__': 'date', 'value': obj.isoformat()}
        if isinstance(obj, decimal.Decimal):
            return {'__type__': 'decimal', 'value': str(obj)}
        if isinstance(obj, bytes):
            return {'__type__': 'bytes', 'value': obj.hex()}
        if isinstance(obj, set):
            return {'__type__': 'set', 'value': list(obj)}
        return super().default(obj)


def _extended_decoder(dct):
    t = dct.get('__type__')
    if t == 'datetime':
        return datetime.datetime.fromisoformat(dct['value'])
    if t == 'date':
        return datetime.date.fromisoformat(dct['value'])
    if t == 'decimal':
        return decimal.Decimal(dct['value'])
    if t == 'bytes':
        return bytes.fromhex(dct['value'])
    if t == 'set':
        return set(dct['value'])
    return dct


class JSONFileBasedCache(FileBasedCache):

    def _serialize(self, value):
        return json.dumps(value, cls=_ExtendedEncoder, ensure_ascii=False)

    def _deserialize(self, data):
        return json.loads(data, object_hook=_extended_decoder)

    def set(self, key, value, timeout=None, version=None):
        # Оборачиваем значение в JSON-строку перед сохранением
        try:
            serialized = self._serialize(value)
            return super().set(key, serialized, timeout=timeout, version=version)
        except (TypeError, ValueError):
            # Если JSON не справился — fallback к стандартному поведению
            return super().set(key, value, timeout=timeout, version=version)

    def get(self, key, default=None, version=None):
        raw = super().get(key, default=None, version=version)
        if raw is None:
            return default
        if isinstance(raw, str):
            try:
                return self._deserialize(raw)
            except (ValueError, TypeError):
                return raw
        return raw


class JSONRedisCache(RedisCache):
    pass
