from rest_framework.routers import DefaultRouter
from question import views
from django.urls import path, include


router = DefaultRouter()
router.register("questions", views.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("questions/<slug:slug>/answer/", views.AnswerCreateAPIView.as_view(), name="answer-create"),
    path("answer/<uuid:uuid>/", views.AnswerRetreiveUpdateDestroyAPIView.as_view(), name="answer-detail"),
    path("questions/<slug:slug>/answers/", views.AnsewrListAPIView.as_view(), name="answer-list"),
    path("answers/<uuid:uuid>/like/", views.AnswerLikeAPIView.as_view(), name="answer-like")
    
]


