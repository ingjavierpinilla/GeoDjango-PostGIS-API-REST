from datetime import datetime, timezone
from django.db import models, migrations
from django.contrib.postgres.operations import CreateExtension
from django.utils.text import slugify
from django.contrib.gis.db import models as gis_models

class Dataset(models.Model):
    name = models.CharField(max_length = 95, blank = False)
    date = models.DateTimeField(default = datetime.now(timezone.utc), blank = False)
    slug = models.SlugField(max_length = 95, blank = True , null = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Dataset, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} {self.slug}'

class Row(models.Model):
    dataset_id = models.ForeignKey(Dataset, related_name='rows', on_delete = models.CASCADE)
    point = gis_models.PointField(srid = 4326, blank = False)
    client_id = models.PositiveIntegerField(blank = False)
    client_name = models.CharField(max_length = 45, blank = False)

    def __str__(self):
        return f'{self.dataset_id} {self.point}'
