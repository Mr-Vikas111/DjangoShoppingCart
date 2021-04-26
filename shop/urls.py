from django.urls import path
from . import views
urlpatterns = [
    path("", views.index,name ="ShopName"),
    path("about/", views.about,name ="AboutUs"),
    path("contect/", views.contect,name ="contect"),
    path("tracker/", views.tracker,name ="TrackingStatus"),
    path("search/", views.search,name ="Search"),
    path("products/<int:myid>", views.productview,name ="productview"),
    path("checkout/", views.checkout,name ="Checkout"),
    path("handlerequest/", views.handlerequest,name ="HandleRequest"),
    

]          