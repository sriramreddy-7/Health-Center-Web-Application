from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils import timezone
import os

class PatientPrimaryData(models.Model):
    patient_id = models.CharField(max_length=16, unique=True)
    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    patient_dob = models.DateField()
    patient_gender = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=17)
    guardian_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    registration_date = models.DateField(default=timezone.now)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address=models.TextField(max_length=250, default='')

    def save(self, *args, **kwargs):
        if not self.patient_id:
            date_format = timezone.now().strftime('%Y%m%d')
            today_patient_count = PatientPrimaryData.objects.filter(
                registration_date__exact=timezone.now().date()
            ).count() + 1

            # Get the previous patient ID
            previous_patient = PatientPrimaryData.objects.filter(
                patient_id__startswith=f'cchc{date_format}'
            ).order_by('-patient_id').first()

            if previous_patient:
                previous_count = int(previous_patient.patient_id[-4:])
                today_patient_count = max(today_patient_count, previous_count + 1)

            self.patient_id = f'CCHC{date_format}{today_patient_count:04d}'

        super(PatientPrimaryData, self).save(*args, **kwargs)

    def __str__(self):
        return self.patient_id

class PHR(models.Model):
    patient = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now_add=True)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    pulse = models.CharField(max_length=100)
    bp = models.CharField(max_length=100)
    is_diabetic = models.BooleanField(default=False)
    diabetic_level = models.CharField(max_length=100, blank=True, null=True)
    phi = models.TextField(max_length=1000)
    pov = models.TextField(max_length=300)
    remarks = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.patient}"

# class Appointment(models.Model):
#     appointment_date = models.DateField(default=timezone.now)
#     new_patient_count = models.PositiveIntegerField(default=0)
#     old_patient_count = models.PositiveIntegerField(default=0)
#     total_appointment_count = models.PositiveIntegerField(default=0)

#     def save(self, *args, **kwargs):
#         if self.appointment_date.date() == timezone.now().date():
#             self.new_patient_count += 1
#         else:
#             self.old_patient_count += 1
#         self.total_appointment_count = self.new_patient_count + self.old_patient_count
#         super(Appointment, self).save(*args, **kwargs)

# from django.db import models
# from django.utils import timezone

# class FT(models.Model):
#     patient_id = models.CharField(max_length=16)
#     appointment_date = models.DateField(default=timezone.now)
#     is_new_patient = models.BooleanField(default=True)
#     patient_token = models.IntegerField(default=0)

#     def save(self, *args, **kwargs):
#         if not self.pk:  # Only on creation of a new instance
#             today = timezone.now().date()
#             patient_count = FT.objects.filter(patient_id__contains=f'CCHC{today.strftime("%Y%m%d")}').count()
#             self.token_number = patient_count + 1

#             patient_id_date = self.patient_id[4:12]
#             patient_id_date = timezone.datetime.strptime(patient_id_date, "%Y%m%d").date()

#             if today == patient_id_date:
#                 self.is_new_patient = True
#             else:
#                 self.is_new_patient = False

#             self.patient_id = f'CCHC{self.appointment_date.strftime("%Y%m%d")}{str(self.token_number).zfill(4)}'
#             self.check_duplicate_appointment()

#         super(FT, self).save(*args, **kwargs)

#     def check_duplicate_appointment(self):
#         if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date).exists():
#             raise ValueError("Duplicate appointment for the same patient ID and date.")

#         if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date - timezone.timedelta(days=1)).exists():
#             raise ValueError("Appointment already booked for the same patient ID on the previous day.")

#     def __str__(self):
#         return self.patient_id

from django.db import models
from django.utils import timezone

class FT(models.Model):
    patient_id = models.CharField(max_length=16, unique=True,primary_key=True)
    appointment_date = models.DateField(default=timezone.now)
    is_new_patient = models.BooleanField(default=True)
    patient_token = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation of a new instance
            today = timezone.now().date()
            patient_count = FT.objects.filter(patient_id__contains=f'CCHC{today.strftime("%Y%m%d")}').count()
            self.patient_token = patient_count + 1

            patient_id_date = self.patient_id[4:12]
            patient_id_date = timezone.datetime.strptime(patient_id_date, "%Y%m%d").date()

            if today == patient_id_date:
                self.is_new_patient = True
            else:
                self.is_new_patient = False

            self.check_duplicate_appointment()

        super(FT, self).save(*args, **kwargs)

    def check_duplicate_appointment(self):
        if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date).exists():
            raise ValueError("Duplicate appointment for the same patient ID and date.")

        if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date - timezone.timedelta(days=1)).exists():
            raise ValueError("Appointment already booked for the same patient ID on the previous day.")

    def __str__(self):
        return self.patient_id

def get_report_upload_path(instance, filename):
        # Generate the new filename based on the patient_id
        new_filename = f"{instance.appointment_id}.png"
        # Return the complete upload path
        return f"reports/{new_filename}"
    
    # filename, _ = os.path.splitext(filename)
    # patient_id = str(instance.patient_id)
    # timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    # new_filename = f"{patient_id}_{timestamp}.png"
    # return f"{new_filename}"
    
# def get_upload_path(instance, filename):
#     filename, _ = os.path.splitext(filename)
#     patient_id = str(instance.patient_id)
#     timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
#     new_filename = f"{patient_id}_{timestamp}.png"
#     return os.path.join('reports', new_filename)


class RP(models.Model):
    patient_id = models.CharField(max_length=16)
    report_file = models.FileField(upload_to=get_report_upload_path)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report for Patient ID: {self.patient_id}"

    # def get_report_upload_path(instance, filename):
    #     new_filename = f"{instance.patient_id}.pdf"
    #     return f"reports/{new_filename}"




# class PR(models.Model):
#     patient_id = models.CharField(max_length=16)
#     report_file = models.FileField(upload_to=get_report_upload_path)
#     uploaded_at = models.DateTimeField(default=timezone.now)
#     report_type = models.CharField(max_length=50)
#     doctor_name = models.CharField(max_length=100)
#     is_urgent = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Report for Patient ID: {self.patient_id}"





# class PatientCount(models.Model):
#     date = models.DateField(default=timezone.now)
#     male_count = models.PositiveIntegerField(default=0)
#     female_count = models.PositiveIntegerField(default=0)
#     total_count = models.PositiveIntegerField(default=0)
#     patient = models.ForeignKey(PatientPrimaryData, on_delete=models.CASCADE)

#     @classmethod
#     def update_counts(cls, patient):
#         date_format = timezone.now().date()
#         patient_count = cls.objects.filter(date=date_format).first()

#         if not patient_count:
#             patient_count = cls(date=date_format)

#         if patient.patient_gender == 'Male':
#             patient_count.male_count += 1
#         elif patient.patient_gender == 'Female':
#             patient_count.female_count += 1

#         patient_count.total_count += 1
#         patient_count.save()


# class PatientVisit(models.Model):
#     patient = models.ForeignKey(PatientPrimaryData, on_delete=models.CASCADE)
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     visit_date = models.DateField(auto_now_add=True)
#     visit_count = models.PositiveIntegerField(default=0)

#     def increment_visit_count(self):
#         self.visit_count += 1
#         self.save()

# class Visit(models.Model):
#     patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
#     patient_token = models.CharField(max_length=10, unique=True)
#     appointment_id = models.CharField(max_length=15, unique=True, primary_key=True)
#     visit_date = models.DateField()
#     doctor_name = models.CharField(max_length=100)
#     patient_type = models.CharField(max_length=100)
#     doctor_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     gst = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     today_date = models.DateTimeField(default=timezone.now)

#     def save(self, *args, **kwargs):
        
#         if not self.patient_token:
#             max_count = Visit.objects.filter(visit_date=self.visit_date).count() + 1
#             self.patient_token = f"{max_count:03d}"
        
        
#         if not self.appointment_id:
#             today = timezone.localdate()
#             count = Visit.objects.filter(visit_date=today).count() + 1
#             formatted_date = today.strftime("%d%m%y")
#             self.appointment_id = f"AP{formatted_date}{count:03d}"
        
#         super().save(*args, **kwargs)
        


# class Visit(models.Model):
#     patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
#     patient_token = models.CharField(max_length=10)
#     appointment_id = models.CharField(max_length=15, unique=True, primary_key=True)
#     visit_date = models.DateField()
#     doctor_name = models.CharField(max_length=100)
#     patient_type = models.CharField(max_length=100)
#     doctor_fee = models.DecimalField(max_digits=10, decimal_places=2)
#     gst = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     today_date = models.DateTimeField(default=timezone.now)

#     def save(self, *args, **kwargs):
#         if not self.patient_token:
#             # Get the maximum patient_token for the current visit_date
#             max_token = Visit.objects.filter(visit_date=self.visit_date).aggregate(models.Max('patient_token'))['patient_token__max']
            
#             # Check if there is an existing token for the visit_date
#             if max_token is None:
#                 # Set the initial patient_token as "001" for a new visit_date
#                 self.patient_token = "001"
#             else:
#                 # Split the last used token into count and date
#                 last_token, last_visit_date = max_token.split('-')
                
#                 # Check if the last_visit_date matches the current visit_date
#                 if last_visit_date == self.visit_date.strftime("%Y%m%d"):
#                     # Get the token count from the last used token
#                     token_count = int(last_token)
#                     if token_count < 999:
#                         # Increment the token count by 1 if it's less than 999
#                         token_count += 1
#                     else:
#                         # Set the token count as 1 if it reaches 999
#                         token_count = 1
#                 else:
#                     # Set the token count as 1 for a new visit_date
#                     token_count = 1
                
#                 # Format the count as a 3-digit number
#                 formatted_count = f"{token_count:03d}"
                
#                 # Set the patient_token using the formatted count and visit_date
#                 self.patient_token = formatted_count + "-" + self.visit_date.strftime("%Y%m%d")
        
#         if not self.appointment_id:
#             today = timezone.localdate()
            
#             # Check if the visit_date is different from today's date
#             if self.visit_date != today:
#                 # If the visit_date is different, reset the count to 1
#                 count = 1
#             else:
#                 # Otherwise, get the count of visits for today's date
#                 count = Visit.objects.filter(visit_date=today).count() + 1
            
#             # Format the date as "ddmmyy"
#             formatted_date = today.strftime("%d%m%y")
            
#             # Set the appointment_id using the formatted date and count
#             self.appointment_id = f"AP{formatted_date}{count:03d}"
        
#         super().save(*args, **kwargs)
    
#     class Meta:
#         unique_together = ('patient_token', 'visit_date')

class Visit(models.Model):
    appointment_id = models.CharField(max_length=12, unique=True,primary_key=True)
    patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    visit_date = models.DateField()
    doctor_name = models.CharField(max_length=50)
    patient_type = models.CharField(max_length=20)
    doctor_fee = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    today_date = models.DateField(auto_now_add=True)
    patient_token = models.CharField(max_length=6)

    def save(self, *args, **kwargs):
        # Convert visit_date to a date object
        visit_date = datetime.strptime(self.visit_date, '%Y-%m-%d').date()
        # Generate the AppointmentID and patient token count
        last_count = Visit.objects.filter(visit_date=visit_date).count()
        current_count = last_count + 1
        self.appointment_id = f"AP{visit_date.strftime('%d%m%y')}{current_count:03}"
        self.patient_token = f"{current_count:03}"
        
        # Ensure the count does not exceed 999
        if current_count > 999:
            raise ValueError("Appointment ID count exceeded the maximum limit.")

        super().save(*args, **kwargs)
        

class JDD(models.Model):
    appointment_id = models.OneToOneField('Visit', on_delete=models.CASCADE, primary_key=True)
    patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now_add=True)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    pulse = models.CharField(max_length=100)
    bp = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=100)
    is_diabetic = models.BooleanField(default=False)
    diabetic_level = models.CharField(max_length=100, blank=True, default=None)
    phi = models.TextField(max_length=1000)
    pov = models.TextField(max_length=300)
    remarks = models.TextField(max_length=1000)
        
#class MedicalTest(models.Model):
class Test(models.Model):
    appointment_id = models.OneToOneField('Visit', on_delete=models.CASCADE, primary_key=True)
    patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    remark=models.CharField(max_length=250,null=True)
    test1=models.CharField(max_length=100,null=True)
    test2=models.CharField(max_length=100,null=True)
    test3=models.CharField(max_length=100,null=True)
    test3=models.CharField(max_length=100,null=True)
    test4=models.CharField(max_length=100,null=True)
    test5=models.CharField(max_length=100,null=True)
    test6=models.CharField(max_length=100,null=True)
    test7=models.CharField(max_length=100,null=True)
    test8=models.CharField(max_length=100,null=True)
    test9=models.CharField(max_length=100,null=True)
    test10=models.CharField(max_length=100,null=True)
    test11=models.CharField(max_length=100,null=True)
    test12=models.CharField(max_length=100,null=True)
    test13=models.CharField(max_length=100,null=True)
    test14=models.CharField(max_length=100,null=True)
    test15=models.CharField(max_length=100,null=True)
    test16=models.CharField(max_length=100,null=True)
    test17=models.CharField(max_length=100,null=True)
    test18=models.CharField(max_length=100,null=True)
    date_and_time = models.DateTimeField(auto_now_add=True)
    
    

class MedicalTestResult(models.Model):
    appointment_id = models.CharField(max_length=20, unique=True, primary_key=True)
    patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    report_file = models.ImageField(upload_to=get_report_upload_path)
    uploaded_datetime = models.DateTimeField(auto_now_add=True)

    def get_report_upload_path(instance, filename):
        new_filename = f"{instance.appointment_id}.pdf"
        return f"reports/{new_filename}"  
    
    
    
class TestForm(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class PatientTest(models.Model):
    appointment_id = models.OneToOneField('Visit', on_delete=models.CASCADE, primary_key=True)
    patient_id = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    tests = models.ManyToManyField(TestForm)
    date_prescribed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_id} - {self.appointment_id}"
    
    

class TestReport(models.Model):
    patient_test = models.ForeignKey(PatientTest, on_delete=models.CASCADE, related_name='test_reports')
    test = models.ForeignKey(TestForm, on_delete=models.CASCADE)
    report = models.FileField(upload_to='test_reports/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.test.name} (Patient: {self.patient_test.patient_id})"
    
    
    
class Medicine(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True)
    medicine_type = models.CharField(max_length=100, blank=True)
    dosage_form = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    side_effect = models.TextField(blank=True)
    dosage_strength =models.TextField(blank=True)
    
    def __str__(self):
        return self.name