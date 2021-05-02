# FRD-APP

FRD-APP is a django-based web application for the administration of several processing needed to create XML/TEI documents from data stored in https://www.freud-edition.net


## internal cheet-sheet

## download manifestations of a work a TEI-Docs

* `download_work -w 7f1ce2ef-dc26-45e2-b90a-85d866403b1c -s media`
  * creates `media/werke/josef-popper-lynkeus-und-die-theorie-des-traumes`


same works with `manage.py`

`python manage.py download_work 7f1ce2ef-dc26-45e2-b90a-85d866403b1c 5a325f79-997b-435e-9e30-1637b4c0a152 0e8b07dc-123f-4554-8139-c7b15a75aaaf` 