from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.utils import add_postgis_srs
from django.contrib.auth.models import User

add_postgis_srs(102671)


class CpdBeats(models.Model):
    objectid = models.IntegerField()
    district = models.CharField(max_length=2)
    sector = models.CharField(max_length=1)
    beat = models.CharField(max_length=1)
    beat_num = models.CharField(max_length=4)
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    geom = models.PolygonField(srid=102671)
    objects = models.GeoManager()
    

# Auto-generated `LayerMapping` dictionary for CpdBeats model
cpdbeats_mapping = {
    'objectid' : 'OBJECTID',
    'district' : 'DISTRICT',
    'sector' : 'SECTOR',
    'beat' : 'BEAT',
    'beat_num' : 'BEAT_NUM',
    'shape_area' : 'SHAPE_AREA',
    'shape_len' : 'SHAPE_LEN',
    'geom' : 'POLYGON',
}
class BeatUser(models.Model):
    user = models.ForeignKey(User, unique=True)
    cpdBeatIntersection = models.ForeignKey(CpdBeats, blank=False, null = False)
    reportedIncidents = models.ManyToManyField("Incident")
    cellNum = models.CharField(max_length=16)
    def __unicode__(self):
        return self.user.username
    #User has an email class
class Incident(models.Model):
    objid = models.AutoField(primary_key=True)
    reportedBy = models.ForeignKey(BeatUser, blank=False, null=False)
    msg = models.CharField(max_length = 255)
    relatedIncidents = models.ManyToManyField("self")
    beatOccurence = models.ForeignKey(CpdBeats, blank = False, null = False)
    voteTotal = models.DecimalField(default=0, decimal_places=2, max_digits=5)

class SMS(models.Model):
    objid = models.AutoField(primary_key=True)
    smsto = models.CharField(max_length=16)
    smsfrom = models.CharField(max_length=16)
    body = models.CharField(max_length=160)
    time = models.DateTimeField()



