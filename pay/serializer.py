#pay/serializer.py
from rest_framework import serializers
from .models import Pay
from policy.models import Policy
from promotion.models import Promotion
class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model:Pay = Pay
        read_only_fields = ['original_amount', 'final_amount']
        fields = ['id', 'policy', 'promotion', 'original_amount', 'final_amount', 'paymend_detail', 'status','at_creation','at_update']
    