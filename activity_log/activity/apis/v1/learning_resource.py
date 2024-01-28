from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from activity_log.api.mixins import ApiAuthMixin
from activity_log.activity.models import LearningResource
from activity_log.activity.selectors import learning_resource as learning_resource_selector
from activity_log.api.pagination import LimitOffsetPagination, get_paginated_response_context
from activity_log.common.services import error_response, handle_validation_error, success_response


class OutPutLearningResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = '__all__'


class CustomLearningResourcesSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutLearningResourcesSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomLearningResourcesMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutLearningResourcesSerializer())

    class Meta:
        fields = ('is_success', 'data')


class LearningResourcesApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class FilterLearningResourcesSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)

    @extend_schema(parameters=[FilterLearningResourcesSerializer],
                   responses=CustomLearningResourcesMultiResponseSerializer,
                   tags=['LearningResources'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterLearningResourcesSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            learning_resources = learning_resource_selector.get_filtered_learning_resources(
                filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutLearningResourcesSerializer,
                queryset=learning_resources,
                view=self,
            )

        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest):
        pass
