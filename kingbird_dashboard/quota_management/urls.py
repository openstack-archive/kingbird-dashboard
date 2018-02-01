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

from django.conf.urls import url

from kingbird_dashboard.quota_management import views

PROJECT_ID = r'^(?P<project_id>[^/]+)/%s$'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(PROJECT_ID % 'update', views.UpdateQuotaView.as_view(),
        name='update'),
    url(PROJECT_ID % 'sync', views.SyncQuotaView.as_view(), name='sync'),
    url(PROJECT_ID % 'delete', views.DeleteQuotaView.as_view(),
        name='delete'),
    url(PROJECT_ID % 'detail', views.DetailQuotaView.as_view(),
        name='detail'),
]
