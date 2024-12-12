from rest_framework import serializers

from api.models import Good, Token




    
class TokenSerializer(serializers.Serializer):
    def is_valid_token(value):
        if len(value) != 36:
            raise serializers.ValidationError("Token must be 36 characters long")
        if Token.objects.filter(token=value).exists():
            raise serializers.ValidationError("Token already exists")
        return value
    token = serializers.CharField(max_length=36,validators=[is_valid_token])
    
class GoodSerializer(serializers.ModelSerializer):

    class Meta:
        model=Good
        fields = "__all__"

    def validate_amount(self,attrs):
        if attrs <= 0:
            raise serializers.ValidationError("Amount must be more than 0")
        else: return attrs

    def validate_price(self,attrs):
        if attrs <= 0:
            raise serializers.ValidationError("Price must be more than 0")
        else: return attrs
        