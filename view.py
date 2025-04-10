# views.py
from django.shortcuts import render, redirect
from paypalrestsdk import Payment, configure

configure({
    "mode": "sandbox",  # "live" for production
    "client_id": "ARswqGFulQJXuORV7I92wMuxZC_Hmu-oV2IipiaU94UpNAzu7ww61v2KrRdnsC312XJYKFlrtzyUeDVs",
    "client_secret": "EG2tFBimYcQVjR6PGrvz5pWdf_PFGze4bcnXqFdID_s6ALHFiDWuZYKaej70TWqUWazOp6XCHobjE65l"
})

def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/donate",
                "cancel_url": "http://localhost:8000/donate"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Donation",
                        "sku": "donation",
                        "price": amount,
                        "currency": "COP",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": amount,
                    "currency": "COP"
                },
                "description": "Donacion para el refugio de animales"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
        else:
            return render(request, 'donate.html', {'error': payment.error})

    payment_id = request.GET.get('paymentId')
    if payment_id:
        payment = Payment.find(payment_id)
        payer_id = request.GET.get('PayerID')
        if payment.execute({"payer_id": payer_id}):
            return render(request, 'donate.html', {'success': True, 'payment': payment})
        else:
            return render(request, 'donate.html', {'error': payment.error})

    return render(request, 'donate.html')
