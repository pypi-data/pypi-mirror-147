from dataclasses import dataclass

@dataclass
class ml_config:
    make_request_url: str

@dataclass
class jenkins_config:
    jenkins_job_name: str        
    Jenkins_url: str
    jenkins_user: str
    jenkins_pwd: str
    buildWithParameters: bool
    jenkins_params: dict

@dataclass
class api_config:
    jenkins_job_name: str        
    Jenkins_url: str
    jenkins_user: str
    jenkins_pwd: str
    buildWithParameters: bool
    jenkins_params: dict
    aws_stack_name = str
    model_name = str
    model_run_id = str