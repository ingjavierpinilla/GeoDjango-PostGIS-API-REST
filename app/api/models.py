from datetime import datetime, timezone
from django.db import models
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations
from django.contrib.gis.db import models as gis_models

class Dataset(models.Model):
    name = models.CharField(max_length = 95, blank = False)
    date = models.DateTimeField(default = datetime.now(timezone.utc), blank = False)

    def __str__(self):
        return f'{self.id} {self.name}'

class Row(models.Model):
    dataset_id = models.ForeignKey(Dataset, related_name='rows', on_delete = models.CASCADE)
    point = gis_models.PointField(srid = 4326, blank = False)
    client_id = models.PositiveIntegerField(blank = False)
    client_name = models.CharField(max_length = 45, blank = False)

    def __str__(self):
        return f'{self.dataset_id} {self.point}'
