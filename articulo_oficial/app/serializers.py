from rest_framework import serializers
from .models import Articulo

class ArticuloSerializer(serializers.ModelSerializer):
    codigo_ean = serializers.CharField()
    nombre = serializers.CharField()
    descripcion = serializers.CharField()
    caracteristicas = serializers.CharField()

    class Meta:
        model = Articulo
        fields = '__all__'

    def create(self, validate_data):
        instance = Articulo()
        instance.codigo_ean = str(validate_data.get('codigo_ean'))
        instance.nombre = validate_data.get('nombre')
        instance.descripcion = validate_data.get('descripcion')
        instance.caracteristicas = validate_data.get('caracteristicas')
        instance.save()
        return instance

    def validate_codigo_ean(self,data):
        if Articulo.objects.filter(codigo_ean=str(data)).exists():
            raise serializers.ValidationError("El código ya existe")
        else:
            return data