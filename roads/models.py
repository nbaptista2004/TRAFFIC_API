from django.db import models
from django.utils import timezone


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(unique=True)

    def __str__(self):
        return self.name
    
class RoadSegment(models.Model):
    long_start = models.FloatField()
    lat_start = models.FloatField()
    long_end = models.FloatField()
    lat_end = models.FloatField()
    length = models.FloatField()
    speed = models.FloatField()
    sensor = models.ForeignKey(Sensor, related_name="segments", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Segmento {self.id} ({self.speed} km/h)"


class SpeedReading(models.Model):
    road_segment = models.ForeignKey(RoadSegment, related_name="readings", on_delete=models.CASCADE)
    average_speed = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    @property
    def intensity(self):
        if self.average_speed <= 20:
            return "elevada"
        elif self.average_speed <= 50:
            return "média"
        return "baixa"

    def __str__(self):
        return f"{self.road_segment.name} - {self.average_speed} km/h"

class Car(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.license_plate


class Passage(models.Model):
    road_segment = models.ForeignKey("roads.RoadSegment", on_delete=models.CASCADE, related_name="passages")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="passages")
    timestamp = models.DateTimeField()
    sensor = models.ForeignKey("roads.Sensor", on_delete=models.CASCADE, related_name="passages")

    def __str__(self):
        return f"{self.car.license_plate} @ {self.road_segment.id} ({self.timestamp})"