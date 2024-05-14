from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cart.cart import Cart

from .serializers import CartAddProductSerializer,CartItemSerializer,CartDeleteSerializer


class CartGetAddApiView(APIView):
    serializer_class = CartAddProductSerializer
    def post(self, request):
        cart = Cart(request)
        serializer = CartAddProductSerializer(data=request.data, product_id=request.data.get('product_id'))

        if serializer.is_valid():
            product_id = serializer.validated_data.get('product_id')
            quantity = serializer.validated_data.get('quantity')
            size_id = serializer.validated_data.get('size_id',None)
            color_id = serializer.validated_data.get('color_id',None)

            cart.add(product_id,quantity,size_id=size_id,color_id=color_id)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        cart = Cart(request)
        items = [item for item in cart]
        length = len(cart)
        cart_total_price = cart.get_total_price()

        serializer = CartItemSerializer(items, many=True)
        response_data = {
            "items": serializer.data,
            "length": length,
            "cart_total_price": cart_total_price
        }
        return Response(response_data)


class CartProductDeleteApiView(APIView):
    serializer_class = CartDeleteSerializer
    def post(self,request):
        cart = Cart(request)
        serializer = CartDeleteSerializer(data=request.data, product_id=request.data.get('product_id'))

        if serializer.is_valid():
            cart.remove(**serializer.validated_data,remove_all=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




