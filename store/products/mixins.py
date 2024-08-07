from django.db import models


class CodeNameMixin(models.Model):
    code = models.CharField(max_length=50, unique=True, null=True)
    name = models.CharField(max_length=50, null=True)
