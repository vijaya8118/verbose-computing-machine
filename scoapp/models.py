from django.db import models
from django.utils.translation import gettext as _
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser

############### USER REGISTRATION ###########################

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=255)  # Email field
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Contact number (can store numbers and optional)
    
    def __str__(self):
        return self.name

class Domain(DomainMixin):
    pass

class Members(AbstractUser):
    username = models.CharField(max_length = 50, blank = False, null = False, unique = True)
    email = models.EmailField(_('email address'), unique = True)
    phone_no = models.CharField(max_length = 10)
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, default='admin') 

################## models ####################


class Add_item_model(models.Model):
    product=models.CharField(max_length=100)
    rate = models.DecimalField('Selling rate',decimal_places=2,max_digits=6,null=False,default=0)
    rate_purch = models.DecimalField('Purchase rate',decimal_places=2,max_digits=6,null=False,default=0)
    image = models.ImageField('Insert image', upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.product

class Common_InfoShop(models.Model):
    name=models.CharField('Buyer name',max_length=40,default='nil')
    address=models.TextField('address',max_length=90,default='nil')
    phone=models.CharField('Phone Number',max_length=10,default='nil')
    gst=models.CharField('GST Number',max_length=11,default='nil')

    class Meta:
        abstract=True

    def __str__(self):
        return self.name

class Customer(Common_InfoShop):
    def __str__(self):
        return self.name

class Seller(Common_InfoShop):
    def __str__(self):
        return self.name

class Purchase_model(models.Model):
    date=models.DateTimeField( 'date',auto_now_add=True)
    date1=models.DateField( 'date',auto_now_add=True)
    user=models.CharField('User',max_length=30,null=False,default='emp')
    selbuy = models.ForeignKey(Seller,on_delete=models.DO_NOTHING,null=True)
    num=models.AutoField(auto_created = True,primary_key = True)
    STATUS = (
        ('cash',_('cash')),
        ('UPI',_('UPI')),
        ('credit',_('credit')),


    )
    mode=models.CharField('Mode',max_length=15,null=True,choices=STATUS,default='nil',blank=True)
    ####
    product=models.ForeignKey(Add_item_model,on_delete=models.DO_NOTHING,null=True,related_name="Product1:+",default='name')
    qty = models.DecimalField('Quantity',decimal_places=2,max_digits=6,null=False,default=0)
    rate = models.DecimalField('Rate',decimal_places=2,max_digits=6,null=False,default=0)

    amt = models.DecimalField("Amt",null=False,max_digits=9,decimal_places=2,default=0)

    # def save(self, *args, **kwargs):
    #     self.user = request.user.username
    #     super().save(*args, **kwargs)

class PurchaseBook(models.Model):
    date = models.DateTimeField("Date",auto_now_add=True)
    date1=models.DateField( 'date',auto_now_add=True)
    selbuy = models.ForeignKey(Seller,on_delete=models.DO_NOTHING,null=True)

    amt= models.DecimalField('Amount Paid',null=False,max_digits=7,decimal_places=2,default=0)

    STATUS = (
        ('cash',_('cash')),
        ('UPI',_('UPI')),
    )
    mode=models.CharField(' mode',max_length=15,null=False,choices=STATUS,default='nil')
    comment = models.TextField("narration",max_length=150,null=True)


class CashBook(models.Model):
    date = models.DateTimeField("Date",auto_now_add=True)
    date1=models.DateField( 'date',auto_now_add=True)
    selbuy = models.ForeignKey(Customer,on_delete=models.DO_NOTHING,null=False,blank=False)

    amt= models.DecimalField('Amount Paid',null=False,max_digits=7,decimal_places=2,default=0)

    STATUS = (
        ('cash',_('cash')),
        ('UPI',_('UPI')),
    )
    mode=models.CharField(' mode',max_length=15,null=False,choices=STATUS,default='nil')
    comment = models.TextField("narration",max_length=150,null=True)
 
class Invoice_model(models.Model):
    date=models.DateTimeField( 'date',auto_now_add=True)
    date1=models.DateField( 'date',auto_now_add=True)
    selbuy = models.ForeignKey(Customer,on_delete=models.DO_NOTHING,null=False,blank=False)
    num=models.AutoField(auto_created = True,primary_key = True,serialize = False, verbose_name ='Bill num')
    billnum= models.IntegerField("Bill Number",null=False)
    STATUS = (
        ('cash',_('cash')),
        ('UPI',_('UPI')),
        ('credit',_('credit')),

    )
    mode=models.CharField('Mode',max_length=15,null=False,blank=False,choices=STATUS,default='nil')
    ####
    product=models.ForeignKey(Add_item_model,related_name='item',on_delete=models.DO_NOTHING,null=False,blank=False,verbose_name="prod:")
    qty = models.DecimalField('quantity',decimal_places=2,max_digits=6,null=False,default=0)
    rate = models.DecimalField("Rate",null=False,max_digits=6,decimal_places=2,default=0)
    amt = models.DecimalField("Amt",null=False,max_digits=9,decimal_places=2,default=0)

