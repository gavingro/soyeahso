import os
import warnings

import dotenv


def validate_env(variable: str) -> str:
    """Get the environment variable value at the provided key."""
    dotenv.load_dotenv()
    if variable not in os.environ:
        warnings.warn(f"{variable} environment variable not found after loading .env.")
    return os.getenv(variable)
