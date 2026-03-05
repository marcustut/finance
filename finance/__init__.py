from ulid import ULID
from datetime import datetime

def uid() -> str:
    return str(ULID())

def now() -> datetime:
    return datetime.now()
  