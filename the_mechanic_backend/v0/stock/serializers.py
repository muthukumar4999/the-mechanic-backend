from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from the_mechanic_backend.apps.stock.models import Brand, BrandModel, Spare


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('__all__')


class BrandModelSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    full_vehicle_name = serializers.SerializerMethodField()

    def get_full_vehicle_name(self, obj):
        return f'{obj.brand.name} {obj.model_name}'

    def get_brand_name(self, obj):
        return obj.brand.name

    class Meta:
        model = BrandModel
        fields = ('id', 'model_name', 'brand_name', 'full_vehicle_name')


class AddBrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandModel
        fields = ('__all__')


class SpareSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    full_vehicle_name = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()

    def get_full_vehicle_name(self, obj):
        return f'{obj.brand.name} {obj.brand_model.model_name}'

    def get_brand_name(self, obj):
        return obj.brand.name

    def get_model_name(self, obj):
        return obj.brand_model.model_name

    class Meta:
        model = Spare
        fields = ('brand_name', 'full_vehicle_name', 'model_name', 'spare_name', 'quantity',
                  'per_price', 'suppliers', 'quality_class',)


class AddSpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spare
        fields = ('__all__')


#
#
# class CreateFileUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Media
#         fields = ('key', 'file_name', 'uploaded_at',)
#
#
# class GetFileSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField()
#
#     def get_url(self, obj):
#         return settings.AWS_S3_BASE_LINK + obj.key
#
#     class Meta:
#         model = Media
#         fields = ('id', 'file_name', 'url', 'key',)
#
#
# class BasicUserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'user_type', 'phone_number')
#
#
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = 'Unable to login with required credentials'
            raise ValidationError(msg)
        return user

#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name',)
#
#
# class AuthUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AuthUser
#         fields = ('token',)

#
# class CategorySerializer(serializers.ModelSerializer):
#     sub_category_count = serializers.SerializerMethodField()
#     sub_category_names = serializers.SerializerMethodField()
#     sub_categories = serializers.SerializerMethodField()
#     image = GetFileSerializer(required=False)
#
#     def get_sub_categories(self, obj):
#         is_sub_category = self.context.get('is_sub_category', None)
#         if is_sub_category:
#             return SubCategorySerializer(SubCategory.objects.filter(category=obj.id), many=True).data
#         return None
#
#     def get_sub_category_count(self, obj):
#         user = self.context.get('user', None)
#         if user and user.user_type == User.WHOLESALER:
#             wholesaler_products = WholesalerProduct.objects.filter(wholesaler=user,
#                                                                    sub_category__category=obj.id)
#             sub_category_list = [wholesaler_product.sub_category for wholesaler_product in
#                                  wholesaler_products]
#             return len(set(sub_category_list))
#
#         return SubCategory.objects.filter(category=obj.id).count()
#
#     def get_sub_category_names(self, obj):
#         user = self.context.get('user', None)
#         if user and user.user_type == User.WHOLESALER:
#             wholesaler_products = WholesalerProduct.objects.filter(wholesaler=user,
#                                                                    sub_category__category=obj.id)
#             sub_category_list = [wholesaler_product.sub_category for wholesaler_product in
#                                  wholesaler_products]
#             sub_category = list(set(sub_category_list))
#             count = len(sub_category)
#         else:
#             sub_category = SubCategory.objects.filter(category=obj.id)
#             count = sub_category.count()
#         if sub_category:
#             if count > 3:
#                 sub_categories = sub_category[0:4]
#             elif count > 2:
#                 sub_categories = sub_category[0:3]
#             elif count > 1:
#                 sub_categories = sub_category[0:2]
#             else:
#                 sub_categories = sub_category[0:1]
#             return ",".join([sub_category.name for sub_category in sub_categories])
#         return ""
#
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'image', 'sub_category_count', 'sub_category_names', 'sub_categories')
#
#
# class SubCategorySerializer(serializers.ModelSerializer):
#     product_count = serializers.SerializerMethodField()
#     product_names = serializers.SerializerMethodField()
#
#     def get_product_count(self, obj):
#         user = self.context.get('user', None)
#         if user and user.user_type == User.WHOLESALER:
#             wholesaler_products = WholesalerProduct.objects.filter(wholesaler=user,
#                                                                    sub_category=obj.id)
#             product_list = [wholesaler_product.product for wholesaler_product in
#                             wholesaler_products]
#             return len(set(product_list))
#         return Product.objects.filter(sub_category=obj.id).count()
#
#     def get_product_names(self, obj):
#         user = self.context.get('user', None)
#         if user and user.user_type == User.WHOLESALER:
#             wholesaler_products = WholesalerProduct.objects.filter(wholesaler=user,
#                                                                    sub_category=obj.id)
#             product_list = [wholesaler_product.product for wholesaler_product in
#                             wholesaler_products]
#             products = list(set(product_list))
#             count = len(products)
#         else:
#             products = Product.objects.filter(sub_category=obj.id)
#             count = products.count()
#
#         if products:
#             if count > 3:
#                 products = products[0:4]
#             elif count > 2:
#                 products = products[0:3]
#             elif count > 1:
#                 products = products[0:2]
#             else:
#                 products = products[0:1]
#             return ",".join([product.name for product in products])
#         return ""
#
#     class Meta:
#         model = SubCategory
#         fields = ('id', 'name', 'category', 'product_count', 'product_names')
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     image = GetFileSerializer(required=False)
#     wholesalers_count = serializers.SerializerMethodField()
#
#     def get_wholesalers_count(self, obj):
#         return WholesalerProduct.objects.filter(product=obj.id, is_out_of_stock=False).count()
#
#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'sub_category', 'image', 'unit', 'wholesalers_count')
#
#
# class AddProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'sub_category', 'image', 'unit')
#
#
# class AddWholesalerProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WholesalerProduct
#         fields = ('id', 'wholesaler', 'sub_category', 'product', 'price', 'quantity', 'is_out_of_stock',)
#
#
# class WholesalerProductSerializer(serializers.ModelSerializer):
#     wholesaler = UserSerializer()
#     sub_category = SubCategorySerializer()
#     product = ProductSerializer()
#     category = serializers.SerializerMethodField()
#
#     def get_category(self, obj):
#         return CategorySerializer(obj.sub_category.category).data
#
#     class Meta:
#         model = WholesalerProduct
#         fields = ('id', 'wholesaler', 'sub_category', 'product', 'price', 'quantity', 'is_out_of_stock', 'category')
#
#
# class ListWholesalerProductSerializer(serializers.ModelSerializer):
#     product_name = serializers.SerializerMethodField()
#     store_name = serializers.SerializerMethodField()
#     quantity = serializers.SerializerMethodField()
#     current_price = serializers.SerializerMethodField()
#     contact_number = serializers.SerializerMethodField()
#
#     def get_product_name(self, obj):
#         return obj.product.name
#
#     def get_store_name(self, obj):
#         return f'{obj.wholesaler.first_name} {obj.wholesaler.last_name}'
#
#     def get_quantity(self, obj):
#         return f'{obj.quantity} {obj.product.unit}'
#
#     def get_current_price(self, obj):
#         return '0'
#
#     def get_contact_number(self, obj):
#         return obj.wholesaler.username
#
#     class Meta:
#         model = WholesalerProduct
#         fields = ('id', 'store_name', 'product_name', 'price', 'quantity', 'current_price', 'contact_number')
#
#
# class AdminConsumerProductListSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#     category_name = serializers.SerializerMethodField()
#     sub_category_name = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     original_price = serializers.SerializerMethodField()
#
#     def get_name(self,obj):
#         return obj.product.name
#
#     def get_category_name(self, obj):
#         return obj.product.sub_category.category.name
#
#     def get_sub_category_name(self, obj):
#         return obj.product.sub_category.name
#
#     def get_image(self, obj):
#         return GetFileSerializer(obj.product.image).data
#
#     def get_original_price(self, obj):
#         return obj.wholesaler_product.price
#
#
#     class Meta:
#         model = ConsumerProduct
#         fields = ('id', 'name', 'category_name', 'sub_category_name', 'image', 'customer_price','original_price')
#
#
# class OrderCartSerializer(serializers.ModelSerializer):
#     is_out_of_stock = serializers.SerializerMethodField()
#
#     def get_is_out_of_stock(self, obj):
#         return obj.consumer_product.wholesaler_product.is_out_of_stock
#
#     class Meta:
#         model = OrderCart
#         fields = ('id', 'consumer_product', 'quantity', 'updated_at', 'is_out_of_stock')
#
