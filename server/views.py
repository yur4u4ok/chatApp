from django.db.models import Count
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


class ServerListViewSet(ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get('by_user') == 'true'
        by_serverid = request.query_params.get('by_serverid')
        with_num_members = request.query_params.get("with_num_members") == 'true'

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with {by_serverid} id not found")
            except ValueError:
                raise ValidationError(detail="Server value error")

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

        if qty:
            self.queryset = self.queryset[:int(qty)]

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})

        return Response(serializer.data)
