# Copyright 2018 Ericsson AB.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables

from kingbird_dashboard.api import client as kb_client
from kingbird_dashboard.quota_management import forms as kb_forms
from kingbird_dashboard.quota_management import tables as kb_tables

from openstack_dashboard import api as os_api
from openstack_dashboard import policy
from openstack_dashboard.utils import identity


class IndexView(tables.DataTableView):
    table_id = "tenants"
    table_class = kb_tables.TenantsTable
    template_name = 'kingbird/quota_management/index.html'
    page_title = _("Quota Management")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        tenants = []
        marker = self.request.GET.get(
            kb_tables.TenantsTable._meta.pagination_param, None)
        self._more = False
        filters = self.get_filters()

        self._needs_filter_first = False

        if policy.check((("identity", "identity:list_projects"),),
                        self.request):

            # If filter_first is set and if there are not other filters
            # selected, then search criteria must be provided and
            # return an empty list
            filter_first = getattr(settings, 'FILTER_DATA_FIRST', {})
            if filter_first.get('identity.projects', False) and len(
                    filters) == 0:
                self._needs_filter_first = True
                self._more = False
                return tenants

            domain_id = identity.get_domain_id_for_operation(self.request)
            try:
                tenants, self._more = os_api.keystone.tenant_list(
                    self.request,
                    domain=domain_id,
                    paginate=True,
                    filters=filters,
                    marker=marker)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project list."))
        elif policy.check((("identity", "identity:list_user_projects"),),
                          self.request):
            try:
                tenants, self._more = os_api.keystone.tenant_list(
                    self.request,
                    user=self.request.user.id,
                    paginate=True,
                    marker=marker,
                    filters=filters,
                    admin=False)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project information."))
        else:
            msg = \
                _("Insufficient privilege level to view project information.")
            messages.info(self.request, msg)

        if os_api.keystone.VERSIONS.active >= 3:
            domain_lookup = os_api.keystone.domain_lookup(self.request)
            for t in tenants:
                t.domain_name = domain_lookup.get(t.domain_id)
        return tenants


class UpdateQuotaView(forms.ModalFormView):
    form_class = kb_forms.UpdateForm
    template_name = 'kingbird/quota_management/update.html'
    success_url = reverse_lazy("horizon:kingbird:quota_management:index")
    submit_label = _("Update")

    def get_context_data(self, **kwargs):
        context = super(UpdateQuotaView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs['project_id']
        return context

    def get_initial(self, **kwargs):
        return {'project_id': self.kwargs['project_id']}


class SyncQuotaView(forms.ModalFormView):
    form_class = kb_forms.SyncQuotaForm
    template_name = 'kingbird/quota_management/sync.html'
    success_url = reverse_lazy("horizon:kingbird:quota_management:index")
    submit_label = _("Sync")

    def get_context_data(self, **kwargs):
        context = super(SyncQuotaView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs['project_id']
        return context

    def get_initial(self, **kwargs):
        return {'project_id': self.kwargs['project_id']}


class DeleteQuotaView(forms.ModalFormView):
    form_class = kb_forms.DeleteQuotaForm
    template_name = 'kingbird/quota_management/delete.html'
    success_url = reverse_lazy("horizon:kingbird:quota_management:index")
    submit_label = _("Delete")

    def get_context_data(self, **kwargs):
        context = super(DeleteQuotaView, self).get_context_data(**kwargs)
        context["project_id"] = self.kwargs['project_id']
        return context

    def get_initial(self, **kwargs):
        return {'project_id': self.kwargs['project_id']}


class DetailQuotaView(tables.DataTableView):
    table_id = "quota_info"
    table_class = kb_tables.QuotaDetailTable
    template_name = 'kingbird/quota_management/detail.html'

    def get_data(self, **kwargs):
        try:
            project_id = self.kwargs['project_id']
            response = kb_client.detail_quota(self.request, project_id)
            return response
        except Exception:
            msg = _('Unable to get details')
            redirect = reverse('horizon:kingbird:quota_management:index')
            exceptions.handle(self.request, msg, redirect=redirect)
