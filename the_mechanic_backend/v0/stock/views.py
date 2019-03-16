from the_mechanic_backend.apps.stock.models import Brand, BrandModel, Spare
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
            return Utils.dispatch_failure(request, serializer.errors)
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
            return Utils.dispatch_failure(request, serializer.errors)
        except Exception as e:
            return self.internal_server_error(request, e)


class SpareList(CustomBaseClass):
    def get(self, request, brand_model_id):
        """
        return a list of spares for particular model
        :param request:
        @query_param
        search=search_text - to search the spares
        out_of_stock=true - to get only out of stock
        Note: we can use both at same time :)
        :param brand_model_id:
        :return:
        """
        try:
            search = request.GET.get('search')
            out_of_stock = request.GET.get('out_of_stock')
            if search:
                spare = self.get_filter_objects(Spare, brand_model=brand_model_id, spare_name__icontains=search)
            else:
                spare = self.get_filter_objects(Spare, brand_model=brand_model_id)

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
            return Utils.dispatch_failure(request, serializer.errors)
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
            return Utils.dispatch_failure(request, serializer.errors)
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
