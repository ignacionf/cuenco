import datetime
from haystack import indexes
from .models import *

class AutorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre = indexes.CharField(model_attr='nombre', null=True, boost=1.125)
    apellido = indexes.CharField(model_attr='apellido', boost=2)

    def prepare(self, obj):
        data = super(AutorIndex, self).prepare(obj)
        data['boost'] = 5
        return data

    def get_model(self):
        return Autor

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class LibroIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo', boost=2)
    isbn = indexes.CharField(model_attr='isbn', null=True, boost=10)
    autores = indexes.MultiValueField()
    fecha = indexes.DateField(model_attr='fecha', null=True)

    def get_model(self):
        return Libro

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_autores(self, obj):
        return [p.pk for p in obj.autores.all()]

class NotaIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo', boost=1.125)
    libro = indexes.CharField(model_attr='libro', null=True)

    def get_model(self):
        return Nota

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(publicado=True)
