from op import OP_CODE_FUNCTIONS
from script import Script
from io import BytesIO

if __name__ == "__main__":
    script_pubkey = Script([0x76, 0x76, 0x95, 0x93, 0x56, 0x87])
    script_sig = Script([0x82])
    combined_script = script_sig + script_pubkey
    print(combined_script.evaluate(0))
