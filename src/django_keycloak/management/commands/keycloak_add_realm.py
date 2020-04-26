from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from django_keycloak.models import Realm, Server

import django_keycloak.services.users

logger = logging.getLogger(__name__)


def server(url):
    try:
        return Server.objects.get(url=url)
    except Server.DoesNotExist:
        raise TypeError('Server does not exist')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--server', type=server, required=True)
        parser.add_argument('--name', type=str, required=True)

    def handle(self, *args, **options):
        server = options['server']
        name = options['name']

        Realm(name=name, server=server).save()
