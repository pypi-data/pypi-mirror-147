class Message(object):
    """
    Message Class:  Data structure defined to encapsulate 
    the data and other related information in single object.
    """

    MSG_SER_REQUEST = 0
    MSG_SER_RECEIVE = 1
    MSG_SER_RESPONSE = 2
    MSG_SER_RELEASE = 3
    MSG_SER_RELAY = 4
    MSG_CLI_REQUEST = 5
    MSG_CLI_RESPONSE = 6
    CLI_PROBE_REQUEST = 7
    SER_PROBE_REQUEST = 8

    MSG_TYPE = [
        'MSG_SER_REQUEST',
        'MSG_SER_RECEIVE',
        'MSG_SER_RESPONSE',
        'MSG_SER_RELEASE',
        'MSG_SER_RELAY',
        'MSG_CLI_REQUEST',
        'MSG_CLI_RESPONSE',
        'CLI_PROBE_REQUEST',
        'SER_PROBE_REQUEST'
    ]


    def __init__(self, msg_type, from_dc, to_dc, data=None, msg_id=None):
        self.msg_id = msg_id
        self.msg_type = msg_type
        self.from_dc = from_dc
        self.to_dc = to_dc
        self.data = data


if __name__ == '__main__':
    pass
