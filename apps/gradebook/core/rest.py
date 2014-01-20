from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from gradebook.core.models import Context


class ContextList(ListCreateAPIView):
    model = Context
    lookup_field = "external_id"
    paginate_by = None


class ContextDetail(RetrieveUpdateAPIView):
    model = Context
    lookup_field = "external_id"
