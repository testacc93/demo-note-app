from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Note
from .serializers import UserSerializer, LoginSerializer, NoteSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
import jwt
import datetime
from rest_framework.exceptions import AuthenticationFailed, NotFound


class UserAPIView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid Data",
        },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            status.HTTP_200_OK: UserSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid Data",
        },
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                payload = {
                    "email": user.email,
                    "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
                }
                token = jwt.encode(payload=payload, key="secret_key", algorithm="HS256")
                return Response({"token": token})
            else:
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"error": "No user exists with that email"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class NoteListCreateAPIView(APIView):
    def get(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        # user = User.objects.filter(user_id=request.data['user']).first()

        if not token:
            raise AuthenticationFailed("You need to be authenticaed")
        try:
            payload = jwt.decode(token, key="secret_key", algorithms="HS256")
            email = payload["email"]
            user = User.objects.filter(email=email).first()
            notes = Note.objects.filter(user=user)

        except:
            pass

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=NoteSerializer,
        responses={
            status.HTTP_201_CREATED: NoteSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid Data",
        },
    )
    def post(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise AuthenticationFailed("You need to be authenticaed")
        try:
            payload = jwt.decode(token, key="secret_key", algorithms="HS256")
            email = payload["email"]
            user = User.objects.filter(email=email).first()
            request.data["user"] = int(user.id)
            if not user:
                raise NotFound("User not found")
        except Exception as e:
            pass
        try:
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteGetPutAPIView(APIView):

    def get(self, request, notes_id):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise AuthenticationFailed("You need to be authenticaed")
        try:
            note = Note.objects.get(note_id=notes_id)
        except:
            return Response(
                {
                    "message": "No note exist with that id or you may not have the permission to perform this action"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serialzier = NoteSerializer(instance=note)
        return Response(serialzier.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=NoteSerializer,
        responses={
            status.HTTP_202_ACCEPTED: NoteSerializer(),
            status.HTTP_400_BAD_REQUEST: "Invalid Data",
        },
    )
    def put(self, request, notes_id):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise AuthenticationFailed("You need to be authenticated")
        payload = jwt.decode(token, key="secret_key", algorithms="HS256")
        email = payload["email"]
        user = User.objects.filter(email=email).first()
        note = Note.objects.filter(user_id=user.id, note_id=notes_id).first()
        if not note:
            raise NotFound(
                "No note exist with that id or you may not have the permission to perform this action"
            )

        serializer = NoteSerializer(instance=note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, notes_id):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            raise AuthenticationFailed("You need to be authenticated")
        payload = jwt.decode(token, key="secret_key", algorithms="HS256")
        email = payload["email"]
        user = User.objects.filter(email=email).first()
        note = Note.objects.filter(user_id=user.id, note_id=notes_id).first()
        if not note:
            raise NotFound(
                "No note exist with that id or you may not have the permission to perform this action"
            )

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)