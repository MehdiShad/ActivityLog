from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema
from activity_log.activity.models import Topic
from activity_log.api.mixins import ApiAuthMixin
from activity_log.api.pagination import LimitOffsetPagination, get_paginated_response_context
from activity_log.common.services import error_response, handle_validation_error, success_response
from activity_log.activity.selectors import topic as topic_selector

class OutPutTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class CustomTopicsSingleResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    data = OutPutTopicsSerializer()

    class Meta:
        fields = ('is_success', 'data')


class CustomTopicsMultiResponseSerializer(serializers.Serializer):
    is_success = serializers.BooleanField(default=True)
    limit = serializers.IntegerField()
    offset = serializers.IntegerField()
    count = serializers.IntegerField()
    next = serializers.CharField()
    previous = serializers.CharField()
    data = serializers.ListSerializer(child=OutPutTopicsSerializer())

    class Meta:
        fields = ('is_success', 'data')


class TopicsApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 25

    class FilterTopicsSerializer(serializers.Serializer):
        test = serializers.CharField(required=False)

    @extend_schema(parameters=[FilterTopicsSerializer], responses=CustomTopicsMultiResponseSerializer,
                   tags=['Topics'])
    def get(self, request: HttpRequest):
        filter_serializer = self.FilterTopicsSerializer(data=request.query_params)
        validation_result = handle_validation_error(serializer=filter_serializer)
        if not isinstance(validation_result, bool):  # if validation_result response is not boolean
            return Response(validation_result, status=status.HTTP_400_BAD_REQUEST)

        try:
            topics = topic_selector.get_filtered_topics(filters=filter_serializer.validated_data)
            return get_paginated_response_context(
                request=request,
                pagination_class=self.Pagination,
                serializer_class=OutPutTopicsSerializer,
                queryset=topics,
                view=self,
            )

        except Exception as ex:
            response = error_response(message=str(ex))
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: HttpRequest):
        pass
