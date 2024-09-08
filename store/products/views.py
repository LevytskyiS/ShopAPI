from typing import Union
import copy
import logging

from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .utils import (
    parse_json_data,
    model_serializers_mapping,
    filter_models,
    get_deserialized_object,
)

logger = logging.getLogger(__name__)


class ImportAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def post(self, request, format="json") -> Response:
        logger.info(f"INFO: Sent POST request -- USER: {request.user}")
        saved_models, invalid_data = [], []
        json_data = request.data

        if not json_data:
            return Response(
                {"error": "No data were provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        parsed_data: list = parse_json_data(json_data)

        for data in parsed_data:
            if data:
                for key, values in data.items():
                    serializer_model = model_serializers_mapping.get(key)

                    for value in values:
                        serializer = serializer_model(data=value)

                        if not serializer.is_valid(raise_exception=True):
                            object_data = {key: value}
                            object_data["error"] = serializer.errors
                            invalid_data.append(data)
                            continue

                        try:
                            serializer.save()
                        except IntegrityError as e:
                            error_data = copy.deepcopy(data)
                            error_data["error"] = str(e)
                            invalid_data.append(error_data)
                            continue

                        save_obj = copy.deepcopy(data)
                        save_obj[key] = serializer.data
                        saved_models.append(save_obj)

        return Response(
            {
                "received": {
                    "created_or_updated": saved_models,
                    "invalid_data": invalid_data,
                }
            },
            status=status.HTTP_200_OK,
        )


class ModelListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """Accept GET request and return objects by model name."""

    def get(self, request: HttpRequest, model_name: str) -> Response:
        logger.info(f"GET REQUEST from {request.user}")
        result: Union[QuerySet, Response] = filter_models(model_name)

        if isinstance(result, Response):
            return result

        if not result:
            return Response(
                {"result": f"No objects found for model '{model_name}'"}, status=404
            )

        data = [get_deserialized_object(obj) for obj in result]
        logger.info(f"RETURN GET REQUEST to {request.user}")
        return Response(data, status=status.HTTP_200_OK)


class ModelDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    """Accept GET request and return product details by it's model name and id."""

    def get(
        self, request: HttpRequest, model_name: str, pk: int, format="json"
    ) -> Response:
        logger.info(f"GET REQUEST from {request.user}")
        result: Union[QuerySet, Response] = filter_models(model_name)

        if isinstance(result, Response):
            return result

        object_class = result.first().__class__
        model = get_object_or_404(object_class, id=pk)

        serialized_model: ReturnDict = get_deserialized_object(model)
        logger.info(f"RETURN GET REQUEST to {request.user}")
        return Response(serialized_model)
