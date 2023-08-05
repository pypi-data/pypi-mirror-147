from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer


# @receiver(post_save, sender=User)
# def user_created(sender, instance, created, **kwargs):
#     if created:
#         profile = Customer.objects.create(
#             user=instance
#         )


@receiver(post_save, sender=Customer)
def customer_modified(sender, instance, created, **kwargs):
    if not created:
        try:
            user = User.objects.get(customer=instance)
        except:
            pass
        else:
            user.first_name = instance.first_name
            user.last_name = instance.last_name

            if not User.objects.filter(email=instance.email).exists():
                user.email = instance.email
            
            if not User.objects.filter(username=instance.username).exists():
                user.username = instance.username

            user.save()
    

# @receiver(post_delete, sender=User)
# def profile_deleted(sender, instance, **kwargs):
#     p = Customer.objects.filter(email=instance.email).first()
#     if p:
#         p.delete()


# ########################################################
# Another method instead of decorators####################
# post_save.connect(user_created, sender=User)#####
# post_delete.connect(profile_deleted, sender=Customer)###
# ########################################################