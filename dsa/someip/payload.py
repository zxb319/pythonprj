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


class BaseData:
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
    BASE_TYPEs = set(x.value.lower() for x in PACK_SIGN_MAP)

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


class String:
    class EncodingType(enum.Enum):
        UTF8 = 'utf-8'

    ENCODING_TYPEs = {
        EncodingType.UTF8,
    }

    def __init__(self, val: str, encoding_type: EncodingType = EncodingType.UTF8):
        self.val = val

        if encoding_type not in String.ENCODING_TYPEs:
            raise Exception(rf'not support type : {encoding_type}')
        self.encoding_type = encoding_type

    def __bytes__(self):
        bom = b'\xEF\xBB\xBF'
        end = b'\x00'
        val_bytes = self.val.encode(self.encoding_type.value)
        val_len = len(val_bytes) + len(bom) + len(end)
        val_len_bytes = bytes(BaseData(val_len, LEN_TYPE))
        return val_len_bytes + bom + val_bytes + end

    @classmethod
    def from_bytes(cls, type_: EncodingType, bytes_: bytes):
        if type_ not in cls.ENCODING_TYPEs:
            raise Exception(rf'not support type : {type_}')
        return bytes_[LEN_BYTE_COUNT + 3:-1].decode(type_.value)


class Array:
    def __init__(self, elements: List):
        self.elements = elements

    def __bytes__(self):
        elements_bytes = [bytes(e) for e in self.elements]
        elements_count = len(elements_bytes)
        return bytes(BaseData(elements_count, LEN_TYPE)) + b''.join(elements_bytes)


class Struct:
    def __init__(self, elements: dict):
        self.elements = elements

    def __bytes__(self):
        return b''.join(bytes(e) for e in self.elements.values())


def _pyobj_to_payload_obj(pyobj):
    if isinstance(pyobj, tuple):
        if len(pyobj) != 2:
            raise Exception(rf'tuple length must be 2.')
        if not isinstance(pyobj[0], int):
            raise Exception(rf'first tuple elem must be int')
        if pyobj[1].lower() not in BaseData.BASE_TYPEs:
            raise Exception(rf'second tuple elem must in {BaseData.BASE_TYPEs}')
        pyobj = (pyobj[0], BaseType(pyobj[1].lower()))
        return BaseData(*pyobj)
    elif isinstance(pyobj, str):
        return String(pyobj)
    elif isinstance(pyobj, list):
        return Array([_pyobj_to_payload_obj(e) for e in pyobj])
    elif isinstance(pyobj, dict):
        return Struct({k: _pyobj_to_payload_obj(v) for k, v in pyobj.items()})
    else:
        raise Exception(rf'wrong type {type(pyobj)}')


def payload_to_bytes(payload):
    payload_obj = _pyobj_to_payload_obj(payload)
    return bytes(payload_obj)


def bytes_to_payload(bytes_, payload_data_structure):
    payload_obj = _pyobj_to_payload_obj(payload_data_structure)

    pos = 0

    def _parse_bytes(payload):
        nonlocal pos
        if isinstance(payload, BaseData):
            cur_byte_count = byte_count(payload.type)
            pos += cur_byte_count
            return BaseData.from_bytes(payload.type, bytes_[pos - cur_byte_count:pos])

        elif isinstance(payload, String):
            str_len = BaseData.from_bytes(LEN_TYPE, bytes_[pos:pos + LEN_BYTE_COUNT])
            pos += LEN_BYTE_COUNT + str_len
            return String.from_bytes(payload.encoding_type, bytes_[pos - (LEN_BYTE_COUNT + str_len):pos])
        elif isinstance(payload, Array):
            arr_len = BaseData.from_bytes(LEN_TYPE, bytes_[pos:pos + LEN_BYTE_COUNT])
            ret = []
            pos += LEN_BYTE_COUNT
            for i in range(arr_len):
                cur_elem_p = payload.elements[i]
                elem = _parse_bytes(cur_elem_p)
                ret.append(elem)

            return ret

        elif isinstance(payload, Struct):
            ret = {}
            for cur_mem_name, cur_mem_p in payload.elements.items():
                ret[cur_mem_name] = _parse_bytes(cur_mem_p)

            return ret

        else:
            raise Exception(rf'unknown payload type {type(payload)}')

    ret = _parse_bytes(payload_obj)
    if pos != len(bytes_):
        raise Exception(rf'payload and bytes not match')

    return ret


if __name__ == '__main__':
    p = {
        "d": (-1, 'SINT16'),
        "c": (2, 'UINT16'),
        "bb": {
            'aa': ["zxb"] * 1 + ["张新波"] * 2
        },
        "a": (4, 'UINT64'),
    }

    bytes_p = payload_to_bytes(p)

    print(bytes_p.hex())

    p1 = {
        "d": (0, 'UINT16'),
        "c": (0, 'UINT16'),
        "bb": {
            'aa': [""] * 3
        },
        "a": (0, 'UINT64'),
    }
    parsed = bytes_to_payload(bytes_p, p1)

    print(parsed)
