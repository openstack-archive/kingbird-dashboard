# Copyright 2017 - StackStorm, Inc.
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

from horizon import exceptions
from horizon import tables


from kingbird_dashboard.api import client as kb_client
from kingbird_dashboard.resource_management import tables as kb_tables


class IndexView(tables.DataTableView):
    table_id = "sync_jobs"
    table_class = kb_tables.ResourceSyncTable
    template_name = 'kingbird/resource_management/index.html'

    def get_data(self):
        try:
            response = kb_client.sync_list(self.request)
            return response
        except Exception:
            pass


class DetailView(tables.DataTableView):
    table_id = "job_detail"
    table_class = kb_tables.DetailSyncJobTable
    template_name = 'kingbird/resource_management/detail.html'

    def get_data(self, **kwargs):
        try:
            job_id = self.kwargs['job_id']
            job = kb_client.sync_job_detail(self.request, job_id)
            return job
        except Exception:
            msg = _('Unable to get job_details "%s".') % job_id
            redirect = reverse('horizon:kingbird:resource_management:index')
            exceptions.handle(self.request, msg, redirect=redirect)
