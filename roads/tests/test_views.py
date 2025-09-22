from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from roads.models import RoadSegment, SpeedReading, Sensor
from django.utils import timezone


class RoadSegmentFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sensor = Sensor.objects.create(name="Sensor 1", uuid="11111111-1111-1111-1111-111111111111")

        # Segmento 1 -> última leitura elevada
        self.segment1 = RoadSegment.objects.create(
            long_start=0, lat_start=0, long_end=1, lat_end=1, length=100, speed=10, sensor=self.sensor
        )
        SpeedReading.objects.create(road_segment=self.segment1, average_speed=15, timestamp=timezone.now())

        # Segmento 2 -> última leitura média
        self.segment2 = RoadSegment.objects.create(
            long_start=2, lat_start=2, long_end=3, lat_end=3, length=200, speed=40, sensor=self.sensor
        )
        SpeedReading.objects.create(road_segment=self.segment2, average_speed=35, timestamp=timezone.now())

        # Segmento 3 -> última leitura baixa
        self.segment3 = RoadSegment.objects.create(
            long_start=4, lat_start=4, long_end=5, lat_end=5, length=300, speed=80, sensor=self.sensor
        )
        SpeedReading.objects.create(road_segment=self.segment3, average_speed=70, timestamp=timezone.now())

    def test_filter_elevada(self):
        response = self.client.get(reverse("roadsegment-list"), {"intensity": "elevada"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.segment1.id)

    def test_filter_media(self):
        response = self.client.get(reverse("roadsegment-list"), {"intensity": "média"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.segment2.id)

    def test_filter_baixa(self):
        response = self.client.get(reverse("roadsegment-list"), {"intensity": "baixa"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.segment3.id)

    def test_no_filter_returns_all(self):
        response = self.client.get(reverse("roadsegment-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
