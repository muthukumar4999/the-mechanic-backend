from rest_framework import views

from the_mechanic_backend.apps.stock.models import Brand, BrandModel
from the_mechanic_backend.v0.stock import serializers
from the_mechanic_backend.v0.utils import Utils


class BrandList(views.APIView):
    def get(self, request):
        try:
            brands = Brand.objects.all()
            serializer = serializers.BrandSerializer(brands, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {'error': str(e)})

    def post(self, request):
        try:
            serializer = serializers.BrandSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, serializer.errors)
        except Exception as e:
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {'error': str(e)})


class BrandModelList(views.APIView):
    def get(self, request, brand_id):
        try:
            search = request.GET.get('search', '')
            if search:
                brands = BrandModel.objects.filter(brand=brand_id, model_name__icontains=search)
            else:
                brands = BrandModel.objects.filter(brand=brand_id)
            serializer = serializers.BrandModelSerializer(brands, many=True)
            return Utils.dispatch_success(request, serializer.data)
        except Exception as e:
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {'error': str(e)})

    def post(self, request, brand_id):
        try:
            data = request.data
            data['brand'] = brand_id
            serializer = serializers.AddBrandModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Utils.dispatch_success(request, serializer.data)
            return Utils.dispatch_failure(request, serializer.errors)
        except Exception as e:
            return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {'error': str(e)})
# class LoginView(views.APIView):
#     """
#        Login View allows the user to login into the application
#     """
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         """
#         To verify the authorized user and login them to the application
#         :param request:
#         :return:
#         """
#         validate_user = serializers.LoginSerializer(data=request.data)
#         if validate_user.is_valid():
#             user = validate_user.validated_data
#             old_tokens = AuthUser.objects.filter(user=user, is_expired=True)
#             if old_tokens:
#                 old_tokens.delete()
#
#             AuthUser.objects.filter(user=user).update(is_expired=True)
#             new_session = AuthUser(user=user)
#             new_session.token = Utils.generate_token()
#             new_session.save()
#             serializer = serializers.AuthUserSerializer(new_session)
#             return Utils.dispatch_success(request, serializer.data)
#         else:
#             return Utils.dispatch_failure(request, "UNAUTHORIZED_ACCESS", validate_user.errors)
#
#
# class CategoryList(generics.ListCreateAPIView):
#     """
#     Category List
#     """
#     serializer_class = serializers.CategorySerializer
#
#     def get(self, request, *args, **kwargs):
#         """
#         Return the list of categories
#         :param request:
#         :return:
#         """
#         try:
#             is_all_category = request.GET.get('all', None)
#             is_sub_category = request.GET.get('sub_category', None)
#             if is_all_category:
#                 category_list = Category.objects.all()
#             else:
#                 user = request.user
#                 user_type = user.user_type
#                 if user_type == User.WHOLESALER:
#                     wholesaler_products = WholesalerProduct.objects.filter(wholesaler=user)
#                     category_list = [wholesaler_product.sub_category.category for wholesaler_product in
#                                      wholesaler_products]
#                     category_list = set(category_list)
#                 else:
#                     category_list = Category.objects.all()
#             serializer = serializers.CategorySerializer(category_list, many=True, context={"user": request.user,
#                                                                                            'is_sub_category': is_sub_category})
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def post(self, request, *args, **kwargs):
#         """
#         Create a new category
#         :param request:
#         :return:
#         """
#         try:
#             serializer = serializers.CategorySerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class CategoryDetails(views.APIView):
#     """
#     Category Details
#     """
#
#     def get(self, request, category_id, *args, **kwargs):
#         """
#         Get the particular category details
#         :param request:
#         :param category_id: int
#         :return:
#         """
#         try:
#             category = Category.objects.get(id=category_id)
#             serializer = serializers.CategorySerializer(category)
#             return Utils.dispatch_success(request, serializer.data)
#         except Category.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, category_id):
#         """
#         Update a particular Category
#         :param request:
#         :param category_id: category id
#         :return:
#         """
#         try:
#             category = Category.objects.get(id=category_id)
#             serializer = serializers.CategorySerializer(category, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except Category.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class SubCategoryList(views.APIView):
#     """
#     Sub Category List
#     """
#
#     def get(self, request, category_id):
#         """
#         Return the list of sub categories
#         :param request:
#         :param category_id:
#         :return:
#         """
#         try:
#             is_all_sub_category = request.GET.get('all', None)
#             if is_all_sub_category:
#                 sub_category_list = SubCategory.objects.filter(category=category_id)
#             else:
#                 user = request.user
#                 user_type = user.user_type
#                 if user_type == User.WHOLESALER:
#                     wholesaler_products = WholesalerProduct.objects.filter(wholesaler=user,
#                                                                            product__sub_category__category=category_id)
#                     sub_category_list = [wholesaler_product.sub_category for wholesaler_product in
#                                          wholesaler_products]
#                     sub_category_list = set(sub_category_list)
#                 else:
#                     sub_category_list = SubCategory.objects.filter(category=category_id)
#             serializer = serializers.SubCategorySerializer(sub_category_list, many=True, context={"user": request.user})
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def post(self, request, category_id):
#         """
#         Create a new sub category
#         :param request:
#         :param category_id:
#         :return:
#         """
#         try:
#             data = request.data
#             if SubCategory.objects.filter(category=category_id, name__iexact=data['name']):
#                 return Utils.dispatch_failure(request, "ITEM_ALREADY_EXISTS")
#             data['category'] = category_id
#             serializer = serializers.SubCategorySerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class SubCategoryDetails(views.APIView):
#     """
#     Sub Category Details
#     """
#
#     def get(self, request, category_id, sub_category_id):
#         """
#         Get the particular sub category details
#         :param request:
#         :param category_id: int
#         :param sub_category_id: int
#         :return:
#         """
#         try:
#             sub_category = SubCategory.objects.get(id=sub_category_id)
#             serializer = serializers.SubCategorySerializer(sub_category)
#             return Utils.dispatch_success(request, serializer.data)
#         except SubCategory.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, category_id, sub_category_id):
#         """
#         Update a particular Sub Category
#         :param request:
#         :param category_id: category id
#         :param sub_category_id: sub_category id
#         :return:
#         """
#         try:
#             sub_category = SubCategory.objects.get(id=sub_category_id)
#             serializer = serializers.SubCategorySerializer(sub_category, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except SubCategory.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class ProductList(views.APIView):
#     """
#     Product List
#     """
#
#     def get(self, request, sub_category_id):
#         """
#         returns the list of products
#         :param request:
#         :param sub_category_id: sub_category_id
#         :return:
#         """
#         try:
#             products = Product.objects.filter(sub_category=sub_category_id)
#             serializer = serializers.ProductSerializer(products, many=True)
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def post(self, request, sub_category_id):
#         """
#         creates a new product
#         :param request:
#         :param sub_category_id: sub_category_id
#         :return:
#         """
#         try:
#             data = request.data
#             data['sub_category'] = sub_category_id
#             if Product.objects.filter(sub_category=sub_category_id, name__iexact=data['name']):
#                 return Utils.dispatch_failure(request, "ITEM_ALREADY_EXISTS")
#             serializer = serializers.AddProductSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#
# class ProductDetails(views.APIView):
#     """
#     Product Details
#     """
#
#     def get(self, request, sub_category_id, product_id):
#         """
#         Returns a particular product based on sub_category id
#         :param request:
#         :param sub_category_id: sub_category_id
#         :param product_id: product_id
#         :return:
#         """
#         try:
#             product = Product.objects.get(id=product_id, sub_category=sub_category_id)
#             serializer = serializers.ProductSerializer(product)
#             return Utils.dispatch_success(request, serializer.data)
#         except SubCategory.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
#
#     def put(self, request, sub_category_id, product_id):
#         """
#         Updates a particular product
#         :param request:
#         :param sub_category_id: sub_category_id
#         :param product_id: product_id
#         :return:
#         """
#         try:
#             product = Product.objects.get(id=product_id, sub_category=sub_category_id)
#             serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#             else:
#                 return Utils.dispatch_failure(request, 'VALIDATION_ERROR', serializer.errors)
#             return Utils.dispatch_success(request, serializer.data)
#         except SubCategory.DoesNotExist:
#             return Utils.dispatch_failure(request, 'OBJECT_RESOURCE_NOT_FOUND')
#         except Exception as e:
#             print(e)
#             return Utils.dispatch_failure(request, 'INTERNAL_SERVER_ERROR', {"error": str(e)})
