from cinder.api import common


class ViewBuilder(common.ViewBuilder):

    _collection_name = "sessions"

    def summary_list(self, request, sessions, session_count=None):
        return self._list_view(self.summary, request, sessions,
                               session_count)

    def detail_list(self, request, sessions, session_count=None):
        return self._list_view(self.summary, request, sessions, session_count,
                               coll_name=self._collection_name + '/detail')

    def summary(self, request, session):
        return {
            'session': {
                'initiator_ip': session['ip'],
                'session_id': session['sid'],
                'target_id': session['tid'],
            }
        }

    def detail(self, request, session):
        return self.summary(request, session)

    def _list_view(self, func, request, sessions, session_count,
                   coll_name=_collection_name):
        sessions_list = [func(request, session)['session'] for session in sessions]

        sessions_dict = {self._collection_name: snapshots_list}

        return sessions_dict
