from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny

from the_mechanic_backend.apps.service.models import GeneralService, SubService, ServiceType, Service, Customer
from the_mechanic_backend.v0.service import serializers
from the_mechanic_backend.v0.utils import Utils, CustomBaseClass


class GeneralServiceView(CustomBaseClass):
    def get(self, request):
        try:
            gs = self.get_all_objects(GeneralService)
            serializer = serializers.GeneralServiceSerializer(gs, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            self.internal_server_error(request, e)


class SubServiceView(CustomBaseClass):
    def get(self, request, service_type_id):
        try:
            ss = self.get_filter_objects(SubService, service=service_type_id)
            serializer = serializers.SubServiceSerializer(ss, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            self.internal_server_error(request, e)


class ServiceTypeView(CustomBaseClass):
    def get(self, request):
        try:
            st = self.get_all_objects(ServiceType)
            serializer = serializers.ServiceTypeSerializer(st, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return self.internal_server_error(request, e)


class ServiceList(CustomBaseClass):
    def get(self, request):
        try:
            user = request.user
            status = request.GET.get('status', 'NEW')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            if user.is_staff:
                services = self.get_filter_objects(Service, status=status)
            else:
                services = self.get_filter_objects(Service, status=status, labour=user)
            paginator = Paginator(services, per_page=page_size)
            serializer = serializers.ListServiceSerializer(paginator.page(page), many=True)
            response_data = {
                'data': serializer.data,
                'total_pages': paginator.num_pages,
                'current_page': page
            }
            return Utils.dispatch_success(request, response_data)
        except Exception as e:
            return self.internal_server_error(request, e)

    def post(self, request):
        try:
            request_data = request.data
            customer_data = request_data['customer_data']
            customer = Customer(customer_name=customer_data['customer_name'],
                                customer_phone_number=customer_data['customer_phone_number'],
                                customer_email=customer_data['customer_email'],
                                customer_address=customer_data['customer_address'],
                                customer_area=customer_data['customer_area'])
        except Exception as e:
            return self.internal_server_error(request, e)
