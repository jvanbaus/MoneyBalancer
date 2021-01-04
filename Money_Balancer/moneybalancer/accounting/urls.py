from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", views.account, name="account"),
    path("some_template/", views.journal_entry, name="some_template"),
    path("sendemail/", views.sendemail, name="sendemail"),
    path("events/", views.event, name="event"),
    path("journals/", views.journal, name="journal"),
    path("journals/<int:id>", views.journal, name="journalnumber"),
    path("journal_entry/", views.journal_entry, name="journalentry"),
    path("faq/", views.faq, name="faq"),
    path("ledger/<int:id>", views.ledger, name="ledger"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("deactive/<int:id>", views.deactive, name="deactive"),
    path("approve/<int:id>", views.approve, name="approve"),
    path("journals/reject/<int:id>", views.reject, name="reject"),
]
