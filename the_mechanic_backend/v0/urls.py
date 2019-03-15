from django.urls import path, include

urlpatterns = [
    path('stock/', include(('the_mechanic_backend.v0.stock.urls', 'the_mechanic_backend.v0.stock'), namespace='stock')),
    ]
