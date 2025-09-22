from rest_framework import viewsets, permissions, status
from .models import RoadSegment, SpeedReading, Car, Passage, Sensor
from .serializers import RoadSegmentSerializer, SpeedReadingSerializer, PassageSerializer
from django.db.models import OuterRef, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from .permissions import HasSensorApiKey
from rest_framework.generics import ListAPIView, CreateAPIView
from django.utils import timezone
from datetime import timedelta


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite apenas leitura para utilizadores normais,
    escrita só para admins.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        intensity = self.request.query_params.get("intensity")

        if intensity:
            # Pega apenas no último reading de cada segmento
            filtered_segments = []
            for segment in queryset:
                last_reading = segment.readings.order_by("-timestamp").first()
                if last_reading:
                    if intensity == "elevada" and last_reading.intensity == "elevada":
                        filtered_segments.append(segment.id)
                    elif intensity == "média" and last_reading.intensity == "média":
                        filtered_segments.append(segment.id)
                    elif intensity == "baixa" and last_reading.intensity == "baixa":
                        filtered_segments.append(segment.id)

            queryset = queryset.filter(id__in=filtered_segments)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="intensity",
                description="Filtrar pela intensidade da última leitura (elevada, média, baixa)",
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Só a listagem de segmentos aceita ?intensity="" como filtro"""
        return super().list(request, *args, **kwargs)
'''
@extend_schema(
    parameters=[
        OpenApiParameter(name="intensity", description="Filtrar pela intensidade da última leitura (elevada, média, baixa)", required=False, type=str),
    ]
)
class RoadSegmentViewSet(viewsets.ModelViewSet):
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []  # vamos customizar via get_queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        intensity = self.request.query_params.get("intensity")

        if intensity:
            # filtrar pela última leitura associada
            queryset = queryset.filter(
                readings__intensity=intensity
            ).distinct()

        return queryset
        
        #if intensity:
            # Procura a última leitura para cada segmento
        #    latest_reading = SpeedReading.objects.filter(
        #        road_segment=OuterRef("pk")
        #    ).order_by("-timestamp")

        #    queryset = queryset.annotate(
        #        last_speed=Subquery(latest_reading.values("average_speed")[:1])
        #    ).filter(
        #        last_speed__isnull=False
        #    )

        #    if intensity == "elevada":
        #        queryset = queryset.filter(last_speed__lte=20)
        #    elif intensity == "média":
        #        queryset = queryset.filter(last_speed__gt=20, last_speed__lte=50)
        #    elif intensity == "baixa":
        #        queryset = queryset.filter(last_speed__gt=50)

        #return queryset   
'''
class SpeedReadingViewSet(viewsets.ModelViewSet):
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [IsAdminOrReadOnly]

class BulkPassageView(CreateAPIView):
    permission_classes = [HasSensorApiKey]
    serializer_class = PassageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        created_passages = []
        for item in data:
            car, _ = Car.objects.get_or_create(
                license_plate=item["car__license_plate"],
                defaults={"created_at": timezone.now()}
            )
            sensor = Sensor.objects.get(uuid=item["sensor__uuid"])
            passage = Passage.objects.create(
                road_segment_id=item["road_segment"],
                car=car,
                sensor=sensor,
                timestamp=item["timestamp"]
            )
            created_passages.append(passage)
        serializer = self.get_serializer(created_passages, many=True)
        return Response(serializer.data)
    
class PassageByCarView(ListAPIView):
    serializer_class = PassageSerializer

    def get_queryset(self):
        license_plate = self.request.query_params.get("license_plate")
        last_24h = timezone.now() - timedelta(hours=24)
        return Passage.objects.filter(
            car__license_plate=license_plate,
            timestamp__gte=last_24h
        ).select_related("road_segment", "sensor", "car")