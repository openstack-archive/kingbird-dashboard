# Copyright 2018 - Ericsson AB.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf import settings

from glanceclient import client as gl_client

from horizon.utils import memoized

from keystoneauth1 import loading

from keystoneauth1 import session

from keystoneclient.v3 import client as ks_client

import kingbirdclient

from kingbirdclient.api import client as kb_client

from novaclient import client as nv_client

SERVICE_TYPE = 'synchronization'

NOVA_API_VERSION = "2.37"

GLANCE_API_VERSION = "2"


@memoized.memoized
def kingbird_dashboardclient(request):
    """Kingbird Client for API calls."""
    return kb_client.client(
        username=request.user.username,
        auth_token=request.user.token.id,
        project_id=request.user.tenant_id,
        auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    )


def keystone_session(request):
    """Keystone session for establishment of Nova and Glance clients."""
    auth_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    loader = loading.get_plugin_loader('token')
    auth = loader.load_from_options(auth_url=auth_url,
                                    token=request.user.token.id,
                                    project_id=request.user.tenant_id)
    sess = session.Session(auth=auth)
    return ks_client.Client(session=sess)


def _get_endpoint_from_region(keystone_admin, region):
    services_list = keystone_admin.services.list()
    endpoints_list = keystone_admin.endpoints.list()
    service_id = [service.id for service in
                  services_list if service.type == 'image'][0]

    glance_endpoint = [endpoint.url for endpoint in
                       endpoints_list
                       if endpoint.service_id == service_id
                       and endpoint.region == region and
                       endpoint.interface == 'public'][0]
    return glance_endpoint


def nova_client(request, region):
    """Nova Client for API calls."""
    return nv_client.Client(
        NOVA_API_VERSION, session=keystone_session(request).session,
        region_name=region)


def glance_client(request, region):
    """Glance Client for API calls."""
    keystone_admin = keystone_session(request)
    region_endpoint = _get_endpoint_from_region(keystone_admin,
                                                region)
    return gl_client.Client(
        GLANCE_API_VERSION, session=keystone_session(request).session,
        endpoint=region_endpoint)


def regions_list(request):
    """List of available regions."""
    return keystone_session(request).regions.list()


def images_list(request, region):
    """List of images."""
    images_choices = list()
    images_list = glance_client(request, region).images.list()
    for image in images_list:
        images_choices.append(image.id)
    return images_choices


def flavors_list(request, region):
    """List of flavors."""
    flavors_choices = list()
    flavors_list = nova_client(request, region).flavors.list()
    for flavor in flavors_list:
        flavors_choices.append(flavor.name)
    return flavors_choices


def keypairs_list(request, region):
    """List of keypairs."""
    keypairs_choices = list()
    keypairs_list = nova_client(request, region).keypairs.list()
    for keypair in keypairs_list:
        keypairs_choices.append(keypair.name)
    return keypairs_choices


def list_defaults(request):
    """Default Quota Limits."""
    return kingbird_dashboardclient(request).quota_manager.\
        list_defaults()


def global_limits(request, target_tenant_id):
    """Global Quota Limits for any tenant."""
    return kingbird_dashboardclient(request).quota_manager.\
        global_limits(target_tenant_id)


def update_global_limits(request, target_tenant_id, **data):
    """Update Global Limits for a tenant."""
    return kingbird_dashboardclient(request).quota_manager.\
        update_global_limits(target_tenant_id, **data)


def sync_quota(request, target_tenant_id):
    """On Demand Quota Sync."""
    return kingbird_dashboardclient(request).quota_manager.\
        sync_quota(target_tenant_id)


def delete_quota(request, target_tenant_id):
    """Delete Quota for a tenant."""
    try:
        kingbird_dashboardclient(request).quota_manager.\
            delete_quota(target_tenant_id)
        return True
    except kingbirdclient.exceptions.APIException:
        raise


def detail_quota(request, target_tenant_id):
    """Quota Information of a tenant."""
    try:
        return kingbird_dashboardclient(request).quota_manager.\
            quota_detail(target_tenant_id)
    except kingbirdclient.exceptions.APIException:
        raise


def sync_list(request, action=None):
    """List the sync jobs."""
    return kingbird_dashboardclient(request).sync_manager.\
        list_sync_jobs(action)


def sync_job_detail(request, job_id):
    """Detail information of sync job."""
    return kingbird_dashboardclient(request).sync_manager.\
        sync_job_detail(job_id)


def sync_delete(request, job_id):
    """Delete sync jobs from database."""
    return kingbird_dashboardclient(request).sync_manager.\
        delete_sync_job(job_id)


def sync_job_create(request, data):
    """Sync a job from source to target region."""
    return kingbird_dashboardclient(request).sync_manager.\
        sync_resources(**data)
