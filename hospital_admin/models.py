from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=50,unique=True,primary_key=True)
    emp_phone = models.CharField(max_length=10,unique=True)
    emp_dob = models.DateField()
    emp_gender = models.CharField(max_length=10)
    emp_type = models.CharField(max_length=50)
    emp_profile_picture = models.ImageField(upload_to='profile_pictures/',null=True, blank=True)
    
    # EMP_TYPE_CHOICES = {
    #     'Receptionist': 'RP',
    #     'Laboratory_Technician': 'LT',
    #     'Junior_Doctor': 'JD',
    #     'Consultant_Doctor': 'CD',
    # }
    
    # def save(self, *args, **kwargs):
    #     if not self.emp_id:
    #         prefix = 'CCHC'
    #         emp_type_code = self.EMP_TYPE_CHOICES.get(self.emp_type, 'XX')
    #         count = Employee.objects.filter(emp_type=self.emp_type).count() + 1
    #         self.emp_id = f"{prefix}{emp_type_code}{count:03d}"
    #         self.user.username = self.emp_id
    #     super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    
    # emp_first_name = models.CharField(max_length=50)
    # emp_last_name = models.CharField(max_length=50)
    # emp_email = models.EmailField(max_length=50,unique=True)
    
    # emp_address = models.CharField(max_length=100)
    
    