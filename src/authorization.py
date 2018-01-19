from datetime import timedelta


def initialize_jwt(jwt):

    @jwt.user_claims_loader
    def append_claims(user):
        return {
            "name": user.name,
            "email": user.email,
            "is_validated": user.is_validated,
            "groups": "temp"
        }

    @jwt.user_identity_loader
    def get_identity(user):
        return user.username


jwt_configs = {
    "JWT_SECRET_KEY": "temporary_secret_key",
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(minutes=30),
    "JWT_REFRESH_TOKEN_EXPIRES": timedelta(days=21),
    "JWT_IDENTITY_CLAIM": "sub"
}
