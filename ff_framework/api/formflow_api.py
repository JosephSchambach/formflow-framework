from ff_framework.context.context_logging import ContextLogger
from ff_framework.api.api_obj_config import api_obj_config
from ff_framework.api.mailgun_api import MailgunAPI
from time import sleep


class FormFlowAPI:
    def __init__(self, logger: ContextLogger, database, generators):
        self.logger = logger
        self.database = database
        self.generators = generators
        self._mailgun_api = MailgunAPI(logger=self.logger, database=self.database)
        self.obj_config = api_obj_config(self)
        
    def create(self, args, log = True, alert = False):
        arg_type = type(args)
        create_response = []
        if log:
            self.logger.log(f"Creating object of type {arg_type}", level='info')
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Processing {i+1} {arg_type} objects", level='info')
            kwargs = self.obj_config[arg.__class__.__name__]
            result = self._execute(arg, kwargs, alert=alert)
            if result is not None:
                actor = getattr(self, result["context_method"])
                action = getattr(actor, result["execution_method"])
                action_response = action(result["table"], result["columns"], result["values"])
                create_response.append(action_response)
        if log:
            self.logger.log(f"Created {len(create_response)} objects of type {arg_type}", level='info')
        return create_response if len(create_response) > 1 else create_response[0]
    
    def process(self, args, log = True, alert = False, retries = 0, retry_interval = 0):
        arg_type = type(args)
        process_response = []
        if log:
            self.logger.log(f"Processing object of type {arg_type}", level='info')
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Processing {i+1} {arg_type} objects", level='info')
            kwargs = self.obj_config[arg.__class__.__name__]
            result = self._execute(arg, kwargs, log=log, alert=alert, retries=retries, retry_interval=retry_interval)
            if result is not None:
                actor = getattr(self, result["context_method"])
                action = getattr(actor, result["execution_method"])
                action_response = action(result["table"], result["columns"], result["values"])
                process_response.append(action_response)
        if log:
            self.logger.log(f"Processed {len(process_response)} objects of type {arg_type}", level='info')
        return process_response if len(process_response) > 1 else process_response[0]
    
    def send(self, args, log = True, alert = False):
        arg_type = type(args)
        send_response = []
        if log:
            self.logger.log(f"Sending object of type {arg_type}", level='info')
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Sending {i+1} {arg_type} objects", level="info")
            kwargs = self.obj_config[arg.__class__.__name__]
            result = self._execute(arg, kwargs, log=log, alert=alert)
            if result is not None:
                send_response.append(result)
        if log:
            self.logger.log(f"Sent {len(send_response)} objects of type {arg_type}", level='info')
        return send_response if len(send_response) > 1 else send_response[0]
    
    def _execute(self, args, kwargs, log = None, alert = None, retries = 0, retry_interval = 0):
        for _ in range(retries + 1):
            try:
                parent_method = kwargs.get("parent_method")
                kwargs = kwargs.get("kwargs", {})
                attribute = kwargs.get("attribute", 'no attribute')
                if log:
                    self.logger.log(f"Processing class of type {attribute}", level='info')
                if not kwargs:
                    return parent_method(args)
                return parent_method(args, **kwargs)
            except Exception as e:
                if log: 
                    self.logger.log(f"Error processing {attribute}: {e}", level='error')
                if _ == retries - 1:
                    if alert:
                        self.logger.log(f"Failed to process {attribute} after {retries} retries", level='error')
                    raise e
                continue
    