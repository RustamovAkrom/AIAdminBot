from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from apps.bot.models.payments import Payment

import stripe


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            telegram_id = session.get("metadata", {}).get("telegram_id")
            amount = session.get("amount_total") / 100

            Payment.objects.filter(telegram_id=telegram_id, amount=amount).update(
                status="paid"
            )

        elif event["type"] == "checkout.session.expired":
            session = event["data"]["object"]
            telegram_id = session.get("metadata", {}).get("telegram_id")
            amount = session.get("amount_total") / 100

            Payment.objects.filter(telegram_id=telegram_id, amount=amount).update(
                status="failed"
            )

    except Exception as e:
        print("Error Webhook: ", e)
        return JsonResponse({"status": "error"}, status=400)

    return JsonResponse({"status": "success"}, status=200)
