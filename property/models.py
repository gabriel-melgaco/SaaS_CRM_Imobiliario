from django.db import models



class Condominium(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField(null=True, blank=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return 'Condomínio '+ self.name


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.IntegerField(null=True, blank=True, unique=True)
    TYPE_CHOICES = [
        ('house', 'Casa'),
        ('apartment', 'Apartamento'),
        ('farm', 'Sítio'),
    ]
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    sell_disponibility = models.BooleanField()
    sell_reason_unavailability = models.CharField(max_length=200, blank=True, null=True)
    rental_disponibility = models.BooleanField()
    rental_reason_unavailability = models.CharField(max_length=200, blank=True)
    seasonal_disponibility = models.BooleanField()
    seasonal_reason_unavailability = models.CharField(max_length=200, blank=True)
    condominium = models.ForeignKey(Condominium, on_delete=models.PROTECT, related_name='properties', blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='property/', null=True, blank=True)

    def __str__(self):
        return 'IMÓVEL '+ str(self.code)
    
    
class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='property_photos/', null=True, blank=True)

    def __str__(self):
        return f'Foto do {self.property}'
