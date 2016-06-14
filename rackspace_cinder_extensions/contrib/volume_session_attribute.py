#  Copyright 2013-2016 Rackspace US, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from oslo_config import cfg
from oslo_log import log as logging

from cinder.api import extensions
from cinder.api.openstack import wsgi
from lunrclient import client as lunr_api

from rackspace_cinder_extensions.views import sessions as session_views


LOG = logging.getLogger(__name__)
CONF = cfg.CONF
authorize = extensions.soft_extension_authorizer('volume',
                                                 'volume_session_attribute')


class VolumeSessionAttributeController(wsgi.Controller):

    _view_builder_class = session_views.ViewBuilder

    def _get_storage_api(self, req, resp_volume):
        db_volume = req.get_db_volume(resp_volume['id'])
        storage_url = 'http://{host}:8081'.format(**db_volume)
        storage_api = lunr_api.StorageClient(url=storage_url)

        return storage_api

    def _add_volume_session_attribute(self, req, resp_volume):
        storage_api = self._get_storage_api(req, resp_volume)

        try:
            export = storage_api.exports.get(resp_volume['id'])
        except Exception as err:
            err_msg = ('Storage api connection failed '
                       '(error: {}).'.format(err))
            LOG.warning(err_msg, resource=resp_volume)
            return

        sessions = self._view_builder.summary_list(req, export['sessions'])

        key = "{}:sessions".format(Volume_session_attribute.alias)
        resp_volume[key] = sessions['sessions']

    @wsgi.extends
    def show(self, req, resp_obj, id):
        context = req.environ['cinder.context']
        if authorize(context):
            volume = resp_obj.obj['volume']
            self._add_volume_session_attribute(req, volume)

    @wsgi.extends
    def detail(self, req, resp_obj):
        context = req.environ['cinder.context']
        if authorize(context):
            for volume in list(resp_obj.obj['volumes']):
                self._add_volume_session_attribute(req, volume)


class Volume_session_attribute(extensions.ExtensionDescriptor):
    """Expose volume session metadata."""

    name = "VolumeSessionAttribute"
    alias = "rs-vol-session-attr"
    namespace = ("http://docs.rackspace.com/volume/ext/"
                 "volume_session_attribute/api/v2")
    updated = "2016-06-10T19:55:31+00:00"

    def get_controller_extensions(self):
        controller = VolumeSessionAttributeController()
        extension = extensions.ControllerExtension(self, 'volumes', controller)
        return [extension]
