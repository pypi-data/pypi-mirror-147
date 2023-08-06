import json
import requests
import re

class JenkinsJob():
    '''
    Class to manage and interact with Jenkins job
    which deploying user's code to AWS
    '''
    def __init__(self, api_config) -> None:

        self.jenkins_job_name = api_config.jenkins_job_name        
        self.Jenkins_url = api_config.Jenkins_url
        self.jenkins_user = api_config.jenkins_user
        self.jenkins_pwd = api_config.jenkins_pwd
        self.buildWithParameters = api_config.buildWithParameters
        self.jenkins_params = api_config.jenkins_params

        self.job_output_log = ''
        self.api_url = ''
                
        
    def trigger(self):
        '''
        Try to trigger Jenkins job
        and inform user about 
        '''

        auth= (self.jenkins_user, self.jenkins_pwd)
        crumb_data= requests.get("{0}/crumbIssuer/api/json".format(self.Jenkins_url),auth = auth,headers={'content-type': 'application/json'})
        
        if str(crumb_data.status_code) == "200":

            if self.buildWithParameters:
                data = requests.get("{0}/job/{1}/buildWithParameters".format(self.Jenkins_url,self.jenkins_job_name),auth=auth,params=self.jenkins_params,headers={'content-type': 'application/json','Jenkins-Crumb':crumb_data.json()['crumb']})
            else:
                data = requests.get("{0}/job/{1}/build".format(self.Jenkins_url,self.jenkins_job_name),auth=auth,params=self.jenkins_params,headers={'content-type': 'application/json','Jenkins-Crumb':crumb_data.json()['crumb']})

            if str(data.status_code) == "201":
                jenkins_job_status = "Jenkins Deploy Jenkins job is triggered"

            else:
                jenkins_job_status = "Failed to trigger the Jenkins job"
        
        else:
            jenkins_job_status = "Couldn't fetch Jenkins-Crumb"
            
            raise 

                                    
        return {
            'statusCode': 200,
            'status': jenkins_job_status
        }


    def jenkins_job_status(self):
        '''
        gives user current status of
        running job
        '''
            
        try:
                auth= (self.jenkins_user, self.jenkins_pwd)
                while True:
                        data = requests.get(
                            "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/api/json"),
                            auth = auth,
                            headers={'content-type': 'application/json'}).json()

                        if data['building']:
                                print('job is building')
                                return 'job is building'
                        else:
                                if data['result'] == "SUCCESS":
                                    self.job_output_log, self.api_url = self.jenkins_console_output_succed_job()
                                    return 'success'
                                else:
                                    self.job_output_log, self.api_url = self.jenkins_console_output_fail_job()
                                    return  'fail'

                
        except Exception as e:
                print (str(e))
                return False

    def jenkins_console_output_succed_job(self):
        '''
        Jenkins job output for user if 
        job ends up successfully.
        '''
        auth= (self.jenkins_user, self.jenkins_pwd)
        r = requests.get(
                            "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/consoleText"),
                            auth = auth,
                            headers={'content-type': 'application/json'})

        data = r.content.decode('utf-8','ignore')
        end_of_log = data[-1_500:]
        url = self.get_url(data)

        return end_of_log, url


    def jenkins_console_output_fail_job(self):
        '''
        Jenkins job output for user if 
        job failed.
        '''
        auth= (self.jenkins_user, self.jenkins_pwd)
        r = requests.get(
                            "{0}/crumbIssuer/api/json".format(f"{self.Jenkins_url}/job/{self.jenkins_job_name}/lastBuild/consoleText"),
                            auth = auth,
                            headers={'content-type': 'application/json'})

        data = r.content.decode('utf-8','ignore')
        end_of_log = data[-1_500:]
        url = 'Job deploy failed, API was not deployed'

        return end_of_log, url

    def get_url(self, output):
        '''
        Takes Jenkins job output as argument
        and find API url address in it.
        '''
        complete_url = ''

        try:
            found_url = re.search("YOU CAN CALL YOUR API IN THIS URL:\'(.+?)\' RUNNING ON AWS LAMBDA", output).group(1)
            complete_url = str(found_url+'/predict')
            return complete_url
        except AttributeError:
            not_found = 'Not able to find API url inside Jenkins job output log file' 
            return not_found



if __name__ == "main":
    pass