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
   * @ngname horizon.dashboard.kingbird.kingbirds.actions
   *
   * @description
   * Provides all of the actions for Kingbirds.
   */
  angular
    .module('horizon.dashboard.kingbird.kingbirds.actions', [
      'horizon.framework',
      'horizon.dashboard.kingbird'
    ])
    .run(registerKingbirdActions);

  registerKingbirdActions.$inject = [
    'horizon.framework.conf.resource-type-registry.service',
    'horizon.framework.util.i18n.gettext',
    'horizon.dashboard.kingbird.kingbirds.create.service',
    'horizon.dashboard.kingbird.kingbirds.update.service',
    'horizon.dashboard.kingbird.kingbirds.delete.service',
    'horizon.dashboard.kingbird.kingbirds.resourceType'
  ];

  function registerKingbirdActions (
    registry,
    gettext,
    createKingbirdService,
    updateKingbirdService,
    deleteKingbirdService,
    resourceType
  ) {
    var kingbirdsResourceType = registry.getResourceType(resourceType);
    kingbirdsResourceType.globalActions
      .append({
        id: 'createKingbirdAction',
        service: createKingbirdService,
        template: {
          type: 'create',
          text: gettext('Create Kingbird')
        }
      });

    kingbirdsResourceType.batchActions
      .append({
        id: 'batchDeleteKingbirdAction',
        service: deleteKingbirdService,
        template: {
          type: 'delete-selected',
          text: gettext('Delete Kingbirds')
        }
      });

    kingbirdsResourceType.itemActions
      .append({
        id: 'updateKingbirdAction',
        service: updateKingbirdService,
        template: {
          text: gettext('Update Kingbird')
        }
      })
      .append({
        id: 'deleteKingbirdAction',
        service: deleteKingbirdService,
        template: {
          type: 'delete',
          text: gettext('Delete Kingbird')
        }
      });
  }
})();
