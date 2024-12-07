class Endpoint:
    """
    Zalo Open API endpoints

    This class is defined with class methods to avoid changing attributes.
    The idea was using StrEnum but it's not supported until Python 3.11.
    """

    @classmethod
    def message_send(cls, is_hash_phone: bool = False, is_rsa: bool = False) -> str:
        """
        Get message send endpoint
        """
        if is_hash_phone:
            return "https://business.openapi.zalo.me/message/template/hashphone"
        if is_rsa:
            return "https://business.openapi.zalo.me/rsa/message/template"
        return "https://business.openapi.zalo.me/message/template"

    @classmethod
    def message_inquiry_status(cls) -> str:
        """
        Get message inquiry status endpoint
        """
        return "https://business.openapi.zalo.me/message/status"

    @classmethod
    def message_quota(cls) -> str:
        """
        Get message quota endpoint
        """
        return "https://business.openapi.zalo.me/message/quota"

    @classmethod
    def rsa_key_gen(cls) -> str:
        """
        Get RSA key gen endpoint
        """
        return "https://business.openapi.zalo.me/rsa/key/gen"

    @classmethod
    def rsa_key_get(cls) -> str:
        """
        Get RSA key get endpoint
        """
        return "https://business.openapi.zalo.me/rsa/key/get"

    @classmethod
    def template_list(cls) -> str:
        """
        Get template list endpoint
        """
        return "https://business.openapi.zalo.me/template/all"

    @classmethod
    def template_detail(cls) -> str:
        """
        Get template detail endpoint
        """
        return "https://business.openapi.zalo.me/template/info/v2"

    @classmethod
    def access_token(cls) -> str:
        """
        Get access token endpoint
        """
        return "https://oauth.zaloapp.com/v4/oa/access_token"
