from django.db import models


class PartnerAddressManager(models.Manager):
    def get_primary(self, partner):
        qs = self.get_queryset()
        return qs.filter(partner=partner, primary=True).first()
