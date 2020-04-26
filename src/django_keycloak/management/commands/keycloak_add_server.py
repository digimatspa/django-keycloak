from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand

from django_keycloak.models import Server


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, required=True)
        parser.add_argument('--internal', type=str, required=False)

    def handle(self, *args, **options):
        url = options['url']
        internal_url = options.pop('internal', None)

        Server(url=url, internal_url=internal_url).save()
