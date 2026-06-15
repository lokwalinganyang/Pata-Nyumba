from django.core.mail import send_mail
from django.conf import settings

def send_email_notification(subject, message, recipient_list=None):
    if not recipient_list:
        # Use ADMIN_EMAIL from settings, fallback to a generic address
        recipient_list = [getattr(settings, 'ADMIN_EMAIL', 'admin@patanyumba.com')]
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False
        )
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

def notify_new_property(property_obj):
    subject = f"New Property: {property_obj.title}"
    message = f"New property submitted.\nTitle: {property_obj.title}\nLandlord: {property_obj.landlord.name}"
    send_email_notification(subject, message)

def notify_new_report(report_obj):
    subject = f"Report: {report_obj.property.title}"
    message = f"Property reported.\nReason: {report_obj.reason}"
    send_email_notification(subject, message)

def notify_upgrade_request(property_obj, tier):
    subject = f"Upgrade Request: {property_obj.title}"
    message = f"Landlord requested {tier} upgrade for {property_obj.title}"
    send_email_notification(subject, message)