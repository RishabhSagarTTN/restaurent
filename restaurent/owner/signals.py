from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.db.models.signals import post_delete,post_migrate,post_save
from django.utils.timezone import now
import logging
from django.dispatch import receiver
from django.core.cache import cache
from .models import Dishes,Orders
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger=logging.getLogger(__name__)
@receiver(user_logged_in,sender=User)
def loginS(sender,request,user,**kwargs):
    logger.info(f"User {user.username} logged in at {now()}")
    print("-------------------------------------------------------------------")
    ip_address = request.META.get('REMOTE_ADDR')
    logger.info(f"User {user.username} logged in from IP: {ip_address}")
    cache.clear()
    

@receiver(user_logged_out,sender=User)
def logoutS(request,user,**kwargs):
    logger.info(f"User {user.username} logged out at {now()}")
    ip_address = request.META.get('REMOTE_ADDR')
    logger.info(f"User {user.username} logged out from IP: {ip_address}")
    cache.clear()

def test():
       cache.clear()


@receiver(post_save, sender=Dishes)
@receiver(post_save, sender=Orders)
@receiver(post_delete, sender=Dishes)
@receiver(post_delete, sender=Orders)
@receiver(post_migrate, sender=Dishes)
@receiver(post_migrate, sender=Orders)
def cacheSetup(sender,instance, **kwargs):
    test()

