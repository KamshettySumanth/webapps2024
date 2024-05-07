from payapp import views
from django.urls import path


urlpatterns = [
    # dashboard
    path('home/', views.home, name='home'),

    # payments urls
    path('send-request-payment/', views.send_request, name="send_request_payment"),
    path("payments/all/", views.payment_all, name="payment_all"),
    path('payments/', views.payments, name="payments"),
    path("sent/payments/", views.send_payments, name="sent_payments"),
    path('received/payments/', views.received_payments,
         name="received_payments"),
    path('otherequests/', views.other_requests, name="other_requests"),
    path("ownrequests/", views.own_requests, name="own_requests"),


    # notifications
    path('notification/', views.notification, name="notification"),
    path('unseen_notification/', views.unseen_notification,
         name="unseen_notification"),
    path('mark_as_seen/<int:id>/', views.mark_as_seen, name="mark_as_seen"),

    # payment filter on tables

    path('payment/send/', views.payment_send, name="payment_send"),
    path('payment/request/', views.payment_request, name="payment_request"),
    path('payment/request/approve/', views.payment_request_approve,
         name="payment_request_approve"),
    path('payment/request/reject/', views.payment_request_reject,
         name="payment_request_reject"),

]
