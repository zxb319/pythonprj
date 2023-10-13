import enum
import struct
from typing import List


class BasePayload:
    def __init__(self, is_big_endian: bool):
        self.is_big_endian = is_big_endian

    def __bytes__(self):
        raise NotImplementedError()


class BaseDataPayload(BasePayload):
    class Type(enum.Enum):
        BOOLEAN = 'boolean'

        UINT8 = 'uint8'
        UINT16 = 'uint16'
        UINT32 = 'uint32'
        UINT64 = 'uint64'

        SINT8 = 'sint8'
        SINT16 = 'sint16'
        SINT32 = 'sint32'
        SINT64 = 'sint64'

        FLOAT32 = 'float32'
        FLOAT64 = 'float64'

    PACK_SIGN_MAP = {
        Type.UINT8: 'B',
        Type.UINT16: 'H',
        Type.UINT32: 'I',
        Type.UINT64: 'Q',
        Type.SINT8: 'b',
        Type.SINT16: 'h',
        Type.SINT32: 'i',
        Type.SINT64: 'q',
        Type.BOOLEAN: 'B',
        Type.FLOAT32: 'f',
        Type.FLOAT64: 'd',
    }

    def __init__(self, val, type_: 'BaseDataPayload.Type', is_big_endian: bool):
        super().__init__(is_big_endian)

        self.val = val

        if type_ not in BaseDataPayload.PACK_SIGN_MAP:
            raise Exception(rf'not support type : {type_}')
        self.type = type_

        self.endian_sign = '>' if is_big_endian else '<'

    def __bytes__(self):
        return struct.pack(rf'{self.endian_sign}{BaseDataPayload.PACK_SIGN_MAP[self.type]}', self.val)


class StringPayload(BasePayload):
    class EncodingType(enum.Enum):
        UTF8 = 'utf-8'

    ENCODING_TYPEs = {
        EncodingType.UTF8,
    }

    def __init__(self, val: str, encoding_type: 'StringPayload.EncodingType',
                 is_big_endian: bool, is_fixed_length: bool, max_length: int, str_len_type: BaseDataPayload.Type = None):
        super().__init__(is_big_endian)
        self.val = val

        if encoding_type not in StringPayload.ENCODING_TYPEs:
            raise Exception(rf'not support type : {encoding_type}')
        self.encoding_type = encoding_type

        self.is_fixed_length = is_fixed_length
        self.max_length = max_length
        self.str_len_type = str_len_type

    def __bytes__(self):
        bom = b'\xEF\xBB\xBF'
        end = b'\x00'
        val_bytes = self.val.encode(self.encoding_type.value)
        if self.max_length < len(val_bytes) + len(bom) + len(end):
            raise Exception(rf'{self.val} is too long than length:{self.max_length}')
        if self.is_fixed_length:
            return bom + val_bytes + b'\x00' * (self.max_length - len(val_bytes)) + end

        else:
            val_len = len(val_bytes) + len(bom) + len(end)
            val_len_bytes = bytes(BaseDataPayload(val_len, self.str_len_type, self.is_big_endian))
            return val_len_bytes + bom + val_bytes + end


class ArrayPayload(BasePayload):
    def __init__(self, elements: List[BasePayload], is_big_endian: bool, is_fixed_length: bool, max_length: int,
                 len_type: BaseDataPayload.Type = None):
        super().__init__(is_big_endian)
        self.elements = elements
        self.is_fixed_length = is_fixed_length
        self.max_length = max_length
        self.len_type = len_type

    def __bytes__(self):
        elements_bytes = [bytes(e) for e in self.elements]
        if self.max_length < len(elements_bytes):
            raise Exception(rf'Array is too long than length:{self.max_length}')
        if self.is_fixed_length:
            return b''.join(elements_bytes) + b'\x00' * len(elements_bytes[0]) * (self.max_length - len(elements_bytes))
        else:
            elements_count = len(elements_bytes)
            return bytes(BaseDataPayload(elements_count, self.len_type, self.is_big_endian)) + b''.join(elements_bytes)


class StructPayload(BasePayload):
    def __init__(self, elements: List[BasePayload], is_big_endian: bool):
        super().__init__(is_big_endian)
        self.elements = elements

    def __bytes__(self):
        return b''.join(bytes(e) for e in self.elements)


def hex_num_to_bytes(hex_str: str, is_big_endian, bit_count: int):
    if hex_str[:2].lower() == '0x':
        hex_str = hex_str[2:]
    if bit_count != len(hex_str) * 4:
        raise Exception(rf'bit count of 0x{hex_str} is not {bit_count}')

    ret = bytes.fromhex(hex_str)
    if is_big_endian:
        return ret
    else:
        return b''.join(reversed(ret))


class SomeIpPacket:
    class MessageType(enum.Enum):
        REQUEST = b'\x00'
        REQUEST_NO_RETURN = b'\x01'
        NOTIFICATION = b'\x02'
        RESPONSE = b'\x80'
        ERROR = b'\x81'
        TP_REQUEST = b'\x20'
        TP_REQUEST_NO_RETURN = b'\x21'
        TP_NOTIFICATION = b'\x22'
        TP_RESPONSE = b'\xa0'
        TP_ERROR = b'\xa1'

    class ReturnCode(enum.Enum):
        E_OK = b'\x00'

    def __init__(self, service_id: str, method_id: str,
                 client_id: str, session_id: str,
                 protocol_version: str, interface_version: str, message_type: 'SomeIpPacket.MessageType', return_code: 'SomeIpPacket.ReturnCode',
                 payload: bytes):
        self.service_id = hex_num_to_bytes(service_id, True, 16)
        self.method_id = hex_num_to_bytes(method_id, True, 16)
        self.client_id = hex_num_to_bytes(client_id, True, 16)
        self.session_id = hex_num_to_bytes(session_id, True, 16)
        self.protocol_version = hex_num_to_bytes(protocol_version, True, 8)
        self.interface_version = hex_num_to_bytes(interface_version, True, 8)
        self.message_type = message_type.value
        self.return_code = return_code.value
        self.payload = payload

    def __bytes__(self):
        length = 4 + 4 + len(self.payload)
        return (self.service_id + self.method_id +
                bytes(BaseDataPayload(length, BaseDataPayload.Type.UINT32, True)) +
                self.client_id + self.session_id +
                self.protocol_version + self.interface_version + self.message_type + self.return_code +
                self.payload)


if __name__ == '__main__':
    print(bytes.fromhex('0102'))
