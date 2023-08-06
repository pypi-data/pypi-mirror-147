from dataclasses import dataclass

@dataclass
class HttpSigRc:
    key: str
    secret: str
    algorith: str
    headers: str
