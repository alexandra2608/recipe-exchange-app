from datetime import timedelta

from django.db.models import Count, Avg
from django.utils.timezone import now
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import User, Recipe, Tag, RecipeTag, Comment, SavedRecipe, Subscription, Rating
from .serializers import (
    UserSerializer, RecipeSerializer, TagSerializer, RecipeTagSerializer,
    CommentSerializer, SavedRecipeSerializer, SubscriptionSerializer, RatingSerializer, UserWithCommentsSerializer,
    RecipeWithMetricsSerializer, SaveRecipeSerializer
)


# User Views
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Recipe Views
class RecipeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        print(f"User from request: {self.request.user}")
        print(f"Is authenticated: {self.request.user.is_authenticated}")
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Получаем параметры фильтрации из запроса
        title = self.request.query_params.get('title')
        complexity = self.request.query_params.get('complexity')
        tag_id = self.request.query_params.get('tag_id')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if complexity:
            queryset = queryset.filter(complexity=complexity)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset



class RecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecentRecipesAPIView(generics.ListAPIView):
    """
    List recipes added in the last 7 days.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        seven_days_ago = now() - timedelta(days=7)
        return Recipe.objects.filter(created_at__gte=seven_days_ago)


# Tag Views
class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# RecipeTag Views
class RecipeTagListCreateAPIView(generics.ListCreateAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer


class RecipeTagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer


# Comment Views
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# SavedRecipe Views
class SavedRecipeListCreateAPIView(generics.ListCreateAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SavedRecipeSerializer

class SaveRecipeListCreateAPIView(generics.ListCreateAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SaveRecipeSerializer

class SaveRecipeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedRecipe.objects.all()
    serializer_class = SaveRecipeSerializer


# Subscription Views
class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


# Rating Views
class RatingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class RatingRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


# Analytical
class UserRecipesAPIView(generics.ListAPIView):
    """
    Get all recipes created by a specific user
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Recipe.objects.filter(author_id=user_id)


class UserCommentsAPIView(generics.ListAPIView):
    """
    Get all comments written by a specific user
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Comment.objects.filter(user_id=user_id)


class UserSavedRecipesAPIView(generics.ListAPIView):
    """
    Get all saved recipes for a specific user
    """
    serializer_class = SavedRecipeSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return SavedRecipe.objects.filter(user_id=user_id)


class UserSubscriptionsAPIView(generics.ListAPIView):
    """
    Get all subscriptions for a specific user
    """
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Subscription.objects.filter(subscriber_id=user_id)


class UserSubscribersAPIView(generics.ListAPIView):
    """
    Get the number of subscribers for a specific user
    """
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        subscriber_count = Subscription.objects.filter(chef_id=user_id).count()
        return Response({"subscriber_count": subscriber_count}, status=status.HTTP_200_OK)


class UserRatingsAPIView(generics.ListAPIView):
    """
    Get all ratings given to a user's recipes
    """
    serializer_class = RatingSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Rating.objects.filter(recipe__author_id=user_id)


class RecipesByTagAPIView(generics.ListAPIView):
    """
    Get all recipes by a specific tag
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        tag_id = self.kwargs['tag_id']
        return Recipe.objects.filter(tags__id=tag_id)


class CommentsByRecipeAPIView(generics.ListAPIView):
    """
    Get all comments written to a specific recipe
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        recipe_id = self.kwargs['recipe_id']
        return Comment.objects.filter(recipe__id=recipe_id)


class RatingsByRecipeAPIView(generics.ListAPIView):
    """
    Get all ratings to specific recipe
    """

    serializer_class = RatingSerializer

    def get_queryset(self):
        recipe_id = self.kwargs['recipe_id']
        return Rating.objects.filter(recipe__id=recipe_id)


class RecipeByCommentAPIView(generics.RetrieveAPIView):
    """
    Get recipe by a comment
    """

    serializer_class = RecipeSerializer

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        comment = Comment.objects.get(id=comment_id)
        return comment.recipe


class UserWithCommentsAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithCommentsSerializer


class RecipeMetricsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.annotate(
            comment_count=Count('comments'),
            average_rating=Avg('ratings__rating_value'),
            user_rating_count=Count('ratings__user', distinct=True)
        )

        serializer = RecipeWithMetricsSerializer(recipes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeWithRatingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.annotate(
            comment_count=Count('comments'),
            average_rating=Avg('ratings__rating_value'),
            user_rating_count=Count('ratings__user', distinct=True)
        ).filter(average_rating__gt=8)  # Фильтруем рецепты с рейтингом выше 8

        # Сериализация данных
        serializer = RecipeWithMetricsSerializer(recipes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
