from dotenv import load_dotenv
from os import environ
from os.path import join
from os.path import dirname
import os
def basepath(*args):
    """Joints path since basepath."""
    return join(dirname(__file__), '../../', *args)

def load_environment():
    env = os.getenv("ENV_TYPE", "dev")
    basepath('config', 'env.{}'.format(
        environ.get('APP_ENV', env)
    ))
    load_dotenv(basepath('config', 'env.{}'.format(
        environ.get('APP_ENV', env)
    )))
