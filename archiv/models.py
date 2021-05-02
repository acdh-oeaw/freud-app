from django.db import models


class FrdWork(models.Model):
    title_slug = models.CharField(
        max_length=250,
        unique=True,
    )
    drupal_hash = models.CharField(
        max_length=250,
        unique=True,
    )
    drupal_json = models.JSONField(blank=True, null=True)
    save_path = models.CharField(
        max_length=550,
        unique=True,
        blank=True, null=True
    )

    def __str__(self):
        return self.title_slug


class FrdManifestation(models.Model):
    title_slug = models.CharField(
        max_length=250,
        unique=True,
    )
    drupal_hash = models.CharField(
        max_length=250,
        unique=True,
    )
    drupal_json = models.JSONField(blank=True, null=True)
    work = models.ForeignKey(FrdWork, on_delete=models.CASCADE)
    tei_doc = models.TextField(blank=True, null=True)
    save_path = models.CharField(
        max_length=550,
        unique=True,
        blank=True, null=True
    )

    def __str__(self):
        return self.title_slug
