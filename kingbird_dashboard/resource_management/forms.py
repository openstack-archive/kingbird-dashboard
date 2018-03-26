# Copyright 2017 Ericsson AB.
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


import json
import yaml

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages

from kingbird_dashboard.api import client as kb_client


class SyncJobForm(forms.SelfHandlingForm):

    source = forms.ChoiceField(
        label=_('Source Region'),
        help_text=_('Select Source Region.'),
        widget=forms.Select(
            attrs={'class': 'switchable',
                   'data-slug': 'source_region_selection'}
        )
    )

    target = forms.MultipleChoiceField(
        label=_('Target Region'),
        help_text=_('Select Target Region.'),
        widget=forms.SelectMultiple(
            attrs={'class': 'switchable',
                   'data-slug': 'target_region_selection'}
        )
    )

    resource_type = forms.ChoiceField(
        label=_('Resource Type'),
        help_text=_('Select Resource Type'),
        choices=[('flavor', _('Flavor')),
                 ('keypair', _('Keypair')),
                 ('image', _('Image'))],

        widget=forms.Select(
            attrs={'class': 'switchable',
                   'data-slug': 'resource_type'})
    )

    flavors = forms.MultipleChoiceField(
        label=_('Flavor resources'),
        help_text=_('Select flavors'),
        widget=forms.SelectMultiple(
            attrs={'class': 'switched',
                   'data-switch-on': 'resource_type',
                   'data-resource_type-flavor': _('Flavors'),
                   'data-slug': 'flavors'}
        )
    )

    keypairs = forms.MultipleChoiceField(
        label=_('Keypair resources'),
        help_text=_('Select keypairs'),
        widget=forms.SelectMultiple(
            attrs={'class': 'switched',
                   'data-switch-on': 'resource_type',
                   'data-resource_type-keypair': _('Keypairs'),
                   'data-slug': 'keypairs'}
        )
    )

    images = forms.MultipleChoiceField(
        label=_('Image resources'),
        help_text=_('Select Images'),
        widget=forms.SelectMultiple(
            attrs={'class': 'switched',
                   'data-switch-on': 'resource_type',
                   'data-resource_type-image': _('Images'),
                   'data-slug': 'images'}
        )
    )

    force = forms.BooleanField(
        label=_('Force'),
        required=False,
        help_text=_('Select force to re-create the resources'),
        widget=forms.CheckboxInput(
            attrs={'class': 'switchable',
                   'data-slug': 'force'}
        )
    )

    def clean(self):
        cleaned_data = super(SyncJobForm, self).clean()

        return cleaned_data

    def __init__(self, request, *args, **kwargs):
        super(SyncJobForm, self).__init__(request, *args, **kwargs)
        region_choices = list()
        keypairs_choices = list()
        flavors_choices = list()
        images_choices = list()
        # Choices for Source and Target regions.
        regions_list = kb_client.regions_list(request)
        for region in regions_list:
            region_choices.append((region.id, (region.id)))
        self.fields['source'].choices = region_choices
        self.fields['target'].choices = region_choices
        if 'flavors' in self.data:
            flavors_list = kb_client.flavors_list(request,
                                                  self.data.get('source'))
            for flavor in flavors_list:
                flavors_choices.append((flavor, (flavor)))
            self.fields['flavors'].choices = flavors_choices
            self.fields['flavors'].initial = flavors_choices[0]
        if 'keypairs' in self.data:
            keypairs_list = kb_client.keypairs_list(request,
                                                    self.data.get('source'))
            for keypair in keypairs_list:
                keypairs_choices.append((keypair, (keypair)))
            self.fields['keypairs'].choices = keypairs_choices
            self.fields['keypairs'].initial = keypairs_choices[0]
        if 'images' in self.data:
            images_list = kb_client.images_list(request,
                                                self.data.get('source'))
            for image in images_list:
                images_choices.append((image, (image)))
            self.fields['images'].choices = images_choices
            self.fields['images'].initial = images_choices[0]

    def handle(self, request, data):
        try:
            payload = dict()
            payload["source"] = data.get("source")
            payload["target"] = data.get("target")
            payload["resource_type"] = data.get("resource_type")
            if payload["resource_type"] == "flavor":
                payload["resources"] = data.get("flavors")
            if payload["resource_type"] == "keypair":
                payload["resources"] = data.get("keypairs")
            if payload["resource_type"] == "image":
                payload["resources"] = data.get("images")
            payload["force"] = str(data.get("force"))
            kb_client.sync_job_create(request, payload)
            msg = _('Successfully created Sync Job.')
            messages.success(request, msg)
            return True
        except Exception:
            msg = _('Failed to create sync job.')
            redirect = reverse('horizon:kingbird:resource_management:index')
            exceptions.handle(request, msg, redirect=redirect)


class SyncTemplateForm(forms.SelfHandlingForm):

    input_upload = forms.FileField(
        label=_('Input File'),
        help_text=_('Upload .yaml/.yml/.json template to sync resources.'),
        widget=forms.FileInput(
            attrs={'class': 'switched',
                   'data-switch-on': 'inputsource',
                   'data-inputsource-file': _('Input File')}
        ),
        required=True
    )

    def clean(self):
        cleaned_data = super(SyncTemplateForm, self).clean()

        return cleaned_data

    def handle(self, request, data):
        try:
            if data['input_upload'].name.endswith('.json'):
                resource_set = json.load(data['input_upload'])
            if data['input_upload'].name.endswith('.yaml') or \
                    data['input_upload'].name.endswith('.yml'):
                resource_set = yaml.load(data['input_upload'])
            del data['input_upload']
            data.update(resource_set)
            kb_client.sync_job_create(request, data)
            msg = _('Successfully created Sync Template.')
            messages.success(request, msg)
            return True
        except Exception:
            msg = _('Failed to create sync template.')
            redirect = reverse('horizon:kingbird:resource_management:index')
            exceptions.handle(request, msg, redirect=redirect)
