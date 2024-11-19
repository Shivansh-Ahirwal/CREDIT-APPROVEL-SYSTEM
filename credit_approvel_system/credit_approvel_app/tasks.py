from celery import shared_task
import pandas as pd
from .models import customer, loan

@shared_task
def ingest_customer_data(file_path):
    print('entered the ingest customer method.')
    try:
        # Load Excel file into a DataFrame
        customer_data = pd.read_excel(file_path)
        # Iterate through rows and add to database
        for _, row in customer_data.iterrows():
            row_dict = row.to_dict()
            customer_instance = customer.objects.create(
                customer_id=row_dict['Customer ID'],
                first_name=row_dict['First Name'],
                last_name=row_dict['Last Name'],
                monthly_salary=row_dict['Monthly Salary'],
                phone_number=row_dict['Phone Number'],
                approved_limit=row_dict['Approved Limit']
            )
            if customer_instance:
                print('created customer instance.')
            customer_instance.save()
        return "Customer data ingested successfully."
    except Exception as e:
        return str(e)

@shared_task
def ingest_loan_data(file_path):
    try:
        # Load Excel file into a DataFrame
        loan_data = pd.read_excel(file_path)

        # Iterate through rows and add to database
        for _, row in loan_data.iterrows():
            row_dict = row.to_dict()
            customer = customer.objects.get(customer_id=row_dict['Customer Id'])
            loan_instance = loan.objects.create(
                customer_id= customer,
                loan_id = row_dict['Loan Id'],
                loan_amount= row_dict['Loan Amount'],
                tenure= row_dict['Tenure'],
                interest_rate = row_dict['Interest Rate'],
                monthly_repayment= row_dict['Monthly payment'],
                emis_paid_on_time= row_dict['EMIs paid on Time'],
                start_date= row_dict['Date of Approval'],
                end_date= row_dict['End Date'],
            )
            if loan_instance:
                print('created loan instance.')
        return "Loan data ingested successfully."
    except Exception as e:
        return str(e)

