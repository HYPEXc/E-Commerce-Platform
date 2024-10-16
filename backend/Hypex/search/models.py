from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class SearchListView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        from . import client
        query = request.GET.get('q')
        tags = request.GET.get('tags') or None
        if not query:
            return Response({'error': 'Please enter a search query'}, status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query, tags=tags)
        return Response(results)
