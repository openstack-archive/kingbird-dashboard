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

from horizon.utils import memoized

import kingbirdclient

from kingbirdclient.api import client as kb_client

SERVICE_TYPE = 'synchronization'


@memoized.memoized
def kingbird_dashboardclient(request):
    """Kingbird Client for API calls."""
    return kb_client.client(
        username=request.user.username,
        auth_token=request.user.token.id,
        project_id=request.user.tenant_id,
        auth_url=getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    )


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
