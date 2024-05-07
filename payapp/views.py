from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import PaymentSendForm, PaymentRequestForm
from .models import Notification, Payment, PaymentRequest
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import Q
from django.db import transaction
from decimal import Decimal
from register.models import CustomUser
from .utils import exchange_rate


    
@login_required(login_url='signin')
def home(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please signin first')
        return redirect('signin')
    
    user = request.user
    
    # transactions involving the current user
    send_transactions = Payment.objects.filter(sender=user) | Payment.objects.filter(recipient=user)
    request_transactions = PaymentRequest.objects.filter(requested_to=user) | PaymentRequest.objects.filter(requested_from=user)

    # Combine and sort transactions
    transactions = list(chain(send_transactions, request_transactions))
    transactions = sorted(transactions, key=lambda x: x.created_at, reverse=True)
    
    context = {
        "history": transactions
    }

    return render(request, 'payapp/home.html', context)


@login_required(login_url='signin')
def send_request(request):
    sendform = PaymentSendForm(user=request.user)
    requestform = PaymentRequestForm(user=request.user)
    paymentrequests = PaymentRequest.objects.filter(
        requested_from=request.user)
    context = {
        "sendform": sendform,
        "requestform": requestform,
        "balance": request.user.userbalance.balance,
        "paymentrequests": paymentrequests
    }
    return render(request, "payapp/transaction.html", context)


@login_required(login_url='signin')
def send_payments(request):
    sentpayments = Payment.objects.filter(sender=request.user)
    context= {
        "history": sentpayments
        }
    return render(request, "payapp/activity.html", context)


@login_required(login_url='signin')
def received_payments(request):
    receivedpayments = Payment.objects.filter(recipient=request.user)
    context = {
        "history": receivedpayments
    }
    return render(request, "payapp/activity.html", context)



@login_required(login_url='signin')
def other_requests(request):
    receivedrequests = PaymentRequest.objects.filter(
        requested_from=request.user)
    context = {
        "history": receivedrequests
    }
    return render(request, "payapp/activity.html", context)


@login_required(login_url='signin')
def own_requests(request):
    receivedrequests = PaymentRequest.objects.filter(requested_to=request.user)
    context = {
        "history": receivedrequests
    }
    return render(request, "payapp/activity.html", context)


@login_required(login_url='signin')
def payments(request):
    user = request.user

    send_transactions = Payment.objects.filter(sender=user)

    receive_transactions = Payment.objects.filter(recipient=user)

    receive_requests = PaymentRequest.objects.filter(requested_to=user)

    send_requests = PaymentRequest.objects.filter(requested_from=user)

    transactions = list(send_transactions) + list(receive_transactions) + list(receive_requests) + list(send_requests)

    transactions_sorted = sorted(
        transactions, key=lambda x: x.created_at, reverse=True
    )

    context = {
        "history": transactions_sorted
    }

    return render(request, "payapp/activity.html", context)


@login_required(login_url='signin')
def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {
        "notifications": notifications
    }
    return render(request, "payapp/notification.html", context)


@login_required(login_url='signin')
def unseen_notification(request):
    notifications = Notification.objects.filter(
        user=request.user, is_seen=False)
    context = {
        "notifications": notifications
    }
    return render(request, "payapp/notification.html", context)


@login_required(login_url='signin')
def mark_as_seen(request, id):
    notification = Notification.objects.filter(id=id).first()
    if notification:
        notification.is_seen = True
        notification.save()
    return redirect("notification")

@login_required(login_url='signin')
def payment_send(request):
    try:
        form = PaymentSendForm(user=request.user)
        if request.method == "POST":
            email = request.POST.get('recipient')
            user = CustomUser.objects.filter(email=email).first()
            amount = Decimal(request.POST.get('amount'))
            if email == request.user.email:
                messages.warning(request, "Sending money to yourself is not allowed")
                return render(request, "payapp/payment_send.html", {"form": form})
            if not user:
                messages.warning(request, "User not found")
                return render(request, "payapp/payment_send.html", {"form": form})
            with transaction.atomic():
                instance = Payment.objects.create(
                    sender=request.user, recipient=user, amount=amount)
                recipient = instance.recipient
                sender = instance.sender
                principal = Decimal(instance.amount)
                sender.userbalance.balance -= principal
                actual_principal = Decimal(exchange_rate(
                    sender.currency, recipient.currency))*principal
                recipient.userbalance.balance += actual_principal
                sender.userbalance.save()
                recipient.userbalance.save()
                instance.save()
                messages.success(request, "Payment completed successfully")
                return redirect('payments')
    except Exception as e:
        messages.error(request, str(e))

    return render(request, "payapp/payment_send.html", {"form": form})


@login_required(login_url='signin')
def payment_request(request):
    if request.method == "POST":
        email = request.POST.get("requested_to")
        send_from = CustomUser.objects.filter(email=email).first()
        amount = request.POST.get("amount")
        if email == request.user.email:
            messages.warning(request, "You can't request money to yourself")
            return redirect(request.META.get("HTTP_REFERER"))
        if not send_from:
            messages.success(request, "User with this email doesn't exist")
            return redirect(request.META.get("HTTP_REFERER"))
        instance = PaymentRequest.objects.create(
            requested_to=request.user, requested_from=send_from, amount=amount)
        if instance:
            messages.success(request, "Request completed successfully")
            return redirect("payments")
    form = PaymentRequestForm()
    return render(request, "payapp/payment_request.html", {"form": form})


@login_required(login_url='signin')
def payment_request_approve(request):
    if request.method == "POST":
        id = request.POST.get("tr_id")
        Treq = PaymentRequest.objects.filter(id=id).first()
        receiver_id = request.POST.get('send_to')
        sender_id = request.POST.get('send_from')
        sender = CustomUser.objects.filter(id=sender_id).first()
        receiver = CustomUser.objects.filter(id=receiver_id).first()
        amount = Decimal(request.POST.get("amount"))
        if sender.userbalance.balance >= amount:
            with transaction.atomic():
                sending_amount = Decimal(exchange_rate(
                    receiver.currency, sender.currency))*Decimal(amount)
                sender.userbalance.balance -= sending_amount
                receiver.userbalance.balance += amount
                sender.userbalance.save()
                receiver.userbalance.save()
                Payment(sender=sender, recipient=receiver,
                            amount=amount).save()
                Treq.is_accepted = True
                Treq.save()
                messages.success(request, "Payment completed successfully")
        else:
            Treq.is_accepted = False
            Treq.save()
            messages.warning(request, "You donot have enough balance.")
    return redirect("payments")


@login_required(login_url='signin')
def payment_request_reject(request):
    if request.method == "POST":
        id = request.POST.get("tr_id")
        trreq = PaymentRequest.objects.get(id=id)
        trreq.is_accepted = False
        trreq.save()
        messages.success(request, "Payment request rejected successfully")
    return redirect("payments")


@login_required(login_url='signin')
def payment_all(request):

    if request.user.is_superuser:
        type = request.GET.get('type')
        if type == 'sent-received':
            send_transactions = Payment.objects.filter()
            transactions = list(chain(send_transactions))
            transactions_sorted = sorted(
                transactions, key=lambda x: x.created_at, reverse=True)
            context = {
                "history": transactions_sorted
            }
            return render(request, "payapp/payment_all.html", context)
        if type == 'sent-received_request':
            request_transactions = PaymentRequest.objects.filter()
            transactions = list(chain(request_transactions))
            transactions_sorted = sorted(
                transactions, key=lambda x: x.created_at, reverse=True)
            context = {
                "history": transactions_sorted
            }
            return render(request, "payapp/payment_all.html", context)
        send_transactions = Payment.objects.filter()
        request_transactions = PaymentRequest.objects.filter()

        transactions = list(chain(send_transactions, request_transactions))
        transactions_sorted = sorted(
            transactions, key=lambda x: x.created_at, reverse=True)
        context = {
            "history": transactions_sorted
        }
        return render(request, "payapp/payment_all.html", context)
    else:
        messages.error(request, "Unauthorized: You don't have permission to access this page")
        return redirect("transaction")
