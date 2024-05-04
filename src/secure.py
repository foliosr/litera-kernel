from secrets import randbelow
import hashlib
from typing import Optional
from src.config import Settings


class Secure:

    @staticmethod
    def sha256_str(in_put: str):
        out_put = hashlib.sha256(in_put.encode()).hexdigest()
        return out_put

    @staticmethod
    def code_generator(abc: Optional[str], length):
        if abc is None or "":
            abc = Settings.default_abc()
        list(abc)
        keys = []
        code = ''
        for i in range(length):
            keys.append(randbelow(len(abc) - 1))
        for i in range(len(keys)):
            for j in range(len(abc)):
                if keys[i] == j:
                    code += abc[j]
        return code
