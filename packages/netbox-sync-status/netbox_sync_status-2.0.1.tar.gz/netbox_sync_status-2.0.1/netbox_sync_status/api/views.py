from core.events import OBJECT_UPDATED
from dcim.models import Device
from django.apps import apps
from django.db.models import Prefetch, Q
from drf_spectacular.utils import extend_schema
from extras.events import enqueue_event
from netbox.api.metadata import ContentTypeMetadata
from netbox.api.viewsets import BaseViewSet, NetBoxModelViewSet
from netbox.context import events_queue
from rest_framework import mixins as drf_mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from netbox_sync_status.filtersets import SyncStatusFilterSet

from .. import models
from .serializers import (
    SyncStatusSerializer,
    SyncSystemDeviceStatusSerializer,
    SyncSystemSerializer,
)


class ObjectSyncView(APIView):
    queryset = models.SyncStatus.objects.all()
    serializer_class = None

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request, obj_type, pk, format=None):
        if not obj_type or "." not in obj_type:
            return Response(
                {"detail": "Invalid object type"}, status=status.HTTP_400_BAD_REQUEST
            )

        app_label, model_name = obj_type.split(".")
        self.queryset = apps.get_model(app_label, model_name).objects
        selected_objects = self.queryset.filter(
            pk=pk,
        )

        for obj in selected_objects:
            obj.snapshot()
            queue = events_queue.get()
            enqueue_event(queue, obj, request.user, request.id, OBJECT_UPDATED)
            events_queue.set(queue)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SyncStatusViewSet(
    drf_mixins.CreateModelMixin,
    drf_mixins.RetrieveModelMixin,
    drf_mixins.ListModelMixin,
    BaseViewSet,
):
    metadata_class = ContentTypeMetadata
    queryset = models.SyncStatus.objects.all()
    serializer_class = SyncStatusSerializer
    filterset_class = SyncStatusFilterSet


class SyncSystemViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = models.SyncSystem.objects.all()
    serializer_class = SyncSystemSerializer

    @extend_schema(responses=SyncSystemDeviceStatusSerializer(many=True), request=None)
    @action(
        detail=True,
        methods=["get"],
        url_path="sync-status",
        renderer_classes=[JSONRenderer],
    )
    def render_system_sync_status(self, request, pk):
        """
        Resolve and render the sync status of all devices
        """
        system = self.get_object()
        devices = Device.objects.prefetch_related(
            Prefetch(
                "sync_status",
                queryset=models.SyncStatus.objects.filter(
                    Q(system__id=system.id) & Q(is_latest=True)
                ),
                to_attr="sync_events",
            )
        ).all()

        results = []
        for device in devices:
            if len(device.sync_events) > 0:
                results.append(
                    {"device_name": device.name, "status": device.sync_events[0].status}
                )
            else:
                results.append({"device_name": device.name, "status": "not-started"})

        return Response(results)
