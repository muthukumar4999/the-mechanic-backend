import datetime

from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny

from the_mechanic_backend.apps.service.models import GeneralService, SubService, ServiceType, Service, Customer, \
    Vehicle, GeneralServiceTestResults, CustomerComplaints, SubServiceCost, SpareCost, ServiceCost
from the_mechanic_backend.apps.stock.models import Spare
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
            data = request.data
            customer_data = data['customer_data']
            customer = Customer(customer_name=customer_data['customer_name'],
                                customer_phone_number=customer_data['customer_phone_number'],
                                customer_email=customer_data['customer_email'],
                                customer_address=customer_data['customer_address'],
                                customer_area=customer_data['customer_area'])
            customer.save()
            vehicle_data = data['vehicle_data']

            vehicle = Vehicle(
                vehicle_number=vehicle_data['vehicle_number'],
                vehicle_brand=vehicle_data['vehicle_brand'],
                vehicle_model=vehicle_data['vehicle_model'],
                vehicle_color=vehicle_data['vehicle_color'],
            )

            vehicle.save()

            # data = {
            #
            #     "customer_data": {
            #         "customer_name": "",
            #         "customer_phone_number": "",
            #         "customer_email": "",
            #         "customer_address": "",
            #         "customer_area": "",
            #     },
            #     "helmet": True,
            #     "vehicle_data": {
            #         "vehicle_number": "",
            #         "vehicle_brand": "",
            #         "vehicle_model": "",
            #         "vehicle_color": "",
            #         "vehicle_odo_reading": "",
            #     },
            #     "services": [{"id": 1, 'has_total': True, "total": 1000, },
            #                  {"id": 2, 'has_total': True, "total": 500, },
            #                  {"id": 3, 'has_total': True, "total": 1500, },
            #                  {"id": 4, 'has_total': True, "total": 200, }, ],
            #     "general_service_check_list": [{"id": 1, "status": "'WORKING"},
            #                                    {"id": 2, "status": "'NOT_WORKING"},
            #                                    {"id": 3, "status": "'REPLACE"}, ],
            #     "customer_complaints": ["12345677", "23523523523", "23423423423"],
            #     "spares": [{"id": 1, "quantity": 10, },
            #                {"id": 2, "quantity": 1, },
            #                {"id": 3, "quantity": 2, },
            #                {"id": 4, "quantity": 3, }, ],
            #     "outworks": [{"id": 1, "cost": 100},
            #                  {"id": 2, "cost": 100},
            #                  {"id": 3, "cost": 100}],
            #     "labour_charge": 1000.00,
            #     "labour": 1,
            #     "delivery_date": "",
            #     "is_pickup": True,
            #     "pickup_details": {
            #         "pickup_cost": 1200,
            #         "pickup_address": "",
            #         "delivery_address": ""
            #     }
            # }

            # Add basic service
            service = Service(
                customer=customer,
                helmet=data['helmet'],
                vehicle=vehicle,
                vehicle_odo_reading=vehicle_data['vehicle_odo_reading'],
                status=Service.NEW,
                spare_count=len(data['spares']),
                service_in_date=datetime.datetime.now(),
                delivery_date=data['delivery_date'],
                labour_charge=data['labour_charge'],
            )

            # service pickup details
            if data['is_pickup']:
                service.is_pickup = data['is_pickup'],
                service.pickup_cost = data['pickup_details']['pickup_cost'],
                service.pickup_address = data['pickup_details']['pickup_address'],
                service.delivery_address = data['pickup_details']['delivery_address'],

            service.save()

            # service service_type details
            for _service in data['services']:
                service_type = self.get_object(ServiceType, _service['id'])
                if service_type:
                    service.services.add(service_type)

            # service general_service details
            for _general_service_check_list in data['general_service_check_list']:
                gs = self.get_object(GeneralService, _general_service_check_list['id'])
                if gs:
                    GeneralServiceTestResults(service=service,
                                              check_list=gs,
                                              status=_general_service_check_list['status']).save()

            # service Customer Complaints
            for _complaints in data['customer_complaints']:
                CustomerComplaints(complain=_complaints, service=service).save()

            # service add Other works
            for _outworks in data['outworks']:
                sub = self.get_object(SubService, _outworks['id'])
                if sub:
                    SubServiceCost(service=service,
                                   SubService=sub,
                                   cost=_outworks['cost']).save()

            # service spare details
            for _spare in data['spares']:
                spare = self.get_object(Spare, _spare['id'])
                if spare:
                    SpareCost(spare=spare,
                              quantity=_spare['quantity'],
                              per_price=spare.per_price,
                              ).save()

            # service service's :)
            for _service in data['services']:
                service_type = self.get_object(ServiceType, _service['id'])
                if service_type and _service['has_total']:
                    ServiceCost(service_type=service_type,
                                service=service,
                                cost=_service['total']).save()

            return Utils.dispatch_success(request, 'SUCCESS')

        except Exception as e:
            return self.internal_server_error(request, e)
