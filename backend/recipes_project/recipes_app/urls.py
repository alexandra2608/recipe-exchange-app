from django.conf.urls.static import static
from django.urls import path, include
from .views import *
from django.conf import settings
app_name = "recipes_app"

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # User
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('users/<int:user_id>/subscriptions/', UserSubscriptionsAPIView.as_view(), name='user-subscriptions'),
    path('users/<int:user_id>/subscribers/', UserSubscribersAPIView.as_view(), name='user-subscribers'),
    path('users/<int:user_id>/recipes/', UserRecipesAPIView.as_view(), name='user-recipes'),
    path('users/<int:user_id>/saved-recipes/', UserSavedRecipesAPIView.as_view(), name='user-saved-recipes'),

    path('users/<int:user_id>/comments/', UserCommentsAPIView.as_view(), name='user-comments'),
    path('users/<int:user_id>/ratings/', UserRatingsAPIView.as_view(), name='user-ratings'),
    path('users-with-comments/', UserWithCommentsAPIView.as_view(), name='users-with-comments'),

    # Recipe
    path('recipes/', RecipeListCreateAPIView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', RecipeRetrieveUpdateDestroyAPIView.as_view(), name='recipe-detail'),
    path('recipes/by-tag/<int:tag_id>/', RecipesByTagAPIView.as_view(), name='recipes-by-tag'),
    path('recipes/by-comment/<int:comment_id>/', RecipeByCommentAPIView.as_view(), name='recipe-by-comment'),
    path('recipes/metrics/', RecipeMetricsAPIView.as_view(), name='recipe-metrics'),
    path('recipes/recent/', RecentRecipesAPIView.as_view(), name='recent-recipes'),
    path('recipes/high-rating/', RecipeWithRatingAPIView.as_view(), name='recipes-high-rating'),

    # Tag
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagRetrieveUpdateDestroyAPIView.as_view(), name='tag-detail'),

    # RecipeTag
    path('recipe-tags/', RecipeTagListCreateAPIView.as_view(), name='recipetag-list-create'),
    path('recipe-tags/<int:pk>/', RecipeTagRetrieveUpdateDestroyAPIView.as_view(), name='recipetag-detail'),

    # Comment
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('comments/by-recipe/<int:recipe_id>/', CommentsByRecipeAPIView.as_view(), name='comments-by-recipe'),

    # SavedRecipe
    path('saved-recipes/', SavedRecipeListCreateAPIView.as_view(), name='savedrecipe-list-create'),
    path('save-recipe/<int:pk>/', SaveRecipeRetrieveUpdateDestroyAPIView.as_view(), name='save-recipe-detail'),
    path('save-recipe/', SaveRecipeListCreateAPIView.as_view(), name='save-recipe-list-create'),

    # Subscription
    path('subscriptions/', SubscriptionListCreateAPIView.as_view(), name='subscription-list-create'),
    path('subscriptions/<int:pk>/', SubscriptionRetrieveUpdateDestroyAPIView.as_view(), name='subscription-detail'),

    # Rating
    path('ratings/', RatingListCreateAPIView.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', RatingRetrieveUpdateDestroyAPIView.as_view(), name='rating-detail'),
    path('ratings/by-recipe/<int:recipe_id>/', RatingsByRecipeAPIView.as_view(), name='ratings-by-recipe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
