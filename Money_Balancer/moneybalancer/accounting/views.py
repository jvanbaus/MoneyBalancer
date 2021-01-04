from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Journal
from .filters import journalFilter
from .filters import accountFilter

from django.contrib import messages

from register.models import CustomUser
from django.core.mail import send_mail

from datetime import datetime
import random
import re
import decimal


random.seed(datetime.now())


def home(request):
    return render(request, "accounting/home.html")


def deactive(request, id):
    account = Account.objects.get(id=id)
    print(account.account_balance)
    if int(account.account_balance) <= 0:
        account.account_status = 'D'
        account.save()
        print("Deactive")
        return redirect('account')
    else:
        messages.error(request, "Can not be deactived")
        return redirect('account')

    return messages.error(request, "Problem has occured!")


@login_required
def ledger(request, id):
    accountLedger = Account.objects.get(id=id)
    journals = Journal.objects.all()
    journal_entry_debit = []
    journal_entry_credit = []
    balance = []
    # b = 0
    # Messy code needs to be cleaned up

    for x in journals:
        if x.journal_status == 'A':
            # balance.append(0)
            # print(x.id, "First")
            check_id_out = 0
            for n in x.journal_account_numbers:
                p = x.journal_account_numbers
                r = int(n)
                i = p.index(n)

                d = x.journal_account_debits[i]
                c = x.journal_account_credits[i]

                if r == accountLedger.account_number:

                    journal_entry_debit.append(d)
                    journal_entry_credit.append(c)

                    both = sum(journal_entry_debit) - sum(journal_entry_credit)

                    balance.append(both)

                    # print(balance[x.id - 1])
                    # print(len(balance))
                    # if journal_entry_debit != 0:
                    #     if len(balance) != 0:
                    #         b = balance[len(balance)-1] + d
                    #         print(b)

                    #     else:
                    #         b = 0 + d
                    #         print("hit")

                    # else:
                    #     if len(balance) != 0:
                    #         b = c - balance[len(balance)-1]
                    #         print(b)

                    #     else:
                    #         b = c - 0
                    #         print("hit")

                    # both = sum(journal_entry_debit) - sum(journal_entry_credit)
                    # print(both)
                    # balance.append(both)
                    # o = sum(journal_entry_debit)
                    # z = sum(journal_entry_credit)
                    # print("debit: ", o)
                    # print("credit:", z)
                    # print(b)

                    '''
                    To be clear I did not understand the domain at this time
                    Transaction can not be debited twice in the same transcation
                    this code would work if it could be
                    '''

                    # print(x.id, "Second")
                    # check_id_in = 1

                    # print(journal_entry_debit)
                    # if check_id_out == check_id_in:
                    #     print(x.id)
                    #     y = journal_entry_debit[x.id-1]
                    #     print(y)
                    #     journal_entry_debit.pop(x.id-1)
                    #     print(journal_entry_debit)
                    #     journal_entry_debit.append([d, y])
                    #     print(journal_entry_debit)
                    # else:
                    #     journal_entry_debit.append(d)
                    #     journal_entry_debit.append(d)
                    #     journal_entry_credit.append(c)

                    # journal_entry_debit.append(
                    #     x.journal_account_debits[i])
                    # journal_entry_credit.append(
                    #     x.journal_account_credits[i])

                    # d = x.journal_account_debits[i]
                    # c = x.journal_account_credits[i]

                    # print(journal_entry_debit, journal_entry_credit)
                    # check_id_out = check_id_out + 1
                    # check_id_in = check_id_in + 1
                    # print("Outside Number: ", check_id_out)
                    # print("Inside Number: ", check_id_in)
                    # print(id_stuff)

                    # print(x.journal_account_debits[i])
                    # print(x.journal_account_credits[i])
            else:
                pass

    items = zip(journals, journal_entry_debit, journal_entry_credit, balance)
    context = {
        'accountLedger': accountLedger,
        # 'journals': journals,
        'items': items,
    }
    return render(request, "accounting/ledger.html", context)


def edit(request, id):

    accountEdit = Account.objects.get(id=id)

    context = {
        'accountEdit': accountEdit
    }

    if request.method == "POST":
        # event = EventsLog()

        user = request.user.id
        # number = request.POST.get("accountnumber")
        name = request.POST.get("accountname")
        des = request.POST.get("accountdes")
        catagory = request.POST.get("accountcatagory")
        subcatagory = request.POST.get("accountsubcatagory")
        # side = request.POST.get("normalside")
        # initial = request.POST.get("accountinital")
        balance = request.POST.get("accountbalance")
        # debit = request.POST.get("accountdebit")
        # credit = request.POST.get("accountcredit")
        statement = request.POST.get("accountstatement")
        status = request.POST.get("accountstatus")
        com = request.POST.get("accountcom")

        # account num auto assigned
        #  num = catagory + '000' + str(random.randint(000, 999)) + \
        #   '000'

        side = ""
        # Side catagory left | right
        # Logic off somewhere
        if catagory == "1" or catagory == "5":
            side = "L"
            print("Left")
        else:
            side = "R"

            # print(side)
            # Check subcatagory later
            # if catagory == 1:
            #     if subcatagory != 1 or subcatagory != 2 or subcatagory != 3 or subcatagory != 4:
            #         pass

        # Used to check empty balance
        if balance != "":
            balance = balance
        else:
            balance = accountEdit.account_balance

        # Used to check name| name has to be unique
        if name == "":
            pass
        else:
            accountEdit.account_name = name

        # a.account_number = int(num)
        # accountEdit.account_name = name
        accountEdit.account_description = des
        accountEdit.account_side = side
        accountEdit.account_catagory = catagory
        accountEdit.account_subcatagory = subcatagory
        # accountEdit.account_inital_balance = initial
        accountEdit.account_balance = balance
        # accountEdit.account_debit = debit
        # accountEdit.account_credit = credit
        accountEdit.account_modified_date = datetime.now()
        accountEdit.account_modified_user = user
        accountEdit.account_statement = statement
        accountEdit.account_status = status
        accountEdit.account_comment = com

        accountEdit.save()

        # event.account = accountEdit
        # event.save()

        messages.success(request, "Account created!")
        return redirect('account')

    return render(request, "accounting/edit.html", context)


def sendemail(request):
    users = CustomUser.objects.all()

    context = {
        'users': users,
    }

    if request.method == "POST":
        user_email = request.user.email

        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        try:
            send_mail(
                subject,
                message,
                'movethewaters@gmail.com',
                [email],
                fail_silently=False,
            )
        except:
            messages.error(request, "Email could not be sent")

    return render(request, "accounting/sendemail.html", context)


@login_required
def account(request):

    accounts = Account.objects.all()

    myFilter = accountFilter(request.GET, queryset=accounts)
    accounts = myFilter.qs

    context = {
        'accounts': accounts, 'myFilter': myFilter
    }

    if request.method == "POST":
        a = Account()
        # e = EventsLog()

        # number = request.POST.get("accountnumber")
        name = request.POST.get("accountname")
        des = request.POST.get("accountdes")
        catagory = request.POST.get("accountcatagory")
        subcatagory = request.POST.get("accountsubcatagory")
        # side = request.POST.get("normalside")
        initial = request.POST.get("accountinital")
        # balance = request.POST.get("accountbalance")
        # debit = request.POST.get("accountdebit")
        # credit = request.POST.get("accountcredit")
        statement = request.POST.get("accountstatement")
        status = request.POST.get("accountstatus")
        com = request.POST.get("accountcom")

        # account num auto assigned
        # num = catagory + str(random.randint(0000000, 999999999))
        num = catagory + '000' + str(random.randint(000, 999)) + \
            '000'

        side = ""
        # Side catagory left | right
        # Logic off somewhere
        if catagory == "1" or catagory == "5":
            side = "L"
            # print("Left")
        else:
            side = "R"

        # print(side)
        # Check subcatagory later
        # if catagory == 1:
        #     if subcatagory != 1 or subcatagory != 2 or subcatagory != 3 or subcatagory != 4:
        #         pass

        a.account_number = int(num)
        a.account_name = name
        a.account_description = des
        a.account_side = side
        a.account_catagory = catagory
        a.account_subcatagory = subcatagory
        a.account_inital_balance = initial
        a.account_balance = initial
        # a.account_debit = debit
        # a.account_credit = credit
        a.account_statement = statement
        a.account_status = status
        a.account_comment = com

        a.save()

        # print("this is the account id: ",  a.id)
        # theAccount = Account.objects.get(id=a.id)
        # e.account = theAccount
        # e.event_account_description = theAccount.account_description
        # e.event_account_name = theAccount.account_name
        # e.event_account_status = theAccount.account_status
        # e.event_account_balance = theAccount.account_balance

        # e.save()

        messages.success(request, "Account created!")

    return render(request, "accounting/accounts.html", context)


@login_required
def event(request):

    events = Account.history.all()

    context = {

        'events': events,

    }

    return render(request, "accounting/event.html", context)


@login_required
def some_template(request):

    return render(request, "accounting/some_template.html")


def approve(request, id):

    journal = Journal.objects.get(id=id)
    accounts = Account.objects.all()
    c = 0
    # x = account.get(account_number=journal.journal_account_numbers[0])

    for x in journal.journal_account_numbers:
        account = accounts.get(account_number=x)
        print(account)
        if journal.journal_account_debits[c] != 0:
            account.account_balance = account.account_balance + \
                decimal.Decimal(journal.journal_account_debits[c])
            print(account.account_balance)
        else:
            account.account_balance = account.account_balance + \
                decimal.Decimal(journal.journal_account_credits[c])
            print(account.account_balance)

        account.save()
        c = c + 1

    journal.journal_status = 'A'
    journal.save()

    return redirect('journal')


def reject(request, id):

    journal = Journal.objects.get(id=id)

    if request.method == "POST":

        com = request.POST.get("journalaccountcom")

        journal.journal_status = 'R'
        journal.journal_comment = com
        journal.save()
        return redirect('journal')

    return messages.error(request, "Journal was not Rejected!")


def journal(request, id):
    # journal = Journal.objects.get(id=id)
    pass


@login_required
def journal(request):

    journals = Journal.objects.all()
    user = CustomUser.objects.all()
    user_names = []

    # Loop through the contents
    for x in journals:
        #     # a_num = x.journal_account_numbers
        #     a_debit = x.journal_account_debits
        #     a_credit = x.journal_account_credits
        k = user.get(id=x.journal_user)
        user_names.append(k.username)

    #     # Should be a function
    #     num = re.findall(r'[0-9]+', a_num)
    #     debit = re.findall(r'[0-9]+', a_debit)
    #     credit = re.findall(r'[0-9]+', a_credit)
    #     print(num[0], debit[0], credit[2])

    myFilter = journalFilter(request.GET, queryset=journals)
    journals = myFilter.qs

    items = zip(journals, user_names)
    context = {
        'items': items,
        'myFilter': myFilter,
    }

    return render(request, "accounting/journal.html", context)


def journal_entry(request):

    journalAccounts = Journal.objects.all()
    accounts = Account.objects.all()

    context = {
        'accounts': accounts,
        'journals': journalAccounts,
        'date': datetime.now(),
        # 'range': range(8),
    }

    account_names_debit = []
    account_names_credit = []
    journal_debits = []
    journal_credits = []

    if request.method == "POST":

        j = Journal()
        a = Account()
        user = request.user.id

        typ = request.POST.get("journaltype")
        des = request.POST.get("journalaccountdes")
        credits_entered = request.POST.get("creditnumber")
        debits_entered = request.POST.get("debitnumber")

        print("credit entered: " + credits_entered)
        print("debits entered: " + debits_entered)

        for x in debits_entered:
            account_names_debit.append(request.POST.get(
                "journalaccountnamesdebit{}".format(int(x) - 1)))

            journal_debits.append(request.POST.get(
                "journalaccountdebit{}".format((int(x)-1))))

        for y in credits_entered:
            account_names_credit.append(request.POST.get(
                "journalaccountnamescredit{}".format(int(y) - 1)))

            journal_credits.append(request.POST.get(
                "journalaccountcredit{}".format(int(y) - 1)))

        # if request.POST.get("journalaccountdebit") != 0 and request.POST.get("journalaccountdebit") != "":

            # for x in range(8):
            #     if request.POST.get("journalaccount{:d}".format(x)) is not None:

            #         account_names.append(request.POST.get(
            #             "journalaccount{:d}".format(x)))

            #         if request.POST.get("journalaccountdebit{:d}".format(x)) == '':
            #             journal_debits.append('0')
            #         else:
            #             journal_debits.append(request.POST.get(
            #                 "journalaccountdebit{:d}".format(x)))

            #         if request.POST.get("journalaccountcredit{:d}".format(x)) == '':
            #             journal_credits.append('0')
            #         else:
            #             journal_credits.append(request.POST.get(
            #                 "journalaccountcredit{:d}".format(x)))

            #         jounral_descriptions.append(request.POST.get(
            #             "journalaccountdes{:d}".format(x)))

        debits = [float(journal_debits[x])
                  for x in range(len(journal_debits))]
        credits = [float(journal_credits[x])
                   for x in range(len(journal_credits))]

        if sum(debits) == sum(credits):
            # debit names and numbers json
            d_nums = []
            d_names = []

            # credit names and numbers json
            c_nums = []
            c_names = []

            for x in range(len(account_names_debit)):
                k = account_names_debit[x].split('-')
                d_nums.append(k[0])
                d_names.append(k[1])

            for y in range(len(account_names_credit)):
                k = account_names_credit[x].split('-')
                c_nums.append(k[0])
                c_names.append(k[1])

            j.journal_account_number_debit = d_nums
            j.journal_account_name_debits = d_names
            j.journal_account_number_credits = c_nums
            j.journal_account_name_credits = c_names
            j.journal_account_debits = debits
            j.journal_account_credits = credits
            j.journal_type = typ
            j.journal_description = des
            j.journal_user = user
            # j.journal_file = upload

            j.save()

            messages.success(request, "Successfully Journal Made")
        else:
            messages.error(request, "Debits and Credits must be equal")

    return render(request, "accounting/journalentry.html", context)


def faq(request):
    return render(request, "accounting/faq.html")
