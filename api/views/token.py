from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id,
        'role': user.role.id if user.role else None,
        'company_id': user.company.id if user.company else None,
    }
