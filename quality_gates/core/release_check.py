from atlassian import Jira
from quality_gates.core.check_time import convertTime, timeValidate
from quality_gates.utils.logger import logger
from quality_gates.settings import settings



class getJira:

    host = None
    token = None

    def __init__(self,host,token):
        self.jira = Jira(
            url=host,
            token=token)

        pass
    
    def checkIssue(self, issue_key):
        '''
        Check if issue exist
        '''
        try:
            self.jira.issue(issue_key)
            return True
        except Exception as e:
            logger.info(f"has exception: {e}")
            return False


    def jiraFilter(self, issue_key):
        '''
        Get fields from jira issue
        
        issue_type:
        11803 - Заявка на обслуживание с согласованием
        12406 - Change request
        
        status:
        11700 - Согласование
        10110 - На исполнении        
        '''
        try:
            issue = self.jira.issue(issue_key)
        except Exception as e:
            logger.error(e)
            return {
                "status": False,
                "message": f"{e}"
            }
        if issue['fields']['issuetype']['id']== '11803' or issue['fields']['issuetype']['id'] == '12406':
            if issue['fields']['status']['id'] == '11700':
                return {
                    "status": False,
                    "message": f"Issue status is not approved - current status is {issue['fields']['status']['name']}"
                    }
            elif issue['fields']['status']['id'] == '10110':
                startTime = convertTime(issue['fields']['customfield_10012'])
                logger.info(f"startTime: {startTime}")
                endTime = convertTime(issue['fields']['customfield_10013'])
                logger.info(f"endTime: {endTime}")
                if startTime is None or endTime is None:
                    logger.error("Can`t get time from issue")
                    return {
                        "status": False,
                        "message": "Can`t get time from issue"
                    }
                else:
                    try:
                        allow_deploy = timeValidate(startTime, endTime)
                        return allow_deploy
                    except Exception as e:
                        logger.error(e)
                        return {
                            "status": False,
                            "message": f"{e}"
                        }
            else:
                return {
                    "status": False,
                    "message": f"Issue status is not approved or not in progress - current status is {issue['fields']['status']['name']}"
                }
        else:
            return {
                "status": False,
                "message": f"Issue type is not a request for change - current type is {issue['fields']['issuetype']['name']}"
            }
         
            
    def comment_issue(self, issue_key, comment):
        '''
        Add comment to issue
        '''
        try:
            self.jira.issue_add_comment(issue_key, comment)
        except Exception as e:
            logger.error(e)
            return False
        return True


jira = getJira(settings.jira_host, settings.jira_token.get_secret_value())