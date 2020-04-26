from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from django_keycloak.models import Realm, Client

import django_keycloak.services.users

logger = logging.getLogger(__name__)


def realm(name):
    try:
        return Realm.objects.get(name=name)
    except Realm.DoesNotExist:
        raise TypeError('Realm does not exist')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--realm', type=realm, required=True)
        parser.add_argument('--client_id', type=str, required=True)
        parser.add_argument('--secret', type=str, required=True)

    def handle(self, *args, **options):
        realm = options['realm']
        client_id = options['client_id']
        secret = options['secret']

        Client(realm=realm, client_id=client_id, secret=secret).save()
