from rest_framework import serializers
from rest_framework.response import Response
from Address.models import Zone
from PaymentPlans.models import PaymentPlan
from Payment.models import PaymentMethod, PaymentHistory



class PaymentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlan
        fields = ['id', 'name', 'thumbnail', 'image_text', 'balance', 'duration', 'duration_type', 'note']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name']


class PaymentHistorySerializer(serializers.ModelSerializer):
    lawyer = serializers.CharField(source = 'lawyer.name')
    payment_method = serializers.CharField(source = 'payment_method.name')
    chosen_payment_plan = PaymentPlanSerializer()
    class Meta:
        model = PaymentHistory
        fields = ['id', 'lawyer', 'chosen_payment_plan', 'payment_method', 'amount', 'status', 'approved_at', 'created_by', 'transaction_number']

    # lawyer, chosen_payment_plan, payment_method, amount, status, approved_at, approved_by, created_by, note, transaction_number


