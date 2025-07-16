from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=150)
    address = models.JSONField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# c1 = Customer(first_name = "Django", last_name = "Reinhardt", email = "dj_rein@mail.com", address="Liberchies, Pont-à-Celles, Belgium")
# c1.save()

# c1.first_name = "Darwin"
# c1.last_name = "Nunez"
# c1.email = "660xxxxx@kmitl.ac.th"
# c1.save()


class Cart(models.Model):
    customer_id = models.ForeignKey("shop.Customer", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    expired_in = models.IntegerField(default=60)

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    remaining_amount = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# p1 = Product(name = "USB-C Charger", description = "20W fast charging USB-C adapter, compact and efficient.", remaining_amount=100, price=299.50)
# p2 = Product(name = "Noise Cancelling Earbuds", description = "Wireless earbuds with advanced noise cancelling technology.", remaining_amount=50, price=1890.00)
# p3 = Product(name = "Mechanical Keyboard", description = "RGB mechanical keyboard designed for gamers with tactile feedback.", remaining_amount=25, price=2499.99)
# p1.save()
# p2.save()
# p3.save()


class CartItem(models.Model):
    cart = models.ForeignKey("shop.Cart", on_delete=models.CASCADE)
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

class ProductCategory(models.Model):
    name = models.CharField(max_length=150)
    productcategories = models.ManyToManyField("shop.Product")

class Order(models.Model):
    customer = models.ForeignKey("shop.Customer", on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    remark = models.TextField(null=True)

# c=Customer.objects.get(pk=1)
# c.first_name

# o = Order(customer=c, order_date="2025-07-16", remark="This is order for Darwin Nunez")
# o.save()



class OrderItem(models.Model):
    order = models.ForeignKey("shop.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

oi1 = OrderItem(order=o , product=p3 , amount=1)
oi2 = OrderItem(order=o , product=p1 , amount=2)
oi1.save()
oi2.save()



class Payment(models.Model):
    order = models.OneToOneField("shop.Order", on_delete=models.CASCADE)
    payment_date =  models.DateField(auto_now_add=True)
    remark = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class PaymentItem(models.Model):
    payment = models.ForeignKey("shop.Payment", on_delete=models.CASCADE)
    order_item = models.OneToOneField("shop.OrderItem", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class PaymentMethod(models.Model):
    payment = models.ForeignKey("shop.Payment", on_delete=models.CASCADE)
    class Method(models.TextChoices):
        QR = "QR", 
        CREDIT = "CREDIT"

    method = models.CharField(
        max_length=10,
        choices=Method,
        default=Method.QR
    )
