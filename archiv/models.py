import os
import shutil
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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

    def get_absolute_url(self):
        return reverse('work_detail', kwargs={'pk': self.id})

    def get_absolute_save_path(self):
        return os.path.join(settings.MEDIA_ROOT, 'werke', self.title_slug) 


@receiver(pre_delete, sender=FrdWork)
def delete_werk_folder(sender, instance, using, **kwargs):
    try:
        shutil.rmtree(instance.get_absolute_save_path())
    except FileNotFoundError:
        pass


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

    def get_absolute_url(self):
        return reverse('manifestation_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.title_slug


class FrdCollation(models.Model):
    work = models.ForeignKey(FrdWork, on_delete=models.CASCADE)
    manifestation = models.ManyToManyField(
        FrdManifestation
    )

    def __str__(self):
        return f"{self.work.title_slug} (ID: {self.id})"

    def get_absolute_url(self):
        return reverse('collation_detail', kwargs={'pk': self.id})

    def files(self):
        return [x.save_path for x in self.manifestation.all()]

    def hashes(self):
        return "|".join([x.drupal_hash for x in self.manifestation.all()])


class FrdCollationSample(models.Model):
    title_slug = models.CharField(
        max_length=250,
        unique=True,
    )
    parent_col = models.ForeignKey(
        FrdCollation, on_delete=models.CASCADE
    )
    data_html = models.TextField(blank=True, null=True)
    data_tei = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title_slug
