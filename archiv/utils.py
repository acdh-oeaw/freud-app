from archiv.models import FrdWork


def get_or_create_werk(drupal_work):
    frd_work, _ = FrdWork.objects.get_or_create(
        title_slug=drupal_work.md__path__alias.split('/')[-1],
        drupal_hash=drupal_work.werk_id,
    )
    frd_work.drupal_json = drupal_work.werk
    frd_work.save()
    return frd_work
