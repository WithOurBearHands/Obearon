"""
CRUD operations for the database.
"""

from .role import get_friend_role
from .role import get_verify_role
from .role import get_hibernation_role
from .role import set_friend_role
from .role import set_verify_role
from .role import set_hibernation_role
from .verification import create_verification
from .verification import get_successful_verifications
from .verification import remove_verification
from .verification import update_warframe_name
from .warframe_player import create_warframe_player
from .warframe_player import get_warframe_players
from .warframe_player import get_warframe_players_name

__all__ = [
    "create_verification",
    "get_successful_verifications",
    "remove_verification",
    "update_warframe_name",
    "set_verify_role",
    "get_verify_role",
    "set_friend_role",
    "get_friend_role",
    "set_hibernation_role",
    "get_hibernation_role",
    "create_warframe_player",
    "get_warframe_players",
    "get_warframe_players_name",
]
