import enum
import re
import struct
from typing import List

BIG_ENDIAN = True
ENDIAN_SIGN = '>' if BIG_ENDIAN else '<'


class BaseType(enum.Enum):
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


def byte_count(base_type: BaseType):
    return int(re.search(r'\d+$', base_type.value).group(0)) // 8


LEN_TYPE = BaseType.UINT32
LEN_BYTE_COUNT = byte_count(LEN_TYPE)


class BaseDataPayload:
    PACK_SIGN_MAP = {
        BaseType.UINT8: 'B',
        BaseType.UINT16: 'H',
        BaseType.UINT32: 'I',
        BaseType.UINT64: 'Q',
        BaseType.SINT8: 'b',
        BaseType.SINT16: 'h',
        BaseType.SINT32: 'i',
        BaseType.SINT64: 'q',
        BaseType.BOOLEAN: 'B',
        BaseType.FLOAT32: 'f',
        BaseType.FLOAT64: 'd',
    }

    def __init__(self, val, type_: BaseType):
        self.val = val
        if type_ not in self.PACK_SIGN_MAP:
            raise Exception(rf'not support type : {type_}')
        self.type = type_

    def __bytes__(self):
        return struct.pack(rf'{ENDIAN_SIGN}{self.PACK_SIGN_MAP[self.type]}', self.val)

    @classmethod
    def from_bytes(cls, type_: BaseType, bytes_: bytes):
        return struct.unpack(rf'{ENDIAN_SIGN}{cls.PACK_SIGN_MAP[type_]}', bytes_)[0]


class StringPayload:
    class EncodingType(enum.Enum):
        UTF8 = 'utf-8'

    ENCODING_TYPEs = {
        EncodingType.UTF8,
    }

    def __init__(self, val: str, encoding_type: EncodingType = EncodingType.UTF8):
        self.val = val

        if encoding_type not in StringPayload.ENCODING_TYPEs:
            raise Exception(rf'not support type : {encoding_type}')
        self.encoding_type = encoding_type

    def __bytes__(self):
        bom = b'\xEF\xBB\xBF'
        end = b'\x00'
        val_bytes = self.val.encode(self.encoding_type.value)
        val_len = len(val_bytes) + len(bom) + len(end)
        val_len_bytes = bytes(BaseDataPayload(val_len, LEN_TYPE))
        return val_len_bytes + bom + val_bytes + end

    @classmethod
    def from_bytes(cls, type_: EncodingType, bytes_: bytes):
        if type_ not in cls.ENCODING_TYPEs:
            raise Exception(rf'not support type : {type_}')
        return bytes_[3:-1].decode(type_.value)


class ArrayPayload:
    def __init__(self, elements: List):
        self.elements = elements

    def __bytes__(self):
        elements_bytes = [bytes(e) for e in self.elements]
        elements_count = len(elements_bytes)
        return bytes(BaseDataPayload(elements_count, LEN_TYPE)) + b''.join(elements_bytes)


class StructPayload:
    def __init__(self, elements: dict):
        self.elements = elements

    def __bytes__(self):
        return b''.join(bytes(e) for e in self.elements.values())


def bytes_to_payload(bytes_, payload):
    pos = 0

    def _parse_bytes(payload):
        nonlocal pos
        if isinstance(payload, BaseDataPayload):
            cur_byte_count = byte_count(payload.type)
            pos += cur_byte_count
            return BaseDataPayload.from_bytes(payload.type, bytes_[pos - cur_byte_count:pos])

        elif isinstance(payload, StringPayload):
            str_len = BaseDataPayload.from_bytes(LEN_TYPE, bytes_[pos:pos + LEN_BYTE_COUNT])
            pos += LEN_BYTE_COUNT + str_len
            return StringPayload.from_bytes(payload.encoding_type, bytes_[pos - str_len:pos])
        elif isinstance(payload, ArrayPayload):
            arr_len = BaseDataPayload.from_bytes(LEN_TYPE, bytes_[pos:pos + LEN_BYTE_COUNT])
            ret = []
            pos += LEN_BYTE_COUNT
            for i in range(arr_len):
                cur_elem_p = payload.elements[i]
                elem = _parse_bytes(cur_elem_p)
                ret.append(elem)

            return ret

        elif isinstance(payload, StructPayload):
            ret = {}
            for cur_mem_name, cur_mem_p in payload.elements.items():
                ret[cur_mem_name] = _parse_bytes(cur_mem_p)

            return ret

        else:
            raise Exception(rf'unknown payload type {type(payload)}')

    ret = _parse_bytes(payload)
    if pos != len(bytes_):
        raise Exception(rf'payload and bytes not match')

    return ret


if __name__ == '__main__':
    p = StructPayload({
        "d": BaseDataPayload(-1, BaseType.SINT8),
        "c": BaseDataPayload(2, BaseType.UINT16),
        "bb": StructPayload({
            'aa': ArrayPayload([StringPayload("zxb"), ] * 3)
        }),
        "a": BaseDataPayload(4, BaseType.UINT64),
    })

    bytes_p = bytes(p)

    print(bytes_p)

    p1 = StructPayload({
        "d": BaseDataPayload(0, BaseType.SINT8),
        "c": BaseDataPayload(0, BaseType.UINT16),
        "bb": StructPayload({
            'aa': ArrayPayload([StringPayload("")] * 3)
        }),
        "a": BaseDataPayload(0, BaseType.UINT64),
    })
    parsed = bytes_to_payload(bytes_p, p1)

    print(parsed)
