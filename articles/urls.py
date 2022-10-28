from django.urls import path
from articles import views

app_name = 'articels'

urlpatterns = [
    path('', views.ArticlesView.as_view(), name="Articlesview"),
    path('<int:article_id>/', views.ArticleDetailView.as_view(), name="Article_detail"),
    path('comment/', views.CommnetView.as_view(), name="Commentview"),
    path('comment/<int:commnet_id>', views.CommnetDetailView.as_view(), name="Comment_detail"),
    path('like/', views.LikeView.as_view(), name="Likeview"),
]
