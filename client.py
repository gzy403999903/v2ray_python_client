from v2ray.com.core.app.proxyman.command import command_pb2
from v2ray.com.core.app.proxyman.command import command_pb2_grpc
from v2ray.com.core.common.protocol import user_pb2
from v2ray.com.core.common.serial import typed_message_pb2
from v2ray.com.core.proxy.vmess import account_pb2
import json
import uuid
import grpc

INBOUND_TAG = 'master_server'
SERVER_PORT = '10202'
SERVER_ADDRESS = '102.182.109.139'


def add_user(uuid, email, level=0, alter_id=10):
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = command_pb2_grpc.HandlerServiceStub(channel)

    resp = stub.AlterInbound(
        command_pb2.AlterInboundRequest(
            tag=INBOUND_TAG,
            operation=typed_message_pb2.TypedMessage(
                type=command_pb2._ADDUSEROPERATION.full_name,
                value=command_pb2.AddUserOperation(
                    user=
                    user_pb2.User(
                        level=level,
                        email=email,
                        account=typed_message_pb2.TypedMessage(
                            type=account_pb2._ACCOUNT.full_name,
                            value=account_pb2.Account(
                                id=uuid,
                                alter_id=alter_id
                            ).SerializeToString()
                        )
                    )
                ).SerializeToString()
            )
        )
    )
    print(resp)


if __name__ == '__main__':
    uid = uuid.uuid4().hex
    email = uid + '@email.com'
    add_user(uid, email)

    data = {}
    data['id'] = uid
    data['email'] = email
    data['level'] = 0
    data['alterId'] = 10

    file = open(uid + '.json', encoding='utf-8', mode='w')
    file.write(json.dumps(data, indent=4))

    print(json.dumps(data, indent=4))
