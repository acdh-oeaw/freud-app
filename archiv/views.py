import requests
from django.views.generic.base import TemplateView

from archiv.models import FrdWork


class HomePageView(TemplateView):

    template_name = "archiv/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['works'] = FrdWork.objects.all()
        return context


class ImprintView(TemplateView):
    template_name = 'archiv/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        r = requests.get("https://shared.acdh.oeaw.ac.at/acdh-common-assets/api/imprint.php?serviceID=19058")

        if r.status_code == 200:
            context['imprint_body'] = f"{r.text}"
        else:
            context['imprint_body'] = """
            On of our services is currently not available. Please try it later or write an email to
            acdh@oeaw.ac.at
            """
        return context