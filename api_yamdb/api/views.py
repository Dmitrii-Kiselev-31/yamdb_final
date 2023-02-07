from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User

from api.permissions import (AdminUserOrReadOnly, AuthorAdminReadOnly,
                             CommentReviewPermission, IsAdminOrSuperuser)
from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleReadSerializer,
                          TitleSerializer, TokenCodeSerializer,
                          UserMeSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperuser, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('username', )
    lookup_field = 'username'

    @action(
        detail=False, methods=['GET', 'PATCH'], url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = UserMeSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    sending_email = settings.EMAIL
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Ваш код: {confirmation_code}'
    send_mail(
        user,
        message,
        sending_email,
        [email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer_class = TokenCodeSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if user.confirmation_code != confirmation_code:
        return Response('Код подтверждения неверный',
                        status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(user)
    return Response({
        'token': str(token),
        'access': str(token.access_token),
    },
        status=status.HTTP_200_OK)


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, GenericViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AuthorAdminReadOnly, ]
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminUserOrReadOnly, ]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    permission_classes = [AdminUserOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [CommentReviewPermission, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentReviewPermission, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            title.reviews, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
