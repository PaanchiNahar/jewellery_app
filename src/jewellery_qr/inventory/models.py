from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

# Create your models here.

# Merchant
class MerchantDetail(models.Model):
    merchant_code = models.BigIntegerField(primary_key=True)
    merchant_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    address = models.TextField()

    def __str__(self):
        return self.merchant_name

# Product
class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    product_type = models.CharField(max_length=100)
    weight = models.FloatField()
    seller = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    

    def save(self, *args, **kwargs):
        print(f"Saving product: {self.product_type} with ID {self.product_id}")
        qr_data = f"/inventory/product/{self.product_id}/"
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        self.qr_code.save(f'qr_{self.product_id}.png', File(buffer), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_type} - {self.product_id}"

# Sales
class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# Stock
class Stock(models.Model):
    category = models.CharField(max_length=100, primary_key=True)
    category_stock = models.BigIntegerField()

# Category N
class CategoryN(models.Model):
    category_n_id = models.BigIntegerField(primary_key=True)
    weight = models.FloatField()
    merchant_code = models.ForeignKey(MerchantDetail, on_delete=models.CASCADE)

# Purchases
class Purchase(models.Model):
    category_id = models.BigIntegerField(primary_key=True)
    category_type = models.BigIntegerField()
    merchant_code = models.ForeignKey(MerchantDetail, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    weight = models.FloatField()

# Client Details
class ClientDetail(models.Model):
    client_id = models.BigIntegerField(primary_key=True)
    client_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    address = models.TextField()
    purchase_history = models.BigIntegerField(blank=True, null=True)  # optional, for now

# Mortgage
class Mortgage(models.Model):
    client_id = models.ForeignKey(ClientDetail, on_delete=models.CASCADE)
    product_id = models.BigIntegerField()
    client_name = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    product_weight = models.FloatField()
    product_actual_price = models.BigIntegerField()
    product_price_kept = models.BigIntegerField()
    duration = models.TimeField()
    interest = models.FloatField()
    start_date = models.DateField()

    def __str__(self):
        return f"Mortgage: {self.client_name} - {self.product_id}"