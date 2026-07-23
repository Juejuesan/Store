from django.urls import path

from . import views


app_name = "wallet"


urlpatterns = [

    path(
        "",
        views.wallet_dashboard,
        name="dashboard"
    ),

    path(
        "deposit/",
        views.deposit_request,
        name="deposit"
    ),

    path(
        "withdraw/",
        views.withdraw_request,
        name="withdraw"
    ),

    path(
        "history/",
        views.transaction_history,
        name="history"
    ),

]