import requests
import pandas as pd
import time

from .jenkins_job import JenkinsJob
from .config import api_config

# from jenkins_job import JenkinsJob
# from trigger_pipeline import trigger

class ModelAPI():
    '''
    Main class for API creation and deployment
    '''
    def __init__(self, api_config) -> None: #, api_jenkins_config, api_ml_config) -> None:
        # self.jenkins_config = api_jenkins_config
        # self.ml_config = api_ml_config
        self.api_config = api_config
        self.jenkins_job = JenkinsJob(self.api_config)

        

    def deploy_code(self):
        '''
        Managing model deploy.
        Printing job's status while job is building.
        Gives user output log from Jenkins job
        and if deployment is successfull API's url
        where user can test it with her custom data.
        '''

        data = self.jenkins_job.trigger(self.api_config)
        status = data.get('status')
        time.sleep(10)
        
        while 'job is triggered' in status  or 'job is building' in status:
            status = self.get_jenkins_job_status()
            time.sleep(5)

        status = self.jenkins_job.jenkins_job_status()
        output_log, url = self.get_jenkins_job_output_and_url()

        if status == 'success':
            print(f'API is succesfully deployed, you can call it with in {url}')
        else:
            print(f"Your API deploy failed, look at job_output to get more detailed info")

        return output_log, url


        
    
    def test_api(self, df: pd.DataFrame, api_url):
        '''
        User can test her API with custom
        data with this method. It's simple post request
        to API's url.
        '''

        dfj = df.to_json()
        r = requests.post(url = api_url, data = dfj)
        data = r.content

        if 'Endpoint request timed out' in r:
            return {
            'statusCode': 500,
            'error': 'Endpoint request timed out'
            }  

        else:

            data = r.content
            return {
                'statusCode': 200,
                'predictions': data
            }



    def get_jenkins_job_status(self):
        '''
        Gives user current status of Jenkins job.
        It comes handy if user wants to check if job is
        still build or is done.
        '''
        status = self.jenkins_job.jenkins_job_status()
        return status

    
    def get_jenkins_job_output_and_url(self):
        '''
        Gives user end of Jenkins job output log
        and API's url where user can test it.
        '''
        output = self.jenkins_job.job_output_log
        url = self.jenkins_job.api_url
        return output, url


if __name__ == "__main__":
    pass
