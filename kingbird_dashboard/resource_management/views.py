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
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tables


from kingbird_dashboard.api import client as kb_client
from kingbird_dashboard.resource_management import forms as kb_forms
from kingbird_dashboard.resource_management import tables as kb_tables


class CreateSyncJobView(forms.ModalFormView):
    template_name = 'kingbird/resource_management/create.html'
    form_id = "create_sync_job"
    form_class = kb_forms.SyncJobForm
    submit_label = _("Create Sync Job")
    submit_url = reverse_lazy(
        "horizon:kingbird:resource_management:create_sync_job")
    success_url = reverse_lazy('horizon:kingbird:resource_management:index')
    page_title = _("Create Sync Job")

    def get_form_kwargs(self):
        kwargs = super(CreateSyncJobView, self).get_form_kwargs()
        return kwargs


class CreateSyncTemplateView(forms.ModalFormView):
    template_name = 'kingbird/resource_management/create_template.html'
    form_id = "create_sync_template"
    form_class = kb_forms.SyncTemplateForm
    submit_label = _("Create Sync Template")
    submit_url = reverse_lazy(
        "horizon:kingbird:resource_management:create_sync_template")
    success_url = reverse_lazy('horizon:kingbird:resource_management:index')
    page_title = _("Create Sync Template")

    def get_form_kwargs(self):
        kwargs = super(CreateSyncTemplateView, self).get_form_kwargs()

        return kwargs


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


def load_flavors(request):
    source = request.GET.get('source')
    # Choices for flavors.
    flavors_list = kb_client.flavors_list(request, source)
    return render(request, 'kingbird/resource_management/resources.html',
                  {'resources': flavors_list})


def load_keypairs(request):
    source = request.GET.get('source')
    # Choices for keypairs.
    keypairs_list = kb_client.keypairs_list(request, source)
    return render(request, 'kingbird/resource_management/resources.html',
                  {'resources': keypairs_list})


def load_images(request):
    source = request.GET.get('source')
    # Choices for images.
    images_list = kb_client.images_list(request, source)
    return render(request, 'kingbird/resource_management/resources.html',
                  {'resources': images_list})
