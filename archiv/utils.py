import glob
from pathlib import Path

from django.conf import settings
from archiv.models import FrdWork, FrdManifestation

from acdh_tei_pyutils.tei import TeiReader


def get_or_create_werk(drupal_work):
    frd_work, _ = FrdWork.objects.get_or_create(
        title_slug=drupal_work.md__path__alias.split('/')[-1],
        drupal_hash=drupal_work.werk_id,
    )
    frd_work.drupal_json = drupal_work.werk
    frd_work.save_path = drupal_work.md__path__alias
    frd_work.save()
    return frd_work


def create_mans_from_folder(man_dir, frd_work):
    glob_pattern = f"{man_dir}/*.xml"
    files = glob.glob(glob_pattern)
    manifestations = []
    for x in files:
        doc = TeiReader(x)
        man_id = doc.any_xpath('.//@xml:id')[0].split('__')[-1]
        man_slug = Path(x).stem
        frd_man, _ = FrdManifestation.objects.get_or_create(
            title_slug=man_slug,
            work=frd_work
        )
        frd_man.tei_doc = doc.return_string()
        frd_man.drupal_hash = man_id
        frd_man.save_path = x
        frd_man.save()
        manifestations.append(frd_man)
    return manifestations
