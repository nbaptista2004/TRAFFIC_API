from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from roads.models import RoadSegment, SpeedReading, Sensor
from django.utils import timezone
import datetime


class RoadSegmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="normaluser", password="12345")
        self.admin = User.objects.create_superuser(username="admin", password="12345")

        self.sensor = Sensor.objects.create(
            name="Test Sensor",
            uuid="11111111-1111-1111-1111-111111111111"
        )

        self.segment = RoadSegment.objects.create(
            long_start=10.0,
            lat_start=20.0,
            long_end=11.0,
            lat_end=21.0,
            length=1000,
            speed=50,
            sensor=self.sensor
        )

    def test_list_segments(self):
        """Qualquer utilizador deve conseguir listar segmentos"""
        response = self.client.get("/api/segments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_segment_permission_denied(self):
        """Utilizador normal não pode criar segmentos"""
        self.client.login(username="normaluser", password="12345")
        response = self.client.post("/api/segments/", {
            "long_start": 1.0,
            "lat_start": 1.0,
            "long_end": 2.0,
            "lat_end": 2.0,
            "length": 500,
            "speed": 40,
            "sensor": self.sensor.id
        })
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_segment(self):
        """Admin pode criar segmentos"""
        self.client.login(username="admin", password="12345")
        response = self.client.post("/api/segments/", {
            "long_start": 1.0,
            "lat_start": 1.0,
            "long_end": 2.0,
            "lat_end": 2.0,
            "length": 500,
            "speed": 40,
            "sensor": self.sensor.id
        })
        self.assertEqual(response.status_code, 201)


class SpeedReadingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.segment = RoadSegment.objects.create(
            long_start=10.0,
            lat_start=20.0,
            long_end=11.0,
            lat_end=21.0,
            length=1000,
            speed=50
        )
        self.reading = SpeedReading.objects.create(
            road_segment=self.segment,
            average_speed=30.0
        )

    def test_list_readings(self):
        """Qualquer utilizador deve conseguir listar leituras"""
        response = self.client.get("/api/readings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


class RoadSegmentFilterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.segment1 = RoadSegment.objects.create(
            long_start=10.0, lat_start=20.0,
            long_end=11.0, lat_end=21.0,
            length=1000, speed=50
        )
        self.segment2 = RoadSegment.objects.create(
            long_start=12.0, lat_start=22.0,
            long_end=13.0, lat_end=23.0,
            length=800, speed=40
        )

        # Leituras diferentes
        SpeedReading.objects.create(
            road_segment=self.segment1,
            average_speed=10.0,   # intensidade = elevada
            timestamp=timezone.now()
        )
        SpeedReading.objects.create(
            road_segment=self.segment2,
            average_speed=55.0,   # intensidade = baixa
            timestamp=timezone.now()
        )

    def test_filter_by_intensity_elevada(self):
        response = self.client.get("/api/segments/?intensity=elevada")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.segment1.id)

    def test_filter_by_intensity_baixa(self):
        response = self.client.get("/api/segments/?intensity=baixa")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.segment2.id)
        
