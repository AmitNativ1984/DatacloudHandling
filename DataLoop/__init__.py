import dtlpy as dl
import logging
FORMAT = "[%(asctime)s][%(levelname)s][%(module)s][%(funcName)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logging.getLogger(__name__)

class establish_dataloop_connection:
    def __init__(self):
        self.Client_ID = 'hfmoGbcc7XxBmRz8ZenJmS0CADOuC95I'
        self.Client_secret = 'lFcRgAdiRo5uaxa-hVoIIGvRqZ8xiyrCjXqWBtUlVq1blKMfPmvE90bzPFoYosXP'
        self.email= 'elbit@dataloop.ai'
        self.Password = 'ElbitDatal@@p!'

        dl.login_secret(self.email, self.Password, self.Client_ID, self.Client_secret)
        logging.info("successfully connected to dataloop server")
        dl.projects.list().print()

        project = dl.projects.get(project_name="Elbit")
        project.datasets.list().print()