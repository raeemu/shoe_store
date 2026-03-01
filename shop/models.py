from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "categories"

    def __str__(self):
        return self.name


class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "units"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "suppliers"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "manufacturers"

    def __str__(self):
        return self.name


class Good(models.Model):
    id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    price = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    discount = models.IntegerField()
    amount = models.IntegerField()
    description = models.TextField()
    photo = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "goods"

    def __str__(self):
        return f"{self.product_code} {self.name}"


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "roles"

    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"


class PickupPoint(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    building = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = "pickup_points"

    def __str__(self):
        return f"{self.index}, {self.city}, {self.street}, {self.building}"


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "order_statuses"

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    delivery_date = models.DateField()
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    delivery_code = models.IntegerField()
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = "orders"

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Good, on_delete=models.PROTECT)
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = "order_items"
