from django.db import models

class MonitoringLocation(models.Model):
  location_id = models.CharField(max_length=50)
  location_name = models.CharField(max_length=255)
  location_type = models.CharField(max_length=100)
  waterbody = models.CharField(max_length=255, null=True, blank=True)

  def __str__(self):
    return f"{self.location_name} ({self.location_id})"

class WaterQualityMeasurement(models.Model):
  location = models.ForeignKey(MonitoringLocation, on_delete=models.CASCADE)
  date = models.DateField()
  time = models.TimeField()
  depth = models.FloatField(null=True, blank=True)
  characteristic_name = models.CharField(max_length=100)
  result_value = models.FloatField(null=True, blank=True)
  result_unit = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.characteristic_name} at {self.location} on {self.date}"
