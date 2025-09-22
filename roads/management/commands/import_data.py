import csv
from django.core.management.base import BaseCommand
from roads.models import Sensor, RoadSegment

class Command(BaseCommand):
    help = "Importa dados dos ficheiros sensors.csv e traffic_speed.csv"

    def handle(self, *args, **options):
        # Importar sensores
        with open("sensors.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Sensor.objects.get_or_create(
                    id=row["id"],
                    defaults={
                        "name": row["name"],
                        "uuid": row["uuid"]
                    }
                )
        self.stdout.write(self.style.SUCCESS("Sensores importados!"))

        # Importar segmentos
        with open("traffic_speed.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                RoadSegment.objects.create(
                    id=row["ID"],
                    long_start=row["Long_start"],
                    lat_start=row["Lat_start"],
                    long_end=row["Long_end"],
                    lat_end=row["Lat_end"],
                    length=row["Length"],
                    speed=row["Speed"]
                )
        self.stdout.write(self.style.SUCCESS("Segmentos importados!"))
