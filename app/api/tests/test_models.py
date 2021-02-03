from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models import Dataset, Row
from django.contrib.gis.geos import Point

class TestModels(TestCase):

    def setUp(self):
        self.dataset1 = Dataset.objects.create(
            name = 'Dataset 1'
        )

    def test_dataset_slug_name(self):
        self.assertEquals(self.dataset1.slug, 'dataset-1')

    def test_row_creation_without_dataset_fk(self):
        self.assertRaises(ValueError, Row, dataset_id = 1)

    def test_row_on_ds_delete(self):
        ds2 = Dataset.objects.create(
            name = 'Dataset 2'
        )
        row = Row.objects.create(
            dataset_id = ds2,
            point = Point(0.123,1.12302),
            client_id = 1,
            client_name = 'test'
        ) 
        Dataset.objects.filter(id = ds2.id).delete()
        row = Row.objects.filter(id = row.id)
        self.assertFalse(isinstance(row, Row))
