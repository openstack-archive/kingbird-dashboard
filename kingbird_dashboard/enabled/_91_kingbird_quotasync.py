# Copyright (c) 2018 Ericsson AB.
# All Rights Reserved.
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

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'default'

# The display name of the PANEL_GROUP. Required.
PANEL = 'quota_management'

# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_DASHBOARD = 'kingbird'

# Python panel class of the PANEL to be added.
ADD_PANEL = 'kingbird_dashboard.quota_management.panel.QuotaManagement'

# Static CSS files to be added to Kingbird.
ADD_SCSS_FILES = ['dashboard/kingbird_dashboard/css/style.css']

AUTO_DISCOVER_STATIC_FILES = True

