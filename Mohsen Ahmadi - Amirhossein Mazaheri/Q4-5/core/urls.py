from django.contrib import admin
from django.urls import path, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ctf.urls')),
    # path('auth/generate-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # obtaining JWT tokens
    # path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),  # refreshing JWT tokens
]
