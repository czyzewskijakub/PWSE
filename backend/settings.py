"""Application configuration file.
Every field should be correctly filled"""

DEBUG: bool = True
TESTING: bool = False
SECRET_KEY: str = ""
ALGORITHM: str = ""
EXP_TIME_MIN: float = 0
SQLALCHEMY_DATABASE_URI: str = "sqlite:////pwse/sqlite.db"


