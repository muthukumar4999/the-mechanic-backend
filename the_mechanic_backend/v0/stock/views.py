import datetime

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q

from the_mechanic_backend.apps.accounts.models import Store
from the_mechanic_backend.apps.stock.models import Brand, BrandModel, Spare, SpareCustomer, SpareOrder, SpareSold
from the_mechanic_backend.v0.stock import serializers
from the_mechanic_backend.v0.utils import Utils, CustomBaseClass


class BrandList(CustomBaseClass):
    """
        Brand List and create Endpoint
    """

    def get(self, request):
        """
        returns the list of brand
        :param request:
        :return:
        """
        try:
            search = request.GET.get('search', '')
            if search:
                brands = self.get_filter_objects(Brand, name__icontains=search)
            else:
                brands = self.get_all_objects(Brand)
            serializer = serializers.BrandSerializer(brands, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return self.internal_server_error(request, e)

    def post(self, request):
        """
        Creates a new brand
        :param request:
        {
           "name" : "Honda"
        }
        :return:
        """
        try:
            serializer = serializers.BrandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
        except Exception as e:
            return self.internal_server_error(request, e)


class BrandModelList(CustomBaseClass):
    """
    Brand Model List and create Endpoint
    """

    def get(self, request, brand_id):
        """
        Returnt the list of Models of particular brand
        :param request:
        :param brand_id:
        :return:
        """
        try:
            search = request.GET.get('search', '')
            if search:
                brands = self.get_filter_objects(BrandModel, brand=brand_id, model_name__icontains=search)
            else:
                brands = self.get_filter_objects(BrandModel, brand=brand_id)
            serializer = serializers.BrandModelSerializer(brands, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return self.internal_server_error(request, e)

    def post(self, request, brand_id):
        """
        Creates a new brand model
        :param request:
          {
             "model_name" : "Unicorn"
          }
        :param brand_id:
        :return:
        """
        try:
            data = request.data
            data['brand'] = brand_id
            serializer = serializers.AddBrandModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
        except Exception as e:
            return self.internal_server_error(request, e)


class SpareList(CustomBaseClass):
    def get(self, request, store_id, brand_model_id):
        """
        return a list of spares for particular model
        :param request:
        @query_param
        search=search_text - to search the spares
        out_of_stock=true - to get only out of stock
        Note - we can use both at same time :)
        :param store_id
        :param brand_model_id:
        :return:
        """
        try:
            search = request.GET.get('search')
            out_of_stock = request.GET.get('out_of_stock')
            spare = self.get_filter_objects(Spare, brand_model=brand_model_id, store=store_id)

            if search:
                spare = spare.filter(Q(spare_id__icontains=search) | Q(spare_name__icontains=search))

            if out_of_stock:
                spare = spare.filter(quantity=0)

            serializer = serializers.SpareSerializer(spare, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return self.internal_server_error(request, e)

    def post(self, request, brand_model_id):
        """
        Create a spare
        :param request:
        {
            "spare_name": "SIde Mirror",
            "spare_id": #34545435,
            "quantity": 10,
            "per_price": "500",
            "suppliers": "Glass India",
            "quality_class": "FIRST"
        }
        :param brand_model_id:
        :return:
        """
        try:
            data = request.data
            brand_model = self.get_object(BrandModel, brand_model_id)
            if not brand_model:
                return self.object_not_found(request)
            data['brand'] = brand_model.brand.id
            data['brand_model'] = brand_model_id
            serializer = serializers.AddSpareSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
        except Exception as e:
            return self.internal_server_error(request, e)


class SpareDetails(CustomBaseClass):
    """
    particular spare details
    """

    def get(self, request, spare_id):
        """
        Return requested spare
        :param request:
        :param spare_id:
        :return:
        """
        try:
            spare = self.get_object(Spare, spare_id)
            if not spare:
                return self.object_not_found(request)
            serializer = serializers.SpareSerializer(spare)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return self.internal_server_error(request, e)

    def put(self, request, spare_id):
        """
        Updates the requested spare
        :param request:
        # partial fields are also acceptable
        {
            "spare_name": "SIde Mirror",
            "spare_id": #34545435,
            "quantity": 10,
            "per_price": "500",
            "suppliers": "Glass India",
            "quality_class": "FIRST"
        }
        :param spare_id:
        :return:
        """
        try:
            spare = self.get_object(Spare, spare_id)
            if not spare:
                return self.object_not_found(request)
            serializer = serializers.AddSpareSerializer(spare, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
        except Exception as e:
            return self.internal_server_error(request, e)

    def delete(self, request, spare_id):
        """
        Delete the request spare
        :param request:
        :param spare_id:
        :return:
        """
        try:
            spare = self.get_object(Spare, spare_id)
            if not spare:
                return self.object_not_found(request)
            spare.delete()
            return Utils.dispatch_success(request, 'SUCCESS')
        except Exception as e:
            return self.internal_server_error(request, e)


class SpareOrderList(CustomBaseClass):
    def get(self, request, store_id, *args, **kwargs):
        """
        Returns the list of Spares based on Store
        :param request:
        # params
        start_date=2019-01-31&&
        end_date=2019-12-31&&
        page=1
        :param store_id:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            page = request.GET.get('page', 1)
            qs = SpareOrder.objects.filter(store=store_id, order_date__range=[start_date, end_date])

            paginator = Paginator(qs, per_page=10)
            serializer = serializers.SpareOrderHistorySerializer(paginator.page(page), many=True)
            response_data = {
                "data": serializer.data,
                "page": int(page),
                "total_pages": paginator.num_pages
            }
            return Utils.dispatch_success(request, response_data)
        except Exception as e:
            return self.internal_server_error(request, e)

    def post(self, request, store_id, *args, **kwargs):
        """
        Create a new Order
        :param request:
        {
                "customer_info": {
                    "name": "Muthu Kumar",
                    "email": "itmemk@gmail.com",
                    "phone_number": "9876543210",
                    "address": "ADDRESSS"
                },
                "order_type": "IN_SOURCE / OUT_SOURCE",
                "spares": [
                    {
                        "spare_id": 1,
                        "spare_price_type": 'MRP / MECHANIC / WHOLESALER / CUSTOMER',
                        "spare_count": 2
                    },
                    {
                        "spare_id": 1,
                        "spare_price_type": 'MRP / MECHANIC / WHOLESALER / CUSTOMER',
                        "spare_count": 2
                    },
                    {
                        "spare_id": 1,
                        "spare_price_type": 'MRP / MECHANIC / WHOLESALER / CUSTOMER',
                        "spare_count": 2
                    }
                ]

            }
        :param store_id:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data = request.data

            try:
                customer = SpareCustomer.objects.get(phone_number=data['customer_info']['phone_number'])
            except SpareCustomer.DoesNotExist:
                customer_serializer = serializers.SpareCustomerSerializer(data=data['customer_info'])
                if customer_serializer.is_valid():
                    customer_serializer.save()
                else:
                    return Utils.dispatch_failure(request, "VALIDATION_ERROR", customer_serializer.errors)
                customer = SpareCustomer.objects.get(id=customer_serializer.data['id'])

            today = datetime.date.today()
            today_order_count = SpareOrder.objects.filter(order_date__year=today.year,
                                                          order_date__month=today.month).count()

            order_id = 'SPOR{}{:05d}'.format(today.strftime("%Y%m"), today_order_count + 1)
            with transaction.atomic():
                print(self.get_object(Store, store_id))
                order = SpareOrder(order_id=order_id,
                                   store=self.get_object(Store, store_id),
                                   order_type=data['order_type'],
                                   customer=customer,
                                   total=0.0,
                                   sold_by=request.user)
                order.save()
                total = 0.0
                spares_to_be_created = []
                for _spare in data['spares']:
                    spare = self.get_object(Spare, _spare['spare_id'])
                    price_map = {
                        'MRP': spare.mrp_price,
                        'MECHANIC': spare.mechanic_price,
                        'WHOLESALER': spare.wholesaler_price,
                        'CUSTOMER': spare.customer_price,
                    }
                    sold_spare = SpareSold(order=order,
                                           spare=spare,
                                           spare_count=_spare['spare_count'],
                                           spare_name=spare.spare_name,
                                           spare_price=price_map[_spare['spare_price_type']],
                                           spare_price_type=_spare['spare_price_type'])
                    spares_to_be_created.append(sold_spare)
                    total = total + float(sold_spare.spare_count * sold_spare.spare_price)
                    spare.quantity = spare.quantity - sold_spare.spare_count
                    spare.save()
                SpareSold.objects.bulk_create(spares_to_be_created)
                order.total = total
                order.save()
                return Utils.dispatch_success(request, {'order_id': order.id})
        except Exception as e:
            return self.internal_server_error(request, e)


class SparesAccounts(CustomBaseClass):
    def get_total(self, qs, report_type):
        if report_type == 'IN_SELL':
            pass
        elif report_type == 'OUT_SELL':
            pass
        elif report_type == 'TOTAL_SELL':
            pass
        elif report_type == 'IN_PROFIT':
            pass
        elif report_type == 'OUT_PROFIT':
            pass
        elif report_type == 'TOTAL_PROFIT':
            pass
        else:
            return 0

    def get(self, request):
        try:
            stores = request.GET.get('stores').split(',')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            report_type = request.GET.get('report_type')

            sell_report_type = ['IN_SELL', 'OUT_SELL', 'TOTAL_SELL']
            profit_report_type = ['IN_PROFIT', 'OUT_PROFIT', 'TOTAL_PROFIT']

            profit_map = {
                "IN_PROFIT": "IN_SELL",
                "OUT_PROFIT": "OUT_SELL",
                "TOTAL_PROFIT": "TOTAL_SELL",
            }

            qs = SpareOrder.objects.filter(store__id__in=stores, order_date=[start_date, end_date])

            if report_type in sell_report_type:
                return Utils.dispatch_success(request, {"sell_total": self.get_total(qs, report_type)})

            if report_type in profit_report_type:
                sell_price = self.get_total(qs, report_type)
                response_data = {"sell_total": sell_price}
                return Utils.dispatch_success(request, response_data)







        except Exception as e:
            return self.internal_server_error(request, e)
