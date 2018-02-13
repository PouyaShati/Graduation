from celery.schedules import crontab
from celery.task import periodic_task

from Process.models import Form, Payment
from Student.models import Student
from django.utils import timezone
from django.core.mail import send_mail



@periodic_task(run_every=crontab(hour=0))
def every_monday_morning():
    for form in Form.objects.all():
        if form.instance_of.is_timed and timezone.now() > form.instance_of.max_time:
            m1 = 'دانشجوی گرامی، '
            m2 = form.process.owner.first_name + ' ' + form.process.owner.last_name
            m3 = ' لطفا در پر کردن فرم مرتبط به فرآیند'
            m4 = form.process.instance_of.name
            m5 = ' تعجیل فرمایید. سیستم فارغ التحصیلی دانشگاه شریف'

            send_mail(
                'تاخیر در پر کردن فرم',
                m1+m2+m3+m4+m5,
                'graduation@sharif.edu',
                [form.process.owner.email],
                fail_silently=False,
            )

    for payment in Payment.objects.all():
        if payment.instance_of.is_timed and timezone.now() > payment.instance_of.max_time:
            m1 = 'دانشجوی گرامی، '
            m2 = payment.process.owner.first_name + ' ' + payment.process.owner.last_name
            m3 = ' لطفا در پرداخت مبلغ مرتبط به فرآیند'
            m4 = payment.process.instance_of.name
            m5 = ' تعجیل فرمایید. سیستم فارغ التحصیلی دانشگاه شریف'

            send_mail(
                'تاخیر در پرداخت مبلغ',
                m1+m2+m3+m4+m5,
                'graduation@sharif.edu',
                [form.process.owner.email],
                fail_silently=False,
            )

