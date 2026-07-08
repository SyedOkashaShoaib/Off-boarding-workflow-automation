import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environment.get('DATABASE_URL', 'sqlite:///offboarding.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False