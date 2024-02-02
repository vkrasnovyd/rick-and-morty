from random import choice

from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer
from pagination import CharacterListPagination


@extend_schema(
    responses={200: CharacterSerializer},
)
@api_view(["GET"])
def get_random_character_view(request) -> Response:
    """Get random character from Rick & Morty world."""
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    random_character = Character.objects.get(pk=random_pk)
    serializer = CharacterSerializer(random_character)

    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    """List of characters with filter by name."""

    serializer_class = CharacterSerializer
    pagination_class = CharacterListPagination

    def get_queryset(self) -> QuerySet:
        queryset = Character.objects.all()

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name case insensitive contains (ex. name=bob)",
                required=False,
                type=str,
            )
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)
