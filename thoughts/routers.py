from rest_framework import routers
from .viewsets import ThoughtViewSet,UserViewSet


router = routers.DefaultRouter()
router.register('my-thoughts', ThoughtViewSet,basename='thought')
router.register('my-users',UserViewSet)









