import uuid


class DevConfig:
    JWT_KEY=uuid.uuid4().hex
    JWT_EXP_SECS=3600*1


Config=DevConfig