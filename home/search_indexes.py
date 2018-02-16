import datetime
from haystack import indexes
from .models import *

class AutorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre = indexes.CharField(model_attr='nombre', null=True)
    apellido = indexes.CharField(model_attr='apellido')

    def get_model(self):
        return Autor

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

class LibroIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    isbn = indexes.CharField(model_attr='isbn', null=True)
    autores = indexes.MultiValueField()

    def get_model(self):
        return Libro

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

    def prepare_autores(self, obj):
        return [p.pk for p in obj.autores.all()]

