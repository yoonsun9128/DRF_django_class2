from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.ArticlesView.as_view(), name="article"),
    path('feed/',views.FeedView.as_view(), name="feedview"),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name="Article_detail"),
    path('<int:article_id>/comment/', views.CommnetView.as_view(), name="Commentview"),
    path('<int:article_id>/comment/<int:commnet_id>', views.CommentDetailView.as_view(), name="Comment_detail"),
    path('<int:article_id>/like/', views.LikeView.as_view(), name="Likeview"),
]
