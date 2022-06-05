from hashlib import sha256
from helper import little_endian_to_int, int_to_little_endian

class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False) -> None:
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs 
        self.locktime = locktime
        
    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        
        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'
        
        return 'tx: {}\nversion: {}\ntx_ins:\n{}tx_outs:\n{}locktime: {}'.format(self.id(), self.version, tx_ins, tx_outs, self.locktime)

    def id(self):
        '''
        人が読める16進数表記のトランザクションハッシュ
        '''
        return self.hash().hex()

    def hash(self):
        '''
        バイナリ形式のハッシュ
        '''
        return sha256(self.serialize())[::1]

    @classmethod
    def parse(cls, s, testnet=False):
        version = little_endian_to_int(s)
        return cls(version, None, None, None, testnet=testnet)
