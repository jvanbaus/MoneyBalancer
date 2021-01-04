from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords


class Account(models.Model):

    L = "L"
    R = "R"

    account_sides = (
        (L, "Left"),
        (R, "Right"),
    )

    # Left Assests | Expenses
    # Right Liability | Equity | Revenue

    account_catagories = (
        (1, "Assest"),
        (2, "Liability"),
        (3, "Equity"),
        (4, "Revenue"),
        (5, "Expense"),
    )

    # Assests Checking | Petty cash | Inventory | Accounts receivable
    # Liability Payroll tax liabilities | Sales tax collected | Credit memo liability | Accounts payable
    # Expense Payroll | Insurance | Rent | Equipment | Cost of goods sold(COGS)
    # Equity Owner’s equity | Common stock | Retained earnings
    # Revenue Product sales | Earned interest | Miscellaneous incom

    account_subcatagories = (
        # Assests
        (1, "Checking"),
        (2, "Petty cash"),
        (3, "Inventory"),
        (4, "Accounts receivable"),
        # Liabilites
        (5, "Payroll tax liabilities"),
        (6, "Sales tax collected"),
        (7, "Credit memo liability"),
        (8, "Accounts payable"),
        # Equity
        (9, "Owner’s equity"),
        (10, "Common stock"),
        (11, "Retained earnings"),
        # Revenue
        (12, "Product sales"),
        (13, "Earned interest"),
        (14, "Miscellaneous income"),
        # Expenses
        (15, "Payroll"),
        (16, "Insurance"),
        (17, "Rent"),
        (18, "Equipment"),
        (19, "Cost of goods sold(COGS)"),
    )

    acccount_statements = (
        (1, "Income Sheet"),
        (2, "Balance Sheet"),
        (3, "Retained Earnings"),
    )

    A = "A"
    D = "D"
    P = "P"

    acccount_statuses = (
        (A, "Active"),
        (D, "Deactive"),
        (P, "Pending"),
    )

    account_name = models.CharField(unique=True, max_length=50, null=True)
    account_number = models.PositiveIntegerField(

        unique=True,
        null=True,
        validators=[MinValueValidator(
            10000000), MaxValueValidator(999999999999)],
    )
    account_description = models.TextField(blank=True)
    account_side = models.CharField(
        choices=account_sides, max_length=1, default=L)
    account_catagory = models.IntegerField(
        choices=account_catagories, null=True)
    account_subcatagory = models.IntegerField(
        choices=account_subcatagories, null=True)
    account_inital_balance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    account_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    account_debit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    account_credit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    account_creation_date = models.DateTimeField(auto_now_add=True)
    account_modified_date = models.DateTimeField(auto_now=True)
    account_modified_user = models.IntegerField(null=True, blank=True)
    account_statement = models.IntegerField(
        choices=acccount_statements, null=True)
    account_status = models.CharField(
        choices=acccount_statuses, max_length=1, default=A
    )
    account_comment = models.TextField(blank=True)

    history = HistoricalRecords(
        table_name='accounting_eventlog',
        custom_model_name='AccountingEventLog',
        # excluded_fields=['account_creation_date'],
    )

    def __str__(self):
        return str(self.account_number)


# class EventsLog(models.Model):
#     pass
    # event_name = models.CharField(max_length=50)
    # event_description = models.TextField(blank=True)
    # event_balance = models.DecimalField(
    #     decimal_places=2, max_digits=10, null=True)
    # event_status = models.CharField(max_length=1)
    # event_date = models.DateTimeField(auto_now_add=True)
    # event_user = models.IntegerField(null=True)

    # account = models.ForeignKey("Account", on_delete=models.CASCADE)


class Journal(models.Model):

    A = "A"
    R = "R"
    P = "P"
    V = "V"
    C = "C"

    journal_statuses = (
        (A, "Approved"),
        (R, "Rejected"),
        (P, "Pending")
    )

    journal_types = (
        (A, "Adjusting"),
        (R, "Regular"),
        (V, "Reversing"),
        (C, "Closing"),
    )

    journal_status = models.CharField(
        choices=journal_statuses, max_length=1, default=P
    )
    journal_type = models.CharField(
        choices=journal_types, max_length=1, default=R
    )
    journal_creation_date = models.DateTimeField(auto_now_add=True)
    journal_description = models.TextField(blank=True)
    journal_comment = models.TextField(blank=True)
    journal_file = models.FileField(blank=True)
    journal_user = models.IntegerField(null=True, blank=True)
    journal_account_number_debits = models.JSONField(null=True)
    journal_account_name_debits = models.JSONField(null=True)
    journal_account_number_credits = models.JSONField(null=True)
    journal_account_name_credits = models.JSONField(null=True)
    journal_account_debits = models.JSONField(null=True)
    journal_account_credits = models.JSONField(null=True)

    # account = models.ManyToManyField(Account)
