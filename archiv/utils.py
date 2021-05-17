import glob
import click
import collatex
from pathlib import Path
import asyncio

from django.conf import settings

from acdh_tei_pyutils.tei import TeiReader
from acdh_collatex_utils.acdh_collatex_utils import chunks_to_df
from acdh_collatex_utils.collatex_patch import visualize_table_vertically_with_colors
from collatex.core_functions import export_alignment_table_as_tei
from freud_api_crawler import freud_api_crawler as frd
from freud_api_crawler.post_process import create_united_files


from archiv.models import FrdWork, FrdManifestation, FrdCollationSample


async def create_collations(col_obj):
    await asyncio.sleep(2)
    df = chunks_to_df(col_obj.files(), char_limit=False)
    counter = 0
    for gr in df.groupby('chunk_nr'):
        await asyncio.sleep(2)
        counter += 1
        col_sample_id = f"{col_obj.hashes()}__{counter:03}"
        collation = collatex.Collation()
        cur_df = gr[1]
        for i, row in cur_df.iterrows():
            print(row['id'])
            collation.add_plain_witness(row['id'], row['text'])
        table = collatex.collate(collation)
        col_sample, _ = FrdCollationSample.objects.get_or_create(
            title_slug=col_sample_id,
            parent_col=col_obj
        )
        data = visualize_table_vertically_with_colors(
            table,
            collation
        )
        data_tei = export_alignment_table_as_tei(
            table,
            collation
        )
        col_sample.data_html = data
        col_sample.data_tei = data_tei
        col_sample.save()
    return col_obj


def get_or_create_werk(drupal_work):
    frd_work, _ = FrdWork.objects.get_or_create(
        title_slug=drupal_work.md__path__alias.split('/')[-1],
        drupal_hash=drupal_work.werk_id,
    )
    frd_work.drupal_json = drupal_work.werk
    frd_work.save_path = drupal_work.md__path__alias
    frd_work.save()
    return frd_work


def create_mans_from_folder(man_dir, frd_work, auth_items):
    glob_pattern = f"{man_dir}/*.xml"
    files = glob.glob(glob_pattern)
    manifestations = []
    for x in files:
        doc = TeiReader(x)
        man_id = doc.any_xpath('.//@xml:id')[0].split('__')[-1]
        drupal_man_obj = frd.FrdManifestation(
            auth_items=auth_items, manifestation_id=man_id
        )
        man_slug = Path(x).stem
        frd_man, _ = FrdManifestation.objects.get_or_create(
            title_slug=man_slug,
            work=frd_work
        )
        frd_man.tei_doc = doc.return_string()
        frd_man.drupal_hash = man_id
        frd_man.save_path = x
        try:
            frd_man.drupal_json = drupal_man_obj.manifestation
        except KeyError:
            pass
        frd_man.save()
        manifestations.append(frd_man)
    return manifestations


async def import_work(frd_werk):
    await asyncio.sleep(2)
    out_dir = settings.MEDIA_ROOT
    auth_items = frd.get_auth_items(settings.FRD_USER, settings.FRD_PW)
    werk_obj = frd.FrdWerk(
                auth_items=auth_items,
                werk_id=frd_werk.drupal_hash
            )
    rel_manifestations = werk_obj.manifestations
    for x in rel_manifestations:
        await asyncio.sleep(2)
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
