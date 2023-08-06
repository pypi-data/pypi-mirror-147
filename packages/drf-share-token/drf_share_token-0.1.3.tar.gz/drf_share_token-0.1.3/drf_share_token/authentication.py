from logging import getLogger


from rest_framework import authentication

from drf_share_token.tokens import decode
from drf_share_token.user import ShareTokenUser

logger = getLogger(__file__)

class ShareTokenAuthentication(authentication.BaseAuthentication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        raw_token = request.headers['Authorization'].split()

        if not len(raw_token) == 2 or raw_token[0].lower() != "token":
            return None

        jwt_token = raw_token[1]
        try:
            payload = decode(jwt_token)
            return ShareTokenUser(payload), None
        except Exception as e:
            logger.errot(e, exc_info=True)
            return None
