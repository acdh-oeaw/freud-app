import click
import requests

from tqdm import tqdm

from django.conf import settings
from django.core.management.base import BaseCommand

from freud_api_crawler import freud_api_crawler as frd

from archiv.models import FrdWork

auth_items = frd.get_auth_items(settings.FRD_USER, settings.FRD_PW)
r = requests.get(
    settings.FRD_WORK_LIST,
    cookies=auth_items['cookie'],
    allow_redirects=True
)


class Command(BaseCommand):

    help = "Creates work objects from drupal endpoint"

    def handle(self, *args, **kwargs):
        click.echo(
            click.style(
                "fetching list of works",
                fg='green'
            )
        )
        r = requests.get(
            settings.FRD_WORK_LIST,
            cookies=auth_items['cookie'],
            allow_redirects=True
        )
        items = r.json()['data']
        for x in tqdm(items, total=len(items)):
            wid = x['id']
            wslug = x['attributes']['path']['alias'].split('/')[-1]
            wtitle = x['attributes']['field_titel']['value']
            frd_work, _ = FrdWork.objects.get_or_create(
                title_slug=wslug,
                drupal_hash=wid
            )
            frd_work.drupal_json = x
            frd_work.title = wtitle
            frd_work.save()
