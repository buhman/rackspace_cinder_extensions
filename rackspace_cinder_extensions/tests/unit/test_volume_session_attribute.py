import mock
import webob

from cinder import context
from cinder.tests.unit import utils as tests_utils
from cinder.tests.unit.api import fakes
import lunrclient

from rackspace_cinder_extensions import test
from rackspace_cinder_extensions.tests import fake_lunrclient


class VolumeSessionAttributeTestCase(test.TestCase):

    def setUp(self):
        super(VolumeSessionAttributeTestCase, self).setUp()
        self.context = context.RequestContext('admin', 'fake', True)

    def _get_response(self, volume_id='detail'):
        req = webob.Request.blank('/v2/fake/volumes/{}'.format(volume_id))
        req.method = 'GET'

        res = req.get_response(fakes.wsgi_app(fake_auth_context=self.context))

        return res

    @mock.patch.object(lunrclient.StorageExport, 'get',
                       side_effect=fake_lunrclient.fake_storage_export)
    def test_session_show(self, fake_storage_export):
        volume = tests_utils.create_volume(self.context)

        res = self._get_response(volume.id)
        print(res)
