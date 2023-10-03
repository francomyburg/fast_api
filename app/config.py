from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='app/.env', env_file_encoding='utf-8',case_sensitive=False)

    database_hostname : str
    database_port : str
    user_db : str
    password_db : str
    database_name : str
    secret_key : str
    algorithm : str
    TOKEN_EXPIRE_MINUTES : int

    

    



settings = Settings()