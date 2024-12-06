import os

from dotenv import load_dotenv
from dkdc_util import get_dkdc_dir


class Env:
    def __init__(self):
        # environment variable template
        self.env_var_template = "DKDC_{}"

        # load env
        load_dotenv()
        load_dotenv(os.path.join(os.getcwd(), ".env"))
        load_dotenv(os.path.join(os.path.expanduser("~"), ".env"))
        load_dotenv(os.path.join(get_dkdc_dir(), ".env"))

    def __call__(self, key: str = None, value: str = None) -> dict | str:
        assert not (
            key is None and value is not None
        ), "key must be provided if value is provided"

        if key is None:
            return self.to_dict()

        if value is not None:
            self.put(key, value)

        return self.get(key)

    def get(self, key: str) -> str:
        key = key.upper()

        return Env._try_cast(os.environ.get(self.env_var_template.format(key)))

    def put(self, key: str, value: str) -> str:
        key = key.upper()
        value = str(value).strip().strip('"')

        os.environ[self.env_var_template.format(key)] = value

        return self.get(key)

    def to_dict(self) -> dict:
        env_vars = {
            key: value
            for key, value in os.environ.items()
            if key.startswith(self.env_var_template.format(""))
        }
        env_vars = {key: Env._try_cast(value) for key, value in env_vars.items()}

        return env_vars

    @staticmethod
    def _try_cast(value: str) -> str | int | float | bool:
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                if value.lower() == "true":
                    return True
                elif value.lower() == "false":  # UGGGGHHHHHHHHH
                    return False
                return value
