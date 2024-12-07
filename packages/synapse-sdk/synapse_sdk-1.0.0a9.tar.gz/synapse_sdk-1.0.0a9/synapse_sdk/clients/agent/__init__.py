from synapse_sdk.clients.agent.core import CoreClientMixin
from synapse_sdk.clients.agent.service import ServiceClientMixin


class AgentClient(CoreClientMixin, ServiceClientMixin):
    name = 'Agent'
    agent_token = None
    user_token = None
    tenant = None

    def __init__(self, base_url, agent_token, user_token=None, tenant=None):
        super().__init__(base_url)
        self.agent_token = agent_token
        self.user_token = user_token
        self.tenant = tenant

    def _get_headers(self):
        headers = {'Authorization': self.agent_token}
        if self.user_token:
            headers['SYNAPSE-User'] = f'Token {self.user_token}'
        if self.tenant:
            headers['SYNAPSE-Tenant'] = f'Token {self.tenant}'
        return headers
