from django.db import models
from django.db.models import Sum


class ProductManager(models.Manager):
    def available_products(self):
        return self.filter(is_available=True) 
    
    def available_products_in_category(self, category_name: str):
        return self.filter(
            is_available=True,
            category__name=category_name
                           )

def product_quantity_ordered():
    total_products_ordered = Product.objects.annotate(total_ordered_quantity=Sum('orderproduct__quantity')).exclude(total_ordered_quantity=None).order_by('-total_ordered_quantity')

    result = []
    for product in total_products_ordered:
        result.append(f'Quantity ordered of {product.name}: {product.total_ordered_quantity}')
    
    return '\n'.join(result)

class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return f"{self.category.name}: {self.name}"


class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

