from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Aquí puedes agregar datos al token encriptado (payload)
        # token['username'] = user.username
        # token['role'] = user.rol  <-- Si tienes roles
        return token

    def validate(self, attrs):
        # Esta función maneja la respuesta JSON que recibe el frontend
        data = super().validate(attrs)

        # Agregamos los datos extra que tu frontend necesita
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        
        # VERIFICACIÓN CLAVE PARA TU CASO:
        # Verificamos si el usuario ya tiene la tabla hija 'perfil' creada
        # Asumiendo que tu relación OneToOne se llama 'perfil'
        try:
            profile_exists = hasattr(self.user, 'perfil') and self.user.perfil is not None
        except Exception:
            profile_exists = False

        data['has_profile'] = profile_exists
        
        # También puedes devolver el is_active si lo usas para controlar el flujo
        data['is_active'] = self.user.is_active

        return data