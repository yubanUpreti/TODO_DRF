from django.db import transaction

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from ..serializer.signupSerializer import RegisterSerializer


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            transaction.savepoint_commit(sid)
        except Exception as error:
            transaction.savepoint_rollback(sid)
            return Response({
                'message': "Signup Failed.",
                'error': str(error)}, status=HTTP_400_BAD_REQUEST)

        return Response({'message': "User successfully created."}, status=HTTP_201_CREATED)
