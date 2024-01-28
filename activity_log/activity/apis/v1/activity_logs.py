from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from activity_log.api.mixins import ApiAuthMixin
from activity_log.activity.models import ActivityLog
from activity_log.activity.selectors import activity_logs as activity_logs_selector
from activity_log.api.pagination import LimitOffsetPagination, get_paginated_response_context
from activity_log.common.services import error_response, handle_validation_error, success_response


class OutPutActivityLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'


class CustomActivityLogsSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutActivityLogsSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomActivityLogsMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutActivityLogsSerializer())

    class Meta:
        fields = ('is_success', 'data')


class ActivityLogsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class FilterActivityLogsSerializer(serializers.Serializer):
        is_holiday = serializers.BooleanField(required=False)

    @extend_schema(parameters=[FilterActivityLogsSerializer], responses=CustomActivityLogsMultiResponseSerializer,
                   tags=['ActivityLogs'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterActivityLogsSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            activity_logs = activity_logs_selector.get_filtered_activity_log(filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutActivityLogsSerializer,
                queryset=activity_logs,
                view=self,
            )

        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request: HttpRequest):
    #     pass


class ActivityLogApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 25

    def get(self, request: HttpRequest, activity_log_id: int):
        pass

    def put(self, request: HttpRequest, activity_log_id: int):
        pass
