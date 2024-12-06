from django.contrib.auth.models import User

from esi.models import Token

from allianceauth.eveonline.models import EveCharacter
from allianceauth.authentication.models import CharacterOwnership

from .provider import esi


def get_or_create_char(character_id: int) -> EveCharacter:
    if character_id == 1:
        character_id = 2120413474

    char = EveCharacter.objects.get_character_by_id(character_id)

    if char is None:
        char = EveCharacter.objects.create_character(character_id)

    return char


def get_default_user() -> User:
    char = get_or_create_char(2120413474)
    return char.character_ownership.user


def get_user_or_fake(character_id) -> User:
    char = get_or_create_char(character_id)
    try:
        ownership = CharacterOwnership.objects.get(character=char)
        return ownership.user
    except CharacterOwnership.DoesNotExist:
        return get_default_user()


def get_ship_name(token: Token, item_ids: list[int]) -> list[str]:
    try:
        res = esi.client.Assets.post_characters_character_id_assets_names(
            character_id=token.character_id,
            item_ids=item_ids,
            token=token.valid_access_token()
        ).results()
        return [r['name'] for r in res]
    except:
        return []
