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
                "Your deposit request has been submitted successfully and is waiting for admin approval."
            )

            return redirect("wallet:deposit")

        else:

            # Show every validation error as a popup message
            for errors in form.errors.values():

                for error in errors:

                    messages.error(
                        request,
                        error
                    )

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

            # Check wallet balance
            if amount > wallet.balance:

                messages.error(
                    request,
                    f"Insufficient wallet balance. Your current balance is MMK {wallet.balance:,.0f}, but you requested MMK {amount:,.0f}."
                )

                context = {
                    "wallet": wallet,
                    "form": form,
                }

                return render(
                    request,
                    "wallet/withdraw.html",
                    context,
                )

            # Save withdrawal request
            withdraw.user = request.user
            withdraw.save()

            messages.success(
                request,
                "Your withdrawal request has been submitted successfully and is waiting for admin approval."
            )

            return redirect("wallet:withdraw")

        else:

            # Add each form error to Django messages
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, error)

            context = {
                "wallet": wallet,
                "form": form,
            }

            return render(
                request,
                "wallet/withdraw.html",
                context,
            )

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

