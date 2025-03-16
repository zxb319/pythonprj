import os.path
import uuid


class DevConfig:
    JWT_KEY = uuid.uuid4().hex
    JWT_EXP_SECS = 3600 * 1

    BASE_PATH=os.path.dirname(os.path.relpath(__file__))


Config = DevConfig
