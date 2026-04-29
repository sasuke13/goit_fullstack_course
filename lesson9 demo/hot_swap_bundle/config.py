from pydantic_settings import BaseSettings, SettingsConfigDict

# =========================================================
# HOT SWAP ZONE: uncomment exactly one scenario line
# =========================================================
ACTIVE_SCENARIO = "pair_tokens_stateless"
# ACTIVE_SCENARIO = "single_token"
# ACTIVE_SCENARIO = "pair_tokens_db"
# ACTIVE_SCENARIO = "pair_tokens_cookies"
# ACTIVE_SCENARIO = "single_token_bearer"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "sqlite:///./hot_swap_bundle.db"
    secret_key: str = "change_me_hot_swap_secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 7
    scenario: str = ACTIVE_SCENARIO


settings = Settings()
