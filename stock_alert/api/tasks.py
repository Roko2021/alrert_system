import requests
from datetime import datetime, timedelta
from .models import Alert, TriggeredAlert
from .notifications import send_email_notification


# قائمة الأسهم التي تريد متابعة أسعارها
STOCK_SYMBOLS = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NFLX", "NVDA", "BABA", "INTC"]

def fetch_stock_prices():
    """
    جلب أسعار الأسهم الحالية من API خارجي
    """
    api_key = "EPrwApBRx3WOt6341Dxj0r8OL7Ggvkkf"  # ضع هنا مفتاح API الخاص بك
    base_url = "https://financialmodelingprep.com/api/v3/quote"
    symbols_str = ",".join(STOCK_SYMBOLS)
    url = f"{base_url}/{symbols_str}?apikey={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = {stock['symbol']: stock['price'] for stock in data}
        return prices
    else:
        print(f"Failed to fetch stock prices. Status code: {response.status_code}")
        return None


def check_alerts(current_prices):
    """
    فحص جميع التنبيهات النشطة بناء على الأسعار الحالية.
    عند تحقق شرط التنبيه يتم تسجيل التنبيه المفعّل وإرسال بريد إلكتروني.
    """
    now = datetime.now()
    alerts = Alert.objects.filter(is_active=True)

    for alert in alerts:
        symbol = alert.stock_symbol
        if symbol not in current_prices:
            print(f"Stock symbol {symbol} not found in current prices.")
            continue

        current_price = current_prices[symbol]
        user_email = alert.user.email
        print(f"Checking alert for {symbol} at price {current_price} (User email: {user_email})")

        condition_met = False

        # شرط التنبيه من نوع threshold
        if alert.alert_type == 'threshold' and alert.threshold_value is not None:
            if alert.condition == 'gt' and current_price > alert.threshold_value:
                condition_met = True
            elif alert.condition == 'lt' and current_price < alert.threshold_value:
                condition_met = True

        # شرط التنبيه من نوع duration مع مدة وقت محددة
        elif alert.alert_type == 'duration' and alert.duration_hours is not None:
            # تحقق هل تم تفعيل التنبيه مسبقاً خلال الفترة الزمنية المعينة
            triggered_recent = TriggeredAlert.objects.filter(
                alert=alert,
                triggered_at__gte=now - timedelta(hours=alert.duration_hours)
            ).exists()

            if triggered_recent:
                print(f"Alert for {symbol} already triggered in the last {alert.duration_hours} hours. Skipping.")
                continue

            if alert.condition == 'gt' and current_price > alert.threshold_value:
                condition_met = True
            elif alert.condition == 'lt' and current_price < alert.threshold_value:
                condition_met = True

        # إذا تم تحقق الشرط
        if condition_met:
            print(f"Alert triggered for {symbol} at price {current_price} for user {user_email}")
            TriggeredAlert.objects.create(alert=alert, current_price=current_price)

            subject = f"تنبيه سهم {alert.stock_symbol}"
            message = f"التنبيه الخاص بك لـ {alert.stock_symbol} تحقق عند السعر {current_price}."

            try:
                send_email_notification(user_email, subject, message)
                print(f"تم إرسال البريد إلى {user_email}")
            except Exception as e:
                print(f"فشل إرسال البريد إلى {user_email}: {e}")

        else:
            print(f"No condition met for {symbol} at price {current_price}")


def fetch_and_check_alerts():
    """
    دالة لتجميع الخطوات: جلب الأسعار وفحص التنبيهات
    """
    print("Starting fetch_and_check_alerts...")
    prices = fetch_stock_prices()
    if prices:
        print(f"Fetched prices: {prices}")
        check_alerts(prices)
    else:
        print("Failed to fetch stock prices.")
