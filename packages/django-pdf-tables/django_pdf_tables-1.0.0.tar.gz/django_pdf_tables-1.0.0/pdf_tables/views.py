from django.views.generic import View

from pdf_tables.mixins import PDFMixin, PDFTablesMixin


class PDFView(PDFMixin, View):
    def dispatch(self, request, *args, **kwargs):
        return self.render()


class PDFTableView(PDFTablesMixin, PDFView):
    pass
