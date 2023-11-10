import importlib
import logging
import logging.config
import os
import warnings

ENVIRONMENT_VARIABLE = "UNNAX_AUTH_SETTINGS_MODULE"

class Settings:
    def __init__(self):
        
        # GENERAL
        self.PROJECT=''
        self.FLASK_APP='app.py'
        self.FLASK_ENV=''
        self.FLASK_DEBUG=1
        self.PORT=5000
        self.SECRET_KEY=''
        self.PROPAGATE_EXCEPTIONS=True
        self.PRESERVE_CONTEXT_ON_EXCEPTION=False
        self.SWAGGER_PATH=''

        # LOGGING
        self.LOG_LEVEL = logging.DEBUG
        self.LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
        self.LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        # DATABASE
        self.SQLALCHEMY_DATABASE_URI=''
    
        # OTHER
        self.TOKEN_EXPIRE_MINUTES=59
        self.TOKEN_EXPIRE_HOURS=0
      
        # Load selected environment
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        # Store environment name
        self.ENVIRONMENT = settings_module.split(".")[-1].lower()

        # Import environment
        mod = importlib.import_module(settings_module)
        for setting in dir(mod):
            if setting.startswith("_"):
                continue
            setting_value = getattr(mod, setting)
            if hasattr(self, setting) and setting_value:
                try:
                    setting_value = eval(setting_value)
                except Exception:
                    setattr(self, setting, setting_value)
                else:
                    if isinstance(setting_value, dict):
                        dst = getattr(self, setting)
                        dst.update(setting_value)
                    else:
                        setattr(self, setting, setting_value)
      
     
   
# Set default environment
os.environ.setdefault(ENVIRONMENT_VARIABLE, "conf.settings")

# Global variable to import settings
cfg = Settings()