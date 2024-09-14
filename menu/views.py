# Create your views here.
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Restaurant, FoodItem, Menu
from .serializers import RestaurantSerializer, FoodItemSerializer, MenuSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#qr code generation
from .utils import generate_qr_code
from rest_framework.decorators import action
from rest_framework.response import Response


# Restaurant ViewSet
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create/update
    
    def perform_create(self, serializer):
        # Assign the owner as the currently authenticated user
        serializer.save(owner=self.request.user)

# FoodItem ViewSet

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('restaurant',)
    ordering_fields = '__all__'


# Menu ViewSet
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.select_related('restaurant').all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]  # Anyone can view the menu

    @action(detail=True, methods=['post'], url_path='generate-qr-code')
    def generate_qr_code(self, request, pk=None):
        try:
            menu = self.get_object()
            generate_qr_code(menu)
            return Response({"message": "QR code generated successfully."}, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({"error": "Menu not found."}, status=status.HTTP_404_NOT_FOUND)



#QRCODE GENERATING 

