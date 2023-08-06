from webform.models.definition import Action

class Login():
        def __init__(self,rcic_account):
                self.rcic_account=rcic_account
        
        def login(self):
                return [
                        {
                                "action_type":Action.GotoPage.value,
                                "url":"https://prson-srpel.apps.cic.gc.ca/en/rep/login"
                        },
                        {
                                "action_type":Action.Login.value,
                                "account":self.rcic_account['account'],
                                "password":self.rcic_account['password'],
                                "account_element_id": "#username",
                                "password_element_id": "#password",
                                "login_button_id":"body > pra-root > pra-localized-app > main > div > pra-login-page > pra-login > div > div > form > button"
                }]
