from django.urls import path
from .views import ThougthList,Dashboard,CreateThought,cook,Graf

app_name ='thoughts'

urlpatterns = [
    path('',ThougthList.as_view(),name='list'),
    path('graf/',Graf.as_view(),name='graf'),
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
    path('create-thought/',CreateThought.as_view(),name='create'),
    path('cook/',cook,name="cook"),
    
]
