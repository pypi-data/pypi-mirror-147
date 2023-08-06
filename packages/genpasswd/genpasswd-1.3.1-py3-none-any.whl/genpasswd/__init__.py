"""Generate a strong password which includes alphabets, numbers, special characters"""

__version__ = '1.3.1'

from .genpasswd import PasswordGenerator
from .__main__ import get_argument, generate_password, main
