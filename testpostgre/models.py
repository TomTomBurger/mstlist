from django.db import models
from django.db.models import Q

class Group(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    name = models.CharField('グループ名', max_length=30)

    def __str__(self):
        return self.name

class MemberModelQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(full_name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct()
        return qs.order_by("id")

class MemberModelManager(models.Manager):
    def get_queryset(self):
        return MemberModelQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Member(models.Model):

    full_name = models.CharField('名前', max_length=20)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    auth = models.BooleanField(
        '権限A',
        default=False,
    )
    objects = MemberModelManager()


