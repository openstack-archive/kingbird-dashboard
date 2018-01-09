/**
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.app.core.openstack-service-api')
    .factory('horizon.app.core.openstack-service-api.kingbird_dashboard', API);

  API.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service',
    'horizon.framework.util.i18n.gettext'
  ];

  function API(apiService, toastService, gettext) {
    var service = {
      getKingbird: getKingbird,
      getKingbirds: getKingbirds,
      createKingbird: createKingbird,
      updateKingbird: updateKingbird,
      deleteKingbird: deleteKingbird
    };

    return service;

    ///////////////////////////////
    // Kingbirds

    function getKingbird(id) {
      return apiService.get('/api/kingbird_dashboard/kingbirds/' + id)
        .error(function() {
          var msg = gettext('Unable to retrieve the Kingbird with id: %(id)s.');
          toastService.add('error', interpolate(msg, {id: id}, true));
        });
    }

    function getKingbirds() {
      return apiService.get('/api/kingbird_dashboard/kingbirds/')
        .error(function() {
          toastService.add('error', gettext('Unable to retrieve the Kingbirds.'));
        });
    }

    function createKingbird(params) {
      return apiService.put('/api/kingbird_dashboard/kingbirds/', params)
        .error(function() {
          var msg = gettext('Unable to create the Kingbird with name: %(name)s');
          toastService.add('error', interpolate(msg, { name: params.name }, true));
        });
    }

    function updateKingbird(id, params) {
      return apiService.post('/api/kingbird_dashboard/kingbirds/' + id, params)
        .error(function() {
          var msg = gettext('Unable to update the Kingbird with id: %(id)s');
          toastService.add('error', interpolate(msg, { id: params.id }, true));
        });
    }

    function deleteKingbird(id, suppressError) {
      var promise = apiService.delete('/api/kingbird_dashboard/kingbirds/', [id]);
      return suppressError ? promise : promise.error(function() {
        var msg = gettext('Unable to delete the Kingbird with id: %(id)s');
        toastService.add('error', interpolate(msg, { id: id }, true));
      });
    }
  }
}());
