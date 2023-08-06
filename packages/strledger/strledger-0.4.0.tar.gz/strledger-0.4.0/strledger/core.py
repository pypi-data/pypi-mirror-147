import binascii
from enum import IntEnum
from typing import Optional, Union

from ledgerwallet.client import LedgerClient
from ledgerwallet.params import Bip32Path
from ledgerwallet.transport import enumerate_devices
from stellar_sdk import (
    Keypair,
    TransactionEnvelope,
    DecoratedSignature,
    FeeBumpTransactionEnvelope,
)

__all__ = [
    "get_default_client",
    "DeviceNotFoundException",
    "DEFAULT_KEYPAIR_INDEX",
    "Ins",
    "P1",
    "P2",
    "SW",
    "AppInfo",
    "StrLedger",
]

DEFAULT_KEYPAIR_INDEX = 0


class Ins(IntEnum):
    GET_PK = 0x02
    SIGN_TX = 0x04
    GET_CONF = 0x06
    SIGN_TX_HASH = 0x08


class P1(IntEnum):
    NO_SIGNATURE = 0x00
    SIGNATURE = 0x01
    FIRST_APDU = 0x00
    MORE_APDU = 0x80


class P2(IntEnum):
    NON_CONFIRM = 0x00
    CONFIRM = 0x01
    LAST_APDU = 0x00
    MORE_APDU = 0x80


class SW(IntEnum):
    OK = 0x9000
    CANCEL = 0x6985
    UNKNOWN_OP = 0x6C24
    MULTI_OP = 0x6C25
    NOT_ALLOWED = 0x6C66
    UNSUPPORTED = 0x6D00
    KEEP_ALIVE = 0x6E02


class DeviceNotFoundException(Exception):
    pass


def get_default_client() -> "StrLedger":
    devices = enumerate_devices()
    if len(devices) == 0:
        raise DeviceNotFoundException
    client = LedgerClient(devices[0])
    return StrLedger(client)


class AppInfo:
    def __init__(self, version: str, hash_signing_enabled: bool) -> None:
        self.version = version
        self.hash_signing_enabled = hash_signing_enabled

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.version == other.version
            and self.hash_signing_enabled == other.hash_signing_enabled
        )

    def __str__(self) -> str:
        return f"AppConfiguration(version='{self.version}', hash_signing_enabled={self.hash_signing_enabled})"


class StrLedger:
    def __init__(self, client: LedgerClient) -> None:
        self.client = client

    def get_app_info(self) -> AppInfo:
        data = self.client.apdu_exchange(
            ins=Ins.GET_CONF, sw1=P1.FIRST_APDU, sw2=P2.LAST_APDU
        )
        hash_signing_enabled = bool(data[0])
        version = f"{data[1]}.{data[2]}.{data[3]}"
        return AppInfo(version=version, hash_signing_enabled=hash_signing_enabled)

    def get_keypair(
        self,
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
        confirm_on_device: bool = False,
    ) -> Keypair:
        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        data = self.client.apdu_exchange(
            ins=Ins.GET_PK,
            data=path,
            sw1=P1.NO_SIGNATURE,
            sw2=P2.CONFIRM if confirm_on_device else P2.NON_CONFIRM,
        )
        keypair = Keypair.from_raw_ed25519_public_key(data)
        return keypair

    def sign_transaction(
        self,
        transaction_envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope],
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
    ) -> None:
        sign_data = transaction_envelope.signature_base()
        keypair = self.get_keypair(keypair_index=keypair_index)

        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        payload = path + sign_data
        signature = self._send_payload(payload)
        assert isinstance(signature, bytes)
        decorated_signature = DecoratedSignature(keypair.signature_hint(), signature)
        transaction_envelope.signatures.append(decorated_signature)

    def sign_transaction_hash(
        self,
        transaction_hash: Union[str, bytes],
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
    ) -> bytes:
        if isinstance(transaction_hash, str):
            transaction_hash = binascii.unhexlify(transaction_hash)
        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        payload = path + transaction_hash

        data = self.client.apdu_exchange(
            ins=Ins.SIGN_TX_HASH, data=payload, sw1=P1.FIRST_APDU, sw2=P2.LAST_APDU
        )
        return data

    def _send_payload(self, payload) -> Optional[Union[int, str]]:
        chunk_size = 255
        first = True
        while payload:
            if first:
                p1 = P1.FIRST_APDU
                first = False
            else:
                p1 = P1.MORE_APDU

            size = min(len(payload), chunk_size)
            if size != len(payload):
                p2 = P2.MORE_APDU
            else:
                p2 = P2.LAST_APDU

            resp = self.client.apdu_exchange(Ins.SIGN_TX, payload[:size], p1, p2)
            if resp:
                return resp
            payload = payload[size:]
