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
from django.utils.translation import ungettext_lazy

from horizon import tables

from kingbird_dashboard.api import client as kb_client


class SyncJobCreate(tables.LinkAction):
    name = "sync_job"
    verbose_name = _("Create Sync Job")
    url = "horizon:kingbird:resource_management:create_sync_job"
    classes = ("ajax-modal",)
    icon = "plus"


class SyncTemplateCreate(tables.LinkAction):
    name = "sync_template"
    verbose_name = _("Create Sync Template")
    url = "horizon:kingbird:resource_management:create_sync_template"
    classes = ("ajax-modal",)
    icon = "plus"


class DeleteSyncJob(tables.DeleteAction):

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Sync Job",
            u"Delete Sync Jobs",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Sync Job",
            u"Deleted Sync Jobs",
            count
        )

    def delete(self, request, job_id):
        kb_client.sync_delete(request, job_id)


class DetailSyncJobTable(tables.DataTable):

    resource_sync_id = tables.Column(
        "id",
        verbose_name=_("Resource Sync Identifier"),
    )
    resource_name = tables.Column(
        "resource_name",
        verbose_name=_("Resource Identifier")
    )
    source_region = tables.Column(
        "source_region",
        verbose_name=_("Source Region")
    )
    target_region = tables.Column(
        "target_region",
        verbose_name=_("Target Region")
    )
    resource_type = tables.Column(
        "resource_type",
        verbose_name=_("Resource Type")
    )
    status = tables.Column(
        "status",
        verbose_name=_("Status")
    )
    created_at = tables.Column(
        "created_at",
        verbose_name=_("Created")
    )
    updated_at = tables.Column(
        "updated_at",
        verbose_name=_("Updated")
    )

    def get_object_id(self, datum):
        return datum.id

    class Meta(object):
        name = "job_set"
        verbose_name = _("Job Details")


class ResourceSyncTable(tables.DataTable):

    id = tables.Column(
        "id",
        verbose_name=_("ID"),
        link="horizon:kingbird:resource_management:detail"
    )
    sync_status = tables.Column(
        "status",
        verbose_name=_("Status")
    )
    created_at = tables.Column(
        "created_at",
        verbose_name=_("Created")
    )
    updated_at = tables.Column(
        "updated_at",
        verbose_name=_("Updated")
    )

    def get_object_display(self, datum):
        return datum.id

    class Meta(object):
        name = "job_set"
        verbose_name = _("Resource Management")
        table_actions = (
            SyncJobCreate,
            SyncTemplateCreate,
            DeleteSyncJob
        )
        row_actions = (DeleteSyncJob,)
