from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import customer,loan
import os
from datetime import datetime
from django.core.management import call_command
from decimal import Decimal
# Create your views here.

class dataingestionview(APIView):
    def post(self, request):
        # Define the file paths for customer and loan data
        customer_file_path = r"C:\Users\91975\Desktop\credit-approvel-system\credit_approvel_system\credit_approvel_app\customer_data.xlsx"
        loan_file_path = r"C:\Users\91975\Desktop\credit-approvel-system\credit_approvel_system\credit_approvel_app\loan_data.xlsx"

        # Check if the files exist
        if not os.path.exists(customer_file_path) or not os.path.exists(loan_file_path):
            return Response(
                {'error': 'One or both file paths do not exist.'},
                status=400
            )

        try:
            # Trigger the management command for data ingestion
            call_command('ingest_data', customer_file=customer_file_path, loan_file=loan_file_path)
            return Response({'message': 'Data ingestion tasks have been successfully completed.'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class customercreateview(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract fields from the incoming request
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            monthly_salary = request.data.get('monthly_salary')
            phone_number = request.data.get('phone_number')

            # Validate required fields
            if not first_name or not last_name or not monthly_salary or not phone_number:
                return Response({
                    'message': 'Missing required fields',
                    'errors': {
                        'first_name': 'This field is required.',
                        'last_name': 'This field is required.',
                        'monthly_salary': 'This field is required.',
                        'phone_number': 'This field is required.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Convert monthly_salary to float if it's not already
                monthly_salary = float(monthly_salary)
            except ValueError:
                return Response({
                    'message': 'Invalid value for monthly_salary',
                    'errors': {
                        'monthly_salary': 'Must be a valid number.'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            # Calculate approved_limit based on the monthly salary
            approved_limit = round(36 * monthly_salary, -5)  # rounded to nearest lakh

            # Create customer instance
            customer_instance = customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                monthly_salary=monthly_salary,
                phone_number=phone_number,
                approved_limit=approved_limit
            )

            # Return success response with the created customer data
            return Response({
                'message': 'Customer created successfully',
                'customer': {
                    'customer_id': customer_instance.customer_id,
                    'first_name': customer_instance.first_name,
                    'last_name': customer_instance.last_name,
                    'phone_number': customer_instance.phone_number,
                    'monthly_salary': customer_instance.monthly_salary,
                    'approved_limit': customer_instance.approved_limit
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'message': 'Error occurred while creating customer',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Checkeligibilityview(APIView):
    def post(self, request):
        try:
            # Parse request body and convert to Decimal for precision
            customer_id = request.data.get("customer_id")
            loan_amount = Decimal(request.data.get("loan_amount"))
            interest_rate = Decimal(request.data.get("interest_rate"))
            tenure = int(request.data.get("tenure"))

            # Fetch customer and loan data
            customer_obj = customer.objects.get(customer_id=customer_id)
            loan_objs = loan.objects.filter(customer_id=customer_id)

            # Calculate credit score
            past_loans_paid_on_time = sum([l.emis_paid_on_time for l in loan_objs])
            total_loans = loan_objs.count()
            current_year = datetime.now().year
            loans_in_current_year = loan_objs.filter(start_date__year=current_year).count()
            total_loan_volume = sum([Decimal(l.loan_amount) for l in loan_objs])

            # If sum of current loans exceeds approved limit, credit score is 0
            current_loan_sum = sum(
                [Decimal(l.loan_amount) for l in loan_objs if l.end_date > datetime.now().date()]
            )
            if current_loan_sum > Decimal(customer_obj.approved_limit):
                credit_score = 0
            else:
                credit_score = min(
                    100,
                    (past_loans_paid_on_time * 20)
                    - (total_loans * 5)
                    + (loans_in_current_year * 10)
                    + (total_loan_volume / Decimal(1000)),
                )

            # Check loan approval conditions
            monthly_salary = Decimal(customer_obj.monthly_salary)
            current_emis = sum(
                [Decimal(l.monthly_repayment) for l in loan_objs if l.end_date > datetime.now().date()]
            )
            monthly_installment = (
                loan_amount
                * (interest_rate / 100)
                / Decimal(12)
                * ((1 + (interest_rate / 100) / Decimal(12)) ** tenure)
                / (((1 + (interest_rate / 100) / Decimal(12)) ** tenure) - 1)
            )

            # Determine loan approval and adjust interest rate if necessary
            approval = False
            corrected_interest_rate = interest_rate
            if credit_score > 50:
                approval = True
            elif 30 < credit_score <= 50:
                corrected_interest_rate = max(Decimal(12), interest_rate)
                approval = corrected_interest_rate == interest_rate
            elif 10 < credit_score <= 30:
                corrected_interest_rate = max(Decimal(16), interest_rate)
                approval = corrected_interest_rate == interest_rate
            else:
                approval = False

            # Check EMI condition
            if current_emis + monthly_installment > Decimal(0.5) * monthly_salary:
                approval = False

            # Prepare response
            response_data = {
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": float(interest_rate),
                "corrected_interest_rate": float(corrected_interest_rate),
                "tenure": tenure,
                "monthly_installment": round(float(monthly_installment), 2),
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class createloanview(APIView):
    def post(self, request):
        try:
            # Parse request body
            customer_id = request.data.get("customer_id")
            loan_amount = Decimal(request.data.get("loan_amount"))
            interest_rate = Decimal(request.data.get("interest_rate"))
            tenure = int(request.data.get("tenure"))

            # Fetch customer data
            customer_obj = customer.objects.get(customer_id=customer_id)
            loan_objs = loan.objects.filter(customer_id=customer_id)

            # Calculate credit score
            past_loans_paid_on_time = sum([l.emis_paid_on_time for l in loan_objs])
            total_loans = loan_objs.count()
            current_year = datetime.now().year
            loans_in_current_year = loan_objs.filter(start_date__year=current_year).count()
            total_loan_volume = sum([Decimal(l.loan_amount) for l in loan_objs])

            current_loan_sum = sum(
                [Decimal(l.loan_amount) for l in loan_objs if l.end_date > datetime.now().date()]
            )
            if current_loan_sum > Decimal(customer_obj.approved_limit):
                credit_score = 0
            else:
                credit_score = min(
                    100,
                    (past_loans_paid_on_time * 20)
                    - (total_loans * 5)
                    + (loans_in_current_year * 10)
                    + (total_loan_volume / Decimal(1000)),
                )

            # Check loan approval conditions
            monthly_salary = Decimal(customer_obj.monthly_salary)
            current_emis = sum(
                [Decimal(l.monthly_repayment) for l in loan_objs if l.end_date > datetime.now().date()]
            )
            monthly_installment = (
                loan_amount
                * (interest_rate / 100)
                / Decimal(12)
                * ((1 + (interest_rate / 100) / Decimal(12)) ** tenure)
                / (((1 + (interest_rate / 100) / Decimal(12)) ** tenure) - 1)
            )

            approval = False
            corrected_interest_rate = interest_rate
            if credit_score > 50:
                approval = True
            elif 30 < credit_score <= 50:
                corrected_interest_rate = max(Decimal(12), interest_rate)
                approval = corrected_interest_rate == interest_rate
            elif 10 < credit_score <= 30:
                corrected_interest_rate = max(Decimal(16), interest_rate)
                approval = corrected_interest_rate == interest_rate
            else:
                approval = False

            if current_emis + monthly_installment > Decimal(0.5) * monthly_salary:
                approval = False
                message = "EMI exceeds allowed limit based on monthly salary."
            else:
                message = "Loan approved." if approval else "Loan not approved due to low credit score."

            # Save loan if approved
            loan_id = None
            if approval:
                loan_instance = loan.objects.create(
                    customer_id=customer_id,
                    loan_amount=loan_amount,
                    interest_rate=corrected_interest_rate,
                    tenure=tenure,
                    monthly_repayment=monthly_installment,
                    start_date=datetime.now(),
                    end_date=datetime.now().replace(year=datetime.now().year + (tenure // 12)),
                    emis_paid_on_time=0,
                )
                loan_id = loan_instance.loan_id

            # Prepare response
            response_data = {
                "loan_id": loan_id,
                "customer_id": customer_id,
                "loan_approved": approval,
                "message": message,
                "monthly_installment": round(float(monthly_installment), 2) if approval else None,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class viewloandetails(APIView):
    def get(self, request, loan_id):
        try:
            # Fetch the loan details
            loan_obj = loan.objects.get(loan_id=loan_id)
            
            # Fetch the customer details
            customer_obj = customer.objects.get(customer_id = loan_obj.customer_id)

            # Prepare response data
            response_data = {
                "loan_id": loan_obj.loan_id,
                "customer": {
                    "id": customer_obj.customer_id,
                    "first_name": customer_obj.first_name,
                    "last_name": customer_obj.last_name,
                    "phone_number": customer_obj.phone_number,
                },
                "loan_amount": float(loan_obj.loan_amount),
                "interest_rate": float(loan_obj.interest_rate),
                "monthly_installment": float(loan_obj.monthly_repayment),
                "tenure": loan_obj.tenure,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class viewloansbycustomer(APIView):
    def get(self, request, customer_id):
        try:
            # Fetch all loans for the customer
            loan_objs = loan.objects.filter(customer_id=customer_id)
            
            if not loan_objs:
                return Response({"message": "No active loans found for the customer"}, status=status.HTTP_404_NOT_FOUND)

            loan_list = []
            for loan_obj in loan_objs:
                # Calculate the number of repayments left
                repayments_left = loan_obj.tenure - ((datetime.now().year - loan_obj.start_date.year) * 12 + datetime.now().month - loan_obj.start_date.month)

                loan_list.append({
                    "loan_id": loan_obj.loan_id,
                    "loan_amount": float(loan_obj.loan_amount),
                    "interest_rate": float(loan_obj.interest_rate),
                    "monthly_installment": float(loan_obj.monthly_repayment),
                    "repayments_left": repayments_left
                })
            
            # Prepare response with the list of loans
            response_data = loan_list
            return Response(response_data, status=status.HTTP_200_OK)

        except customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)