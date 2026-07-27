from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    DepositForm,
    WithdrawForm,
)

from .models import (
    Wallet,
    DepositRequest,
    WithdrawRequest,
)


# ======================================================
# WALLET DASHBOARD
# ======================================================

@login_required
def wallet_dashboard(request):
    wallet, created = Wallet.objects.get_or_create(
        user=request.user
    )

    deposits = DepositRequest.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    withdrawals = WithdrawRequest.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    transactions = wallet.transactions.all()[:10]

    context = {
        "wallet": wallet,
        "deposits": deposits,
        "withdrawals": withdrawals,
        "transactions": transactions,
    }

    return render(
        request,
        "wallet/dashboard.html",
        context,
    )


# ======================================================
# DEPOSIT REQUEST
# ======================================================

@login_required
def deposit_request(request):

    wallet = get_object_or_404(
        Wallet,
        user=request.user
    )

    if request.method == "POST":

        form = DepositForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()

            messages.success(
                request,
                "Deposit request submitted successfully. Please wait for admin approval."
            )

            return redirect("wallet:deposit")

    else:

        form = DepositForm()

    recent_deposits = DepositRequest.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    context = {
        "wallet": wallet,
        "form": form,
        "deposits": recent_deposits,
    }

    return render(
        request,
        "wallet/deposit.html",
        context,
    )

# ======================================================
# WITHDRAW REQUEST
# ======================================================

@login_required
def withdraw_request(request):

    wallet = get_object_or_404(
        Wallet,
        user=request.user
    )

    if request.method == "POST":

        form = WithdrawForm(request.POST)

        if form.is_valid():

            withdraw = form.save(commit=False)

            amount = form.cleaned_data["amount"]

            if amount > wallet.balance:

                messages.error(
                    request,
                    "Insufficient wallet balance."
                )

            else:

                withdraw.user = request.user
                withdraw.save()

                messages.success(
                    request,
                    "Withdrawal request submitted successfully."
                )

                return redirect("wallet:history")

    else:

        form = WithdrawForm()

    context = {
        "wallet": wallet,
        "form": form,
    }

    return render(
        request,
        "wallet/withdraw.html",
        context,
    )


# ======================================================
# TRANSACTION HISTORY
# ======================================================

@login_required
def transaction_history(request):

    wallet = get_object_or_404(
        Wallet,
        user=request.user
    )

    transactions = wallet.transactions.all()

    deposits = DepositRequest.objects.filter(
        user=request.user
    )

    withdrawals = WithdrawRequest.objects.filter(
        user=request.user
    )

    context = {
        "wallet": wallet,
        "transactions": transactions,
        "deposits": deposits,
        "withdrawals": withdrawals,
    }

    return render(
        request,
        "wallet/history.html",
        context,
    )