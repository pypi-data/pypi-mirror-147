import time
import cbor2
from waiter import wait
from .candid import decode, Types
from .identity import *
from .constants import *
from .utils import to_request_id
from .certificate import lookup


def sign_request(req, iden):
    req_id = to_request_id(req)
    msg = IC_REQUEST_DOMAIN_SEPARATOR + req_id
    sig = iden.sign(msg)
    envelop = {
        'content': req,
        'sender_pubkey': sig[0],
        'sender_sig': sig[1]
    }
    return req_id, cbor2.dumps(envelop)

class Agent:
    def __init__(self, identity, client, nonce_factory=None, ingress_expiry=300, root_key=IC_ROOT_KEY):
        self.identity = identity
        self.client = client
        self.ingress_expiry = ingress_expiry
        self.root_key = root_key
        self.nonce_factory = nonce_factory

    def get_principal(self):
        return self.identity.sender()

    def get_expiry_date(self):
        return int(time.time() + self.ingress_expiry) * 10**9

    def query_endpoint(self, canister_id, data):
        ret = self.client.query(canister_id, data)
        return cbor2.loads(ret)

    def call_endpoint(self, canister_id, request_id, data):
        self.client.call(canister_id, request_id, data)
        return request_id

    def read_state_endpoint(self, canister_id, data):
        result = self.client.read_state(canister_id, data)
        return result

    def query_raw(self, canister_id, method_name, arg, return_type = None, effective_canister_id = None):
        req = {
            'request_type': "query",
            'sender': self.identity.sender().bytes,
            'canister_id': Principal.from_str(canister_id).bytes if isinstance(canister_id, str) else canister_id.bytes,
            'method_name': method_name,
            'arg': arg,
            'ingress_expiry': self.get_expiry_date()
        }
        _, data = sign_request(req, self.identity)
        result = self.query_endpoint(canister_id if effective_canister_id is None else effective_canister_id, data)
        if result['status'] == 'replied':
            return decode(result['reply']['arg'], return_type)
        elif result['status'] == 'rejected':
            return result['reject_message']

    def update_raw(self, canister_id, method_name, arg, return_type = None, effective_canister_id = None, **kwargs):
        req = {
            'request_type': "call",
            'sender': self.identity.sender().bytes,
            'canister_id': Principal.from_str(canister_id).bytes if isinstance(canister_id, str) else canister_id.bytes,
            'method_name': method_name,
            'arg': arg,
            'ingress_expiry': self.get_expiry_date()
        }
        req_id, data = sign_request(req, self.identity)
        eid = canister_id if effective_canister_id is None else effective_canister_id
        _ = self.call_endpoint(eid, req_id, data)
        # print('update.req_id:', req_id.hex())
        status, result = self.poll(eid, req_id, **kwargs)
        if status == 'rejected':
            raise Exception('Rejected: ' + result.decode())
        elif status == 'replied': 
            return decode(result, return_type)
        else:
            raise Exception('Timeout to poll result, current status: ' + str(status))
            
            

    def read_state_raw(self, canister_id, paths):
        req = {
            'request_type': 'read_state',
            'sender': self.identity.sender().bytes,
            'paths': paths, 
            'ingress_expiry': self.get_expiry_date(),
        }
        _, data = sign_request(req, self.identity)
        ret = self.read_state_endpoint(canister_id, data)
        if ret == b'Invalid path requested.':
            raise ValueError('Invalid path requested!')
        elif ret == b'Could not parse body as read request: invalid type: byte array, expected a sequence':
            raise ValueError('Could not parse body as read request: invalid type: byte array, expected a sequence')
        d = cbor2.loads(ret)
        cert = cbor2.loads(d['certificate'])
        return cert

    def request_status_raw(self, canister_id, req_id):
        paths = [
            ['request_status'.encode(), req_id],
        ]
        cert = self.read_state_raw(canister_id, paths)
        status = lookup(['request_status'.encode(), req_id, 'status'.encode()], cert)
        if (status == None):
            return status, cert
        else:
            return status.decode(), cert

    def poll(self, canister_id, req_id, delay=1, timeout=float('inf')):
        status = None
        for _ in wait(delay, timeout):
            status, cert = self.request_status_raw(canister_id, req_id)
            if status == 'replied' or status == 'done' or status  == 'rejected':
                break
        
        if status == 'replied':
            path = ['request_status'.encode(), req_id, 'reply'.encode()]
            res = lookup(path, cert)
            return status, res
        elif status == 'rejected':
            path = ['request_status'.encode(), req_id, 'reject_message'.encode()]
            msg = lookup(path, cert)
            return status, msg
        else:
            return status, _
