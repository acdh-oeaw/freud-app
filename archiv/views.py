import requests
import asyncio


from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from archiv.models import FrdManifestation, FrdWork, FrdCollation
from archiv.utils import create_collations


async def collate_collation(request, pk):
    col_obj = FrdCollation.objects.get(id=pk)
    loop = asyncio.get_event_loop()
    loop.create_task(create_collations(col_obj))
    print("#########################")
    return HttpResponse("Die Kollationen werden im Hintergrund erstellt!")


class WorkDetailView(DetailView):

    model = FrdWork
    template_name = 'archiv/work_detail.html'


class CollationDetailView(DetailView):

    model = FrdCollation
    template_name = 'archiv/collation_detail.html'


class CollationCreateView(CreateView):

    model = FrdCollation
    fields = ['manifestation', 'work']
    template_name = 'archiv/collation_create.html'

    def get_initial(self):
        initial = super(CollationCreateView, self).get_initial()
        work_id = self.request.GET.get('work', None)
        initial['work'] = work_id
        initial['manifestation'] = [x.id for x in FrdManifestation.objects.filter(work=work_id)]
        return initial

    def get_form(self):
        work_id = self.request.GET.get('work', None)
        form = super(CollationCreateView, self).get_form()
        form.fields['manifestation'].queryset = FrdManifestation.objects.filter(work=work_id)
        form.fields['work'].disabled = True
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        return form


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
