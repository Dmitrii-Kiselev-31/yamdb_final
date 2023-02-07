from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import IntegerField, ModelSerializer
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comments, Genre, Review, Title, User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()), ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if 'me' == value.lower():
            raise serializers.ValidationError(
                'Нельзя использовать имя me'
            )
        if value == '':
            raise serializers.ValidationError(
                'Обязательное поле'
            )
        return value

    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError(
                'Почта обязательна для заполнения'
            )
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role',
            'first_name', 'last_name'
        )
        lookup_field = 'username'

        def __str__(self):
            return self.username


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role',
            'first_name', 'last_name'
        )
        read_only_fields = ('role',)


class TokenCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(ModelSerializer):
    id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

    def __str__(self):
        return self.name, self.slug


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class TitleSerializer(ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')


class TitleReadSerializer(ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField(read_only=True, required=False, default=None)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'category',
            'genre',
            'description',
            'year',
            'rating'
        )
        read_only_fields = ("name", "year", "description",
                            "genre", "category", 'rating')

    def __str__(self):
        return self.name


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='id')

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                'Возможен один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        validators=[UniqueValidator(queryset=Comments.objects.all())]
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
