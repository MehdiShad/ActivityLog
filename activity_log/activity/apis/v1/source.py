from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from activity_log.activity.models import Source
from activity_log.api.mixins import ApiAuthMixin
from activity_log.activity.selectors import source as source_selector
from activity_log.api.pagination import LimitOffsetPagination, get_paginated_response_context
from activity_log.common.services import error_response, handle_validation_error, success_response

class OutPutSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class CustomSourcesSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutSourcesSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomSourcesMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutSourcesSerializer())

    class Meta:
        fields = ('is_success', 'data')


class SourcesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class FilterSourcesSerializer(serializers.Serializer):
        test = serializers.CharField(required=False)

    @extend_schema(parameters=[FilterSourcesSerializer], responses=CustomSourcesMultiResponseSerializer,
                   tags=['Sources'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterSourcesSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            sources = source_selector.get_filtered_sources(filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutSourcesSerializer,
                queryset=sources,
                view=self,
            )

        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest):
        pass
