# from django.core.cache import cache
# from django.db.models.signals import post_save, post_delete
# from django.conf import settings
# from .models import Product

# def update_cache(sender, instance, **kwargs):
#     if sender in (Product,) and kwargs['created'] == False:
#         cache.delete(settings.LIST_CACHE_NAME)

# post_save.connect(update_cache)
# post_delete.connect(update_cache)