# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import tables


class UpdateQuota(tables.LinkAction):
    name = "update"
    verbose_name = _("Update")
    url = "horizon:kingbird:quota_management:update"
    classes = ("ajax-modal", "btn-edit")


class QuotaSync(tables.LinkAction):
    name = "quota_sync"
    verbose_name = _("Sync Quota")
    url = "horizon:kingbird:quota_management:sync"
    classes = ("ajax-modal", "btn-edit")


class DeleteQuota(tables.LinkAction):
    name = "delete_quota"
    verbose_name = _("Delete Quota")
    url = "horizon:kingbird:quota_management:delete"
    classes = ("ajax-modal", "btn-edit")


class TenantsTable(tables.DataTable):
    name = tables.Column(
        "name",
        verbose_name=_("Name")
    )
    description = tables.Column(
        "description",
        verbose_name=_("Description")
    )
    id = tables.Column(
        "id",
        verbose_name=_("Project ID"),
    )
    enabled = tables.Column(
        "enabled",
        verbose_name=_("Enabled"),
    )

    def get_object_id(self, datum):
        return datum.id

    class Meta(object):
        name = "tenant_set"
        verbose_name = _("Quota Management")
        row_actions = (UpdateQuota, QuotaSync, DeleteQuota)
