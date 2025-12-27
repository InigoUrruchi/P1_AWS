import logging
import logging.handlers
import os
from datetime import datetime


class Logger():
    def __init__(self,type, base_dir="logs",):
        #Inicializar variables
        self.base_dir = base_dir
        self.type = type
        self.n = 0
        self.file_name = self.log_name()
        self.logger = self._create_logger()

        os.makedirs(base_dir, exist_ok=True)

    def log_name(self):

        #Fecha actual
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = os.path.join(self.base_dir, f"{self.type}_log_{today}_{self.n}.log")
        return file_name

    def _create_logger(self):
        logger = logging.getLogger(self.type)
        logger.setLevel(logging.INFO)

        #Crear rotacion de logs
        handler = logging.handlers.RotatingFileHandler(
            self.file_name,
            maxBytes= 500_000,
            backupCount= 5,
            encoding="utf-8"
        )

        if not logger.handlers:
            logger.addHandler(handler)

        return logger


    def write_log(self, data):
        #Escribir datos en el log
        self.logger.info(data)





    
