from django.apps.registry import apps
from django.utils.text import slugify

from keycloak.exceptions import KeycloakClientError

import django_keycloak.services.client


def synchronize_client(client):
    """
    Synchronize all models as resources for a client.

    :type client: django_keycloak.models.Client
    """
    for app_config in apps.get_app_configs():
        synchronize_resources(
            client=client,
            app_config=app_config
        )


def synchronize_resources(client, app_config):
    """
    Synchronize all resources (models) to the Keycloak server for given client
    and Django App.

    :type client: django_keycloak.models.Client
    :type app_config: django.apps.config.AppConfig
    """

    if not app_config.models_module:
        return

    uma_client = client.uma_api_client

    access_token = django_keycloak.services.client.get_access_token(
        client=client
    )

    for klass in app_config.get_models():
        scopes = _get_all_permissions(klass._meta)

        try:
            uma_client.resource_set_create(
                token=access_token,
                name=klass._meta.label_lower,
                server_url=client.realm.server.url,
                internal_url=client.realm.server.internal_url,
                type='urn:{client}:resources:{model}'.format(
                    client=slugify(client.client_id),
                    model=klass._meta.label_lower
                ),
                scopes=scopes
            )
        except KeycloakClientError as e:
            if e.original_exc.response.status_code != 409:
                raise


def _get_all_permissions(meta):
    """
    :type meta: django.db.models.options.Options
    :rtype: list
    """
    return meta.default_permissions
