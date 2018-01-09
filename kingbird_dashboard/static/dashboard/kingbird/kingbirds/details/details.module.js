/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  /**
   * @ngdoc overview
   * @ngname horizon.dashboard.kingbird.kingbirds.details
   *
   * @description
   * Provides details features for Kingbird.
   */
  angular
    .module('horizon.dashboard.kingbird.kingbirds.details', [
      'horizon.app.core',
      'horizon.framework.conf'
    ])
    .run(registerDetails);

  registerDetails.$inject = [
    'horizon.app.core.openstack-service-api.kingbird_dashboard',
    'horizon.dashboard.kingbird.kingbirds.basePath',
    'horizon.dashboard.kingbird.kingbirds.resourceType',
    'horizon.framework.conf.resource-type-registry.service'
  ];

  function registerDetails(
    api,
    basePath,
    resourceType,
    registry
  ) {
    registry.getResourceType(resourceType)
      .setLoadFunction(loadFunction)
      .detailsViews.append({
        id: 'kingbirdDetailsOverview',
        name: gettext('Overview'),
        template: basePath + 'details/overview.html'
      });

    function loadFunction(identifier) {
      return api.getKingbird(identifier);
    }
  }
})();
