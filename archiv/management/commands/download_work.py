import click
import glob

from django.conf import settings
from django.core.management.base import BaseCommand

from freud_api_crawler import freud_api_crawler as frd
from freud_api_crawler.post_process import create_united_files

from archiv.utils import get_or_create_werk


class Command(BaseCommand):

    help = "Downloads Manifestations for passed in work id"

    def add_arguments(self, parser):
        parser.add_argument('work_ids', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        auth_items = frd.get_auth_items(settings.FRD_USER, settings.FRD_PW)
        for w in kwargs['work_ids']:
            werk_obj = frd.FrdWerk(
                auth_items=auth_items, werk_id=w
            )
            frd_werk = get_or_create_werk(werk_obj)
            rel_manifestations = werk_obj.manifestations
            for x in rel_manifestations:
                try:
                    frd_man = frd.FrdManifestation(
                        out_dir=settings.MEDIA_ROOT,
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
            click.echo(
                click.style(
                    f"finished download\n{werk_obj.manifestations_count} Manifestations for {werk_obj.md__title} into {settings.MEDIA_ROOT}",
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
