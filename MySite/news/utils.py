from django.db.models import Count


class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()


class RelatedObjectsCountMixin:
    """Добавляет в queryset аннотацию с количеством связанных комментариев."""

    def get_queryset(self):
        return super().get_queryset().annotate(comments_count=Count('comments'))
