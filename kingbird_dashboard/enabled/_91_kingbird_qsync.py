from django.utils.translation import ugettext_lazy as _

# The slug of the panel group to be added to HORIZON_CONFIG. Required.
PANEL_GROUP = 'default'

# The display name of the PANEL_GROUP. Required.
PANEL = 'quota_management'

# The slug of the dashboard the PANEL_GROUP associated with. Required.
PANEL_DASHBOARD = 'kingbird'

# Python panel class of the PANEL to be added
ADD_PANEL = 'kingbird_dashboard.quota_management.panel.QuotaManagement'
