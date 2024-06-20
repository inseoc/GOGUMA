class logManager:
    
    def __init__(self):
        
        self.response_log = dict()
    
    
    def reset_log(self):
        
        self.response_log = dict()
        
    def success_log(self, log, *args):
        
        log['status'] = 200
        log['response'] = "SUCCESS"
        
        log["result"] = args if args else ""
        
        return log

    def err_log(self, log, err_msg, *args):
        
        # if err_msg:
        log['status'] = 401
        log['response'] = err_msg
        
        log["result"] = args if args else ""
        
        return log        
        
        