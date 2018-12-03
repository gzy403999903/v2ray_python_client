from v2ray.com.core.app.proxyman.command import command_pb2
from v2ray.com.core.app.proxyman.command import command_pb2_grpc

from v2ray.com.core.app.stats.command import command_pb2 as stats_command_pb2
from v2ray.com.core.app.stats.command import \
    command_pb2_grpc as status_command_pb2_grpc

from v2ray.com.core.common.protocol import user_pb2
from v2ray.com.core.common.serial import typed_message_pb2
from v2ray.com.core.proxy.vmess import account_pb2
from v2ray.com.core.common.protocol import headers_pb2
from v2ray.com.core.common.net import port_pb2

from v2ray.com.core import config_pb2
from v2ray.com.core.app.proxyman import config_pb2 as proxy_config_pb2
import json
import uuid
import grpc

INBOUND_TAG = 'master_server'
SERVER_PORT = '10010'
SERVER_ADDRESS = '144.**.202'

SECURITY_TYPE_UNKNOWN = 0
SECURITY_TYPE_LEGACY = 1
SECURITY_TYPE_AUTO = 2
SECURITY_TYPE_AES128_GCM = 3
SECURITY_TYPE_CHACHA20_POLY1305 = 4
SECURITY_TYPE_NONE = 5


def add_user(uuid, email, security_type=SECURITY_TYPE_LEGACY, level=0,
             alter_id=32):
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
                                alter_id=alter_id,
                                security_settings=headers_pb2.SecurityConfig(
                                    type=security_type)
                            ).SerializeToString()
                        )
                    )
                ).SerializeToString()
            )
        )
    )
    print(resp)


def remove_user(email):
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = command_pb2_grpc.HandlerServiceStub(channel)

    resp = stub.AlterInbound(
        command_pb2.AlterInboundRequest(
            tag=INBOUND_TAG,
            operation=typed_message_pb2.TypedMessage(
                type=command_pb2._REMOVEUSEROPERATION.full_name,
                value=command_pb2.RemoveUserOperation(
                    email=email
                ).SerializeToString()
            )
        )
    )
    print(resp)


# todo finish add_inbound
# def add_inbound(tag):
#     channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
#     stub = command_pb2_grpc.HandlerServiceStub(channel)
#
#     resp = stub.AddInbound(
#         command_pb2.AlterInboundRequest(
#             inbound=config_pb2.InboundHandlerConfig(
#                 tag=tag,
#                 receiver_settings=typed_message_pb2.TypedMessage(
#                     type=proxy_config_pb2._RECEIVERCONFIG.full_name,
#                     value=proxy_config_pb2.ReceiverConfig(
#                         port_range=port_pb2.PortRange(
#                             From=30,
#                             To=20
#                         ),
#                         listen=None,
#                         allocation_strategy=None,
#                         stream_settings=None,
#                         receive_original_destination=None,
#                         domain_override=None
#                     ).SerializeToString()
#                 ),
#                 proxy_settings=typed_message_pb2.TypedMessage(
#                     type=command_pb2._ADDUSEROPERATION.full_name,
#                     value=command_pb2.RemoveUserOperation(
#                         email=email
#                     ).SerializeToString()
#                 ),
#
#             )
#         )
#     )
#     print(resp)


def get_stats(email=None, tag=None, uplink=True):
    if email:
        s = ''.join(['user>>>', email, '>>>traffic>>>'])
    else:
        s = ''.join(['inbound>>>', email, '>>>traffic>>>'])
    if uplink:
        s = s + '>>>uplink'
    else:
        s = s + '>>>downlink'
    channel = grpc.insecure_channel('%s:%s' % (SERVER_ADDRESS, SERVER_PORT))
    stub = status_command_pb2_grpc.StatsServiceStub(channel)

    resp = stub.GetStats(
        stats_command_pb2.GetStatsRequest(
            name=s,
            reset=False
        )
    )
    print(resp)


if __name__ == '__main__':
    # get_stats('user>>>lin@*.win>>>traffic>>>downlink')
    get_stats('tyf@*.win')
    # uid = uuid.uuid4().hex
    # email = uid + '@email.com'
    # add_user(uid, email, SECURITY_TYPE_CHACHA20_POLY1305)
    #
    # data = {}
    # data['id'] = uid
    # data['email'] = email
    # data['level'] = 0
    # data['alterId'] = 32
    #
    # file = open(uid + '.json', encoding='utf-8', mode='w')
    # file.write(json.dumps(data, indent=4))
    #
    # print(json.dumps(data, indent=4))
