class Config:
    SECRET_KEY = 'e7c76718715412042d18e84e66788f033b019fecb08df2bfdc452f5746724443'

class DevConfig(Config):
    DEBUG= True

config = {
    'dev': DevConfig
}