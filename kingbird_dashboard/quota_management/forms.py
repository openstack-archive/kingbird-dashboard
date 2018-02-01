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


from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from kingbird_dashboard.api import client as kb_client


INDEX_URL = "horizon:kingbird:quota_management:index"


class UpdateForm(forms.SelfHandlingForm):
    ifcb_label = _("Injected File Content (Bytes)")
    ifpb_label = _("Length of Injected File Path")
    metadata_items = forms.IntegerField(min_value=-1,
                                        label=_("Metadata Items"))
    cores = forms.IntegerField(min_value=-1, label=_("VCPUs"))
    instances = forms.IntegerField(min_value=-1, label=_("Instances"))
    key_pairs = forms.IntegerField(min_value=-1, label=_("Key Pairs"))
    volumes = forms.IntegerField(min_value=-1, label=_("Volumes"))
    snapshots = forms.IntegerField(min_value=-1, label=_("Volume Snapshots"))
    gigabytes = forms.IntegerField(
        min_value=-1, label=_("Total Size of Volumes and Snapshots (GiB)"))
    backup_gigabytes = forms.IntegerField(
        min_value=-1, label=_(
            "Total Size of backup Volumes and Snapshots (GiB)"))
    backups = forms.IntegerField(
        min_value=-1, label=_(
            "Total Size of backup Volumes and Snapshots (GiB)"))
    ram = forms.IntegerField(min_value=-1, label=_("RAM (MB)"))
    floating_ips = forms.IntegerField(min_value=-1, label=_("Floating IPs"))
    fixed_ips = forms.IntegerField(min_value=-1, label=_("Fixed IPs"))
    security_groups = forms.IntegerField(min_value=-1,
                                         label=_("Security Groups"))
    security_group = forms.IntegerField(min_value=-1,
                                        label=_("Security Groups"))
    security_group_rule = forms.IntegerField(min_value=-1,
                                             label=_("Security Group Rules"))
    floatingip = forms.IntegerField(min_value=-1, label=_("Floating IPs"))
    network = forms.IntegerField(min_value=-1, label=_("Networks"))
    port = forms.IntegerField(min_value=-1, label=_("Ports"))
    router = forms.IntegerField(min_value=-1, label=_("Routers"))
    subnet = forms.IntegerField(min_value=-1, label=_("Subnets"))

    def __init__(self, request, *args, **kwargs):
        super(UpdateForm, self).__init__(request, *args,
                                         **kwargs)
        target_tenant_id = request.build_absolute_uri().split('/')[-2]
        quotas = kb_client.global_limits(request, target_tenant_id)
        result = {i._data: i._Limit for i in quotas}
        for field in result:
            if field in self.fields:
                self.fields[field].initial = result[field]

    def handle(self, request, data):
        try:
            target_tenant_id = request.build_absolute_uri().split('/')[-2]
            default_quota_obj = kb_client.global_limits(request,
                                                        target_tenant_id)
            default_quota = {i._data: i._Limit for i in default_quota_obj}
            for resource in default_quota:
                if default_quota[resource] == data[resource]:
                    del data[resource]
            if data:
                kb_client.update_global_limits(request, target_tenant_id,
                                               **data)
            msg = _('Quotas updated successfully for tenant "%s".') \
                % target_tenant_id
            messages.success(request, msg)

            return True
        except Exception as e:
            msg = _('Failed to update "%s".') % e
            redirect = reverse('horizon:kingbird:quota_management:index')
            exceptions.handle(request, msg, redirect=redirect)


class SyncQuotaForm(forms.SelfHandlingForm):
    def handle(self, request, data=None):
        target_tenant = request.build_absolute_uri().split('/')[-2]
        try:
            kb_client.sync_quota(request, target_tenant)
            msg = _('On demand Quota sync has been triggered.')
            messages.success(request, msg)
            return True
        except Exception as e:
            msg = _('Failed to Sync Quota "%s".') % e


class DeleteQuotaForm(forms.SelfHandlingForm):
    def handle(self, request, data=None):
        target_tenant = request.build_absolute_uri().split('/')[-2]
        msg = _('Request to delete quotas has been triggered.')
        err_msg = _('Failed to Delete Quota .')
        try:
            kb_client.delete_quota(request, target_tenant)
            messages.success(request, msg)
            return True
        except Exception as e:
            msg = _('Failed to delete quotas for the tenant "%s".') % e
            redirect = reverse('horizon:kingbird:quota_management:index')
            exceptions.handle(request, err_msg, redirect=redirect)
