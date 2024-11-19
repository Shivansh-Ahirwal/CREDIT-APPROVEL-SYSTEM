from django.db import models

# Create your models here.
class customer(models.Model):
    customer_id = models.AutoField(primary_key=True)  
    first_name = models.CharField(max_length=100)  
    last_name = models.CharField(max_length=100)  
    phone_number = models.CharField(max_length=15, unique=True)  
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)  
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"

class loan(models.Model):
    customer_id = models.IntegerField()
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer_id}"