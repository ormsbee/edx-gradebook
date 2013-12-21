from rest_framework.generics import (
    ListCreateAPIView,
)

from gradebook.submissions.models import Submission

# temporary -- we'll actually have to serialize it differently

# might move these things to api.py, and have rest.py call this
class SubmissionList(ListCreateAPIView):
    """
    Does this get autodoced?
    """
    model = Submission