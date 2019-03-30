from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

schema_view = get_schema_view(title="Market App", renderer_classes=[SwaggerUIRenderer, OpenAPIRenderer],
                              urlconf='the_mechanic_backend.v0.urls', description="API V0",
                              url="/api/v0/")

urlpatterns = [
    path('stock/', include(('the_mechanic_backend.v0.stock.urls', 'the_mechanic_backend.v0.stock'), namespace='stock')),
    path('accounts/',
         include(('the_mechanic_backend.v0.accounts.urls', 'the_mechanic_backend.v0.accounts'), namespace='accounts')),
    path('service/',
         include(('the_mechanic_backend.v0.service.urls', 'the_mechanic_backend.v0.service'), namespace='service')),
    path('docs/', schema_view, name='api-docs'),
]
