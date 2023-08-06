# django-mellon - SAML2 authentication for Django
# Copyright (C) 2014-2019 Entr'ouvert
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from importlib import import_module

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserSAMLIdentifier(models.Model):
    user = models.ForeignKey(
        verbose_name=_('user'),
        to=settings.AUTH_USER_MODEL,
        related_name='saml_identifiers',
        on_delete=models.CASCADE,
    )
    name_id = models.TextField(verbose_name=_('SAML identifier'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    issuer = models.ForeignKey('mellon.Issuer', verbose_name=_('Issuer'), null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('user SAML identifier')
        verbose_name_plural = _('users SAML identifiers')
        unique_together = (('issuer', 'name_id'),)


class SessionIndex(models.Model):
    session_index = models.TextField(_('SAML SessionIndex'))
    session_key = models.CharField(_('Django session key'), max_length=40)
    saml_identifier = models.ForeignKey(
        verbose_name=_('SAML identifier'), to=UserSAMLIdentifier, on_delete=models.CASCADE
    )

    @staticmethod
    def cleanup(cls):
        session_engine = import_module(settings.SESSION_ENGINE)
        store = session_engine.SessionStore()

        ids = []
        for si in cls.objects.all():
            if not store.exists(si.session_key):
                ids.append(si.id)
        cls.objects.filter(id__in=ids).delete()

    class Meta:
        verbose_name = _('SAML SessionIndex')
        verbose_name_plural = _('SAML SessionIndexes')
        unique_together = (('saml_identifier', 'session_index', 'session_key'),)


class Issuer(models.Model):
    entity_id = models.TextField(verbose_name=_('IdP Entity ID'), unique=True)
    slug = models.TextField(verbose_name=_('IdP slug'), unique=True, null=True)

    class Meta:
        verbose_name = _('SAML IdP')
        verbose_name_plural = _('SAML IdPs')
