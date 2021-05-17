import click
import glob

from django.conf import settings
from django.core.management.base import BaseCommand

from freud_api_crawler import freud_api_crawler as frd
from freud_api_crawler.post_process import create_united_files

from archiv.models import FrdWork
from archiv.utils import get_or_create_werk, create_mans_from_folder


class Command(BaseCommand):

    help = "Downloads Manifestations for passed in work id"

    def add_arguments(self, parser):
        parser.add_argument('work_ids', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        out_dir = settings.MEDIA_ROOT
        auth_items = frd.get_auth_items(settings.FRD_USER, settings.FRD_PW)
        if "all" in kwargs['work_ids']:
            ids = [x.drupal_hash for x in FrdWork.objects.all()]
        else:
            ids = kwargs['work_ids']
        print(ids)
        for w in ids:
            werk_obj = frd.FrdWerk(
                auth_items=auth_items, werk_id=w
            )
            frd_werk = get_or_create_werk(werk_obj)
            rel_manifestations = werk_obj.manifestations
            for x in rel_manifestations:
                try:
                    frd_man = frd.FrdManifestation(
                        out_dir=out_dir,
                        manifestation_id=x['man_id'],
                        auth_items=auth_items
                    )
                    frd_man.make_xml(save=True, limit=False)
                except Exception as e:
                    click.echo(
                        click.style(
                            f"processing Manifestation {x} did not not work due to Error {e}",
                            fg='red'
                        )
                    )
            werk_count = werk_obj.manifestations_count
            click.echo(
                click.style(
                    f"finished download\n{werk_count} Manifestations for {werk_obj.md__title} into {out_dir}",
                    fg='green'
                )
            )
            werk_save_path = frd_man.manifestation_save_location_folder
            glob_pattern = f"{werk_save_path}/*.xml"
            files = glob.glob(glob_pattern)
            merged = create_united_files(glob_pattern)
            click.echo(
                click.style(
                    f"finished: merged {len(files)} Documents from {glob_pattern}\n\
                    into {len(merged[1].keys())} Documents to {merged[0]}",
                    fg='green'
                )
            )
            create_mans_from_folder(merged[0], frd_werk, auth_items)
