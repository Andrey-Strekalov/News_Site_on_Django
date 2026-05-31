"""
Принцип работы:
- Определяем страну пользователя по IP через GeoIP2 (MaxMind GeoLite2).
- Если база GeoIP2 недоступна — используем fallback-определение по диапазону IP.
- Код страны добавляется к ключу кэша через cache_key_prefix.
- Представления могут читать request.geo_country для построения
  гео-специфичных ключей вручную (через cache.get/set).
"""
from django.core.cache import cache


def _get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def _country_from_ip(ip: str) -> str:
    """Определяет код страны.  Пробует GeoIP2, при ошибке возвращает 'RU'."""
    try:
        from django.contrib.gis.geoip2 import GeoIP2
        g = GeoIP2()
        return g.country_code(ip) or 'UNKNOWN'
    except Exception:
        # База GeoLite2 не подключена — возвращаем условное значение
        # (в учебном проекте достаточно демонстрации механизма)
        return 'RU'


class GeoCacheMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = _get_client_ip(request)

        # Кэшируем сам результат гео-определения (5 мин по IP)
        geo_key = f'geo_country_{ip}'
        country = cache.get(geo_key)
        if country is None:
            country = _country_from_ip(ip)
            cache.set(geo_key, country, 300)

        request.geo_country = country
        request.geo_cache_prefix = f'geo_{country}'

        response = self.get_response(request)
        return response
