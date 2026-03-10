from rest_framework import serializers
from .models import User, Recipe, Tag, RecipeTag, Comment, SavedRecipe, Subscription, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'date_joined', 'profile_image']
        ref_name = 'CustomUserSerializer'


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'instructions',
            'complexity', 'author', 'image',
            'video', 'tags'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        RecipeTag.objects.bulk_create([
            RecipeTag(recipe=recipe, tag=tag) for tag in tags
        ])
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)

        # Удаляем старые связи через промежуточную модель RecipeTag
        RecipeTag.objects.filter(recipe=instance).delete()

        # Добавляем новые теги
        RecipeTag.objects.bulk_create([
            RecipeTag(recipe=instance, tag=tag) for tag in tags
        ])

        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = ['id', 'recipe', 'tag']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'user', 'content', 'created_at']


class SavedRecipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = SavedRecipe
        fields = ['id', 'user', 'recipe']


class SaveRecipeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = SavedRecipe
        fields = ['id', 'user', 'recipe']

class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    chef = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Subscription
        fields = ['id', 'subscriber', 'chef']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'user', 'rating_value']


class UserWithCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'date_joined', 'comments']


class RecipeWithMetricsSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    user_rating_count = serializers.IntegerField()
    author_name = serializers.CharField(source='author.username')

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'complexity', 'author_name', 'image', 'video', 'created_at', 'comment_count', 'average_rating', 'user_rating_count']
