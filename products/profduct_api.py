from django.db.models import Sum
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import FastFoodProduct, ShopingModel
from .serializers import ShoppingCartSerializer


class ShoppingCartCreateAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                'success': False,
                'error': 'Login qilinmadi',
                'redirect': '/login/'
            }, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'success': False, 'error': 'ID kerak'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            delta = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            return Response({'success': False, 'error': 'Notog\'ri miqdor'}, status=status.HTTP_400_BAD_REQUEST)

        if delta == 0:
            return Response({'success': False, 'error': 'Miqdor 0 bo\'lishi mumkin emas'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = get_object_or_404(FastFoodProduct, id=product_id, is_active=True)

            cart_item, created = ShopingModel.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': 0},
            )

            new_quantity = cart_item.quantity + delta
            deleted = False

            if new_quantity <= 0:
                cart_item.delete()
                new_quantity = 0
                deleted = True
            else:
                cart_item.quantity = new_quantity
                cart_item.save(update_fields=['quantity'])

            cart_total_count = ShopingModel.objects.filter(
                user=request.user
            ).aggregate(total=Sum('quantity'))['total'] or 0

            response_data = {
                'success': True,
                'deleted': deleted,
                'product_id': str(product.id),
                'quantity': new_quantity,
                'cart_total_count': cart_total_count,
            }

            if not deleted:
                response_data['data'] = ShoppingCartSerializer(cart_item).data

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)