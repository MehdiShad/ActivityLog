from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from activity_log.activity.models import Item
from activity_log.api.mixins import ApiAuthMixin
from activity_log.activity.selectors import item as item_selector
from activity_log.api.pagination import LimitOffsetPagination, get_paginated_response_context
from activity_log.common.services import error_response, handle_validation_error, success_response


class OutPutItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CustomItemsSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutItemsSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomItemsMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutItemsSerializer())

    class Meta:
        fields = ('is_success', 'data')


class ItemsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class FilterItemsSerializer(serializers.Serializer):
        fa_title = serializers.CharField(required=False)
        en_title = serializers.CharField(required=False)
        content_type = serializers.CharField(required=False)

    @extend_schema(parameters=[FilterItemsSerializer], responses=CustomItemsMultiResponseSerializer,
                   tags=['Items'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterItemsSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            items = item_selector.get_filtered_items(filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutItemsSerializer,
                queryset=items,
                view=self,
            )

        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest):
        pass
