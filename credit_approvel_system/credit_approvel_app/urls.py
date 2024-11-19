from django.urls import path
from .views import dataingestionview,customercreateview,Checkeligibilityview,createloanview,viewloandetails,viewloansbycustomer

urlpatterns = [
    path('ingest-data/', dataingestionview.as_view(), name='ingest-data'),
    path('register/', customercreateview.as_view(), name='register'),
    path("check-eligibility/", Checkeligibilityview.as_view(), name="check-eligibility"),
    path("create-loan/", createloanview.as_view(), name="create-loan"),
    path('view-loan/<int:loan_id>/', viewloandetails.as_view(), name='view-loan-by-loanid'),
    path('view-loans/<int:customer_id>/', viewloansbycustomer.as_view(), name='view-loans-by-customer'),
]