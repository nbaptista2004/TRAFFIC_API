from rest_framework import serializers
from .models import RoadSegment, Sensor, SpeedReading, Car, Passage

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'uuid']

class RoadSegmentSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer(read_only=True)
    total_readings = serializers.SerializerMethodField()

    class Meta:
        model = RoadSegment
        fields = [
            'id',
            'long_start',
            'lat_start',
            'long_end',
            'lat_end',
            'length',
            'speed',
            'sensor',
            'total_readings',
        ]

    def get_total_readings(self, obj):
        return obj.readings.count()

class SpeedReadingSerializer(serializers.ModelSerializer):
    road_segment = RoadSegmentSerializer(read_only=True)

    class Meta:
        model = SpeedReading
        fields = ['id', 'road_segment', 'average_speed', 'timestamp', 'intensity']

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "license_plate", "created_at"]

class PassageSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    sensor = SensorSerializer()
    road_segment = RoadSegmentSerializer()

    class Meta:
        model = Passage
        fields = ["id", "car", "road_segment", "sensor", "timestamp"]





