import pandas as pd
from django.core.management.base import BaseCommand
from credit_approvel_app.models import customer, loan

class Command(BaseCommand):
    help = 'Ingest data from Excel files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--customer_file', type=str, help='Path to the customer data Excel file'
        )
        parser.add_argument(
            '--loan_file', type=str, help='Path to the loan data Excel file'
        )

    def handle(self, *args, **kwargs):
        customer_file = kwargs.get('customer_file')
        loan_file = kwargs.get('loan_file')

        if customer_file:
            self.ingest_customer_data(customer_file)

        if loan_file:
            self.ingest_loan_data(loan_file)

        self.stdout.write(self.style.SUCCESS('Data ingestion completed successfully!'))

    def ingest_customer_data(self, file_path):
        self.stdout.write(f'Ingesting customer data from {file_path}...')
        try:
            data = pd.read_excel(file_path)
            for _, row in data.iterrows():
                row_dict = row.to_dict()
                customer.objects.update_or_create(
                    customer_id=row_dict['Customer ID'],
                    first_name=row_dict['First Name'],
                    last_name=row_dict['Last Name'],
                    monthly_salary=row_dict['Monthly Salary'],
                    phone_number=row_dict['Phone Number'],
                    approved_limit=row_dict['Approved Limit']
                )
            self.stdout.write(self.style.SUCCESS('Customer data ingested successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error ingesting customer data: {e}'))

    def ingest_loan_data(self, file_path):
        self.stdout.write(f'Ingesting loan data from {file_path}...')
        try:
            data = pd.read_excel(file_path)
            for _, row in data.iterrows():
                row_dict = row.to_dict()
                loan.objects.update_or_create(
                    customer_id= row_dict['Customer ID'],
                    loan_id = row_dict['Loan ID'],
                    loan_amount= row_dict['Loan Amount'],
                    tenure= row_dict['Tenure'],
                    interest_rate = row_dict['Interest Rate'],
                    monthly_repayment= row_dict['Monthly payment'],
                    emis_paid_on_time= row_dict['EMIs paid on Time'],
                    start_date= row_dict['Date of Approval'],
                    end_date= row_dict['End Date'],
                )
            self.stdout.write(self.style.SUCCESS('Loan data ingested successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error ingesting loan data: {e}'))
