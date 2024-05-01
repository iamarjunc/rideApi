from django.urls import path
from .views import RegisterView, LoginView, CreateRideView, RideDetailView, ListRidesView, RideStatusUpdateView, \
    RideCurrentLocationUpdateView, RideAcceptView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('rides/', CreateRideView.as_view(), name='create_ride'),
    path('rides/<int:ride_id>/', RideDetailView.as_view(), name='ride_detail'),
    path('rides_list/', ListRidesView.as_view(), name='list_rides'),
    path('rides/<int:ride_id>/status/', RideStatusUpdateView.as_view(), name='update_ride_status'),
    path('rides/<int:ride_id>/location/', RideCurrentLocationUpdateView.as_view(), name='ride-location-update'),
    path('rides/<int:ride_id>/accept/', RideAcceptView.as_view(), name='ride-accept'),

]