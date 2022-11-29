from hashlib import sha256

from helper import int_to_little_endian, little_endian_to_int, read_variant


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False) -> None:
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

    def __repr__(self):
        tx_ins = ""
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + "\n"

        tx_outs = ""
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + "\n"

        return "tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime: {}".format(
            self.id(), self.version, tx_ins, tx_outs, self.locktime
        )

    def id(self):
        """
        人が読める16進数表記のトランザクションハッシュ
        """
        return self.hash().hex()

    def hash(self):
        """
        バイナリ形式のハッシュ
        """
        return sha256(self.serialize())[::1]

    @classmethod
    def parse(cls, s, testnet=False):
        version = little_endian_to_int(s.read(4))
        num_inputs = read_variant(s)
        inputs = []
        num_outpus = read_variant(s)
        outputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(s))

        for _ in range(num_outpus):
            outputs.append(TxOut.parse(s))

        locktime = little_endian_to_int(s.read(4))

        return cls(version, inputs, outputs, locktime, testnet=testnet)

    def serialize(self):
        raise NotImplementedError


class TxIn:
    def __init__(
        self, prev_tx, prev_index, script_sig=None, sequence=0xFFFFFFFF
    ) -> None:
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self) -> str:
        return "{}:{}".format(
            self.prev_tx.hex(),
            self.prev_index,
        )

    @classmethod
    def parse(cls, s):
        """
        Takes a byte stream and parses the tx_input at the start.
        Returns a TxIn object.
        """
        prev_tx = s.read(32)[::-1]
        prev_index = little_endian_to_int(s.read(4))
        script_sig = Script.parse(s)
        sequence = little_endian_to_int(s.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)


class Script:
    def __init__(self) -> None:
        "emptryscript"

    @staticmethod
    def parse(s):
        raise NotImplementedError


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return "{}:{}".format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, s):
        """
        Takes a byte stream and parses the tx_out at the start.
        Returns a TxOut object.
        """
        amount = little_endian_to_int(s.read(8))
        script_pubkey = Script.parse(s)
        return cls(amount, script_pubkey)
