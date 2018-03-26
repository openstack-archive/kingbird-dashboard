# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
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

from django.conf.urls import url

from kingbird_dashboard.resource_management import views

SYNCJOB = r'^(?P<job_id>[^/]+)/%s$'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(SYNCJOB % 'detail', views.DetailView.as_view(), name='detail'),
    url(r'^create_sync_job$', views.CreateSyncJobView.as_view(),
        name='create_sync_job'),
    url(r'^create_sync_template$', views.CreateSyncTemplateView.as_view(),
        name='create_sync_template'),
    url(r'^load_flavors$', views.load_flavors, name='load_flavors'),
    url(r'^load_keypairs$', views.load_keypairs, name='load_keypairs'),
    url(r'^load_images$', views.load_images, name='load_images'),
]
