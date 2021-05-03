from django.contrib import admin

from archiv.models import FrdWork, FrdManifestation, FrdCollation


@admin.register(FrdCollation)
class FrdCollation(admin.ModelAdmin):
    list_display = (
        'work',
    )
    list_filter = (
        'work',
        'manifestation'
    )


@admin.register(FrdWork)
class FrdWork(admin.ModelAdmin):
    list_display = (
        'title_slug',
        'drupal_hash'
    )
    search_fields = [
        'title_slug'
    ]


@admin.register(FrdManifestation)
class FrdManifestationAdmin(admin.ModelAdmin):
    list_display = (
        'work',
        'title_slug',
        'drupal_hash',
        'save_path'
    )
    list_filter = (
        'work',
    )
    search_fields = [
        'title_slug'
    ]
