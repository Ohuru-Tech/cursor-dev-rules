---
description: Django REST Framework development standards and best practices for class-based views, permissions, serializers, admin, and environment configuration
globs:
  - "**/settings.py"
  - "**/settings/**/*.py"
  - "**/views.py"
  - "**/views/**/*.py"
  - "**/serializers.py"
  - "**/serializers/**/*.py"
  - "**/permissions.py"
  - "**/permissions/**/*.py"
  - "**/admin.py"
  - "**/models.py"
  - "**/models/**/*.py"
  - "**/urls.py"
  - "**/api/**/*.py"
alwaysApply: false
---

# Django REST Framework Development Standards

Follow these standards when developing Django REST Framework (DRF) applications.

## Environment Configuration

Always use separate environment configurations with `django-environ`:

- **Separate settings files**: Create separate settings files for different environments (base, development, staging, production)
- **Use django-environ**: Use `django-environ` package to manage environment variables
- **Environment variables**: Store all sensitive and environment-specific settings in environment variables
- **Settings structure**: Organize settings in a `settings/` directory with `base.py`, `development.py`, `production.py`, etc.

### Environment Configuration Examples

```python
# settings/base.py
import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

DATABASES = {
    'default': env.db(),
}

# settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
```

## Class-Based Views

Always use class-based views (CBVs) instead of function-based views:

- **Prefer CBVs**: Use DRF's class-based views (`APIView`, `ViewSet`, `GenericViewSet`, etc.)
- **ViewSets for CRUD**: Use `ModelViewSet` or `ReadOnlyModelViewSet` for standard CRUD operations
- **Custom actions**: Use `@action` decorator for custom endpoints on ViewSets
- **APIView for custom logic**: Use `APIView` for endpoints that don't fit standard CRUD patterns

### Class-Based Views Examples

```python
# ✅ Good: Using ViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserDetailSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        # Business logic here
        user.is_active = True
        user.save()
        return Response({'status': 'activated'})

# ❌ Bad: Function-based view
from rest_framework.decorators import api_view

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
```

## Permissions

Always create proper permissions in separate permission files:

- **Separate permission files**: Create `permissions.py` file in each app for custom permissions
- **Use DRF permissions**: Leverage DRF's built-in permission classes (`IsAuthenticated`, `IsAdminUser`, etc.)
- **Custom permissions**: Create custom permission classes when needed, inheriting from `BasePermission`
- **Permission classes**: Assign permissions using `permission_classes` attribute or decorator

### Permissions Examples

```python
# permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows read-only access to all users,
    but write access only to admin users.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

## Business Logic in Views

Keep business logic in views, not in serializers:

- **Views contain logic**: All business logic, data processing, and orchestration should be in views
- **Serializers for validation**: Serializers should only handle data validation and serialization
- **Override DRF methods**: Override default DRF methods (`create`, `update`, `destroy`, `list`, `retrieve`) to implement business logic
- **Custom response handling**: Override `get_serializer_class()` or `get_queryset()` for conditional logic
- **Response customization**: Override methods to customize responses or use specific serializers

### Business Logic in Views Examples

```python
# ✅ Good: Business logic in views
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Business logic in view
        order = serializer.save(user=request.user)
        
        # Additional business logic
        order.calculate_total()
        order.send_confirmation_email()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def list(self, request, *args, **kwargs):
        # Business logic: filter by user if not admin
        queryset = self.filter_queryset(self.get_queryset())
        
        if not request.user.is_staff:
            queryset = queryset.filter(user=request.user)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        # Business logic in view
        if order.can_be_cancelled():
            order.cancel()
            order.send_cancellation_email()
            return Response({'status': 'cancelled'})
        return Response(
            {'error': 'Order cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )

# ❌ Bad: Business logic in serializer
class OrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        # Business logic should not be here
        order.calculate_total()
        order.send_confirmation_email()
        return order
```

## Serializers

Use serializers for validation and data transformation only:

- **Validation only**: Serializers should handle input validation and output serialization
- **Simple serializers**: Keep serializers focused on data structure and validation rules
- **Nested serializers**: Use nested serializers for related objects when appropriate
- **Serializer methods**: Use `SerializerMethodField` for computed fields, but keep logic minimal

### Serializer Examples

```python
# serializers.py
from rest_framework import serializers
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'location']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'profile']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        # Simple computed field - OK
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_email(self, value):
        # Validation logic - OK
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
```

## Admin Models

Create relevant admin models based on project functionality:

- **Functional admin**: Create admin models that reflect the actual functionality and workflow of the project
- **Not random**: Don't create admin models arbitrarily - they should serve a purpose
- **Customize admin**: Customize admin interface with list displays, filters, search, and actions
- **Inline admins**: Use inline admins for related models when appropriate
- **Admin actions**: Create custom admin actions for common operations

### Admin Models Examples

```python
# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Product

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'created_at', 'order_status_color']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'id']
    readonly_fields = ['created_at', 'updated_at', 'total']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_shipped', 'mark_as_delivered']
    
    def order_status_color(self, obj):
        colors = {
            'pending': 'orange',
            'shipped': 'blue',
            'delivered': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    order_status_color.short_description = 'Status'
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Mark selected orders as shipped'
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Mark selected orders as delivered'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_available']
    list_filter = ['is_available', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
```

## Directory Structure

Organize Django/DRF projects with clear separation of concerns:

```text
project/
├── manage.py
├── requirements.txt
├── .env
├── project/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── permissions.py
│   │   ├── admin.py
│   │   └── urls.py
│   └── orders/
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── permissions.py
│       ├── admin.py
│       └── urls.py
```

## URL Configuration

Organize URLs properly:

- **App-level URLs**: Create `urls.py` in each app
- **Router registration**: Use DRF's `DefaultRouter` or `SimpleRouter` for ViewSets
- **Include app URLs**: Include app URLs in project's main `urls.py`

### URL Configuration Examples

```python
# apps/orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.orders.urls')),
    path('api/v1/', include('apps.users.urls')),
]
```

## Best Practices

### Authentication

- **Token authentication**: Use DRF's token authentication or JWT for API authentication
- **Session authentication**: Use session authentication for web interfaces
- **Permission mixins**: Combine authentication and permissions appropriately

### Pagination

- **Enable pagination**: Always enable pagination for list endpoints
- **Custom pagination**: Create custom pagination classes when needed
- **Page size limits**: Set reasonable page size limits

### Filtering and Search

- **Django Filter**: Use `django-filter` for advanced filtering
- **Search fields**: Use `search_fields` in ViewSets for basic search
- **Filter backends**: Configure appropriate filter backends

### Error Handling

- **Exception handling**: Use DRF's exception handling or create custom exception handlers
- **Validation errors**: Return proper validation error responses
- **Custom exceptions**: Create custom exceptions for domain-specific errors

### Testing

- **APITestCase**: Use DRF's `APITestCase` for API endpoint testing
- **Test factories**: Use `factory_boy` or similar for test data creation
- **Permission testing**: Test permissions thoroughly
- **Integration tests**: Write integration tests for complex workflows

### Performance

- **Query optimization**: Use `select_related()` and `prefetch_related()` to avoid N+1 queries
- **Pagination**: Always paginate large result sets
- **Database indexes**: Add database indexes for frequently queried fields
- **Caching**: Use Django's caching framework for expensive operations

### Security

- **CSRF protection**: Ensure CSRF protection is properly configured
- **CORS**: Configure CORS appropriately for API access
- **Rate limiting**: Implement rate limiting for API endpoints
- **Input validation**: Always validate and sanitize user input
- **SQL injection**: Use ORM queries to prevent SQL injection

## Code Examples

### Complete ViewSet Pattern

```python
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderDetailSerializer
from .permissions import IsOrderOwner

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    
    def get_queryset(self):
        queryset = Order.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Business logic
        order = serializer.save(user=request.user)
        order.calculate_total()
        order.send_confirmation_email()
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.can_be_cancelled():
            order.cancel()
            return Response({'status': 'cancelled'})
        return Response(
            {'error': 'Cannot cancel this order'},
            status=status.HTTP_400_BAD_REQUEST
        )
```
