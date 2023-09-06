from re import A
import requests
import pxpshell
import json
import barracuda

class Tenant:
    
    #initializes the tenant object 
    def __init__(self,*args):

       self.name = ""
       self.api = ""
       self.token = ""
       self.client_secret = ""
       self.client_id = ""
       self.tenant_id = ""
       self.app_id = ""
       self.thumb_print = ""
       self.user_list = []
       self.curr_user = ""
       self.UPNs = []
       self.groups = []
       self.auth = {"Authorization": 'Bearer ' + self.token,
               "Content-Type": "application/json"}

       if(len(args) == 2):
            self.name = args[0]
            self.api = 0
       elif len(args) == 7:
            self.name = args[0]
            self.client_secret = args[1]
            self.client_id = args[2]
            self.tenant_id = args[3]
            self.app_id = args[4]
            self.thumb_print = args[5]
            self.api = args[6]
       else:
            print("Could not load the object")
            
            '''
        self.token = ""
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.name = name
        self.appid = app_id
        self.thumb_print = thumb_print
        '''
       

        #self.get_token()       asd
        #self.get_user_list()

    def spam_ops(self, client, target, api):
        if api == 1:
            print("API path")
        else:
            print("Barracuda path")

    def group_op(self, user, toGroup, remove, fromGroup):

        c = -1
        for i in self.groups:
            c+=1
            if i[0] == fromGroup:
                break

        
        url = "https://graph.microsoft.com/v1.0/groups/" + self.groups[toGroup][1] + "/members/$ref"

        body = {
                "@odata.id": "https://graph.microsoft.com/v1.0/directoryObjects/" + self.UPNs[user][1]
            }

        url_delete = "https://graph.microsoft.com/v1.0/groups/"+ self.groups[c][1] +  "/members/" + self.UPNs[user][1] + "/$ref"
        
        if (remove == True):
            try:
                response = requests.delete(url_delete, headers = self.auth)
                print(response)
            except:
                print("error")
        else:
           try:
                response = requests.post(url, json = body, headers = self.auth)
                print(response)
           except:
                print("Error")



    def get_groups(self):

        self.get_token()
        
        url = "https://graph.microsoft.com/v1.0/groups"

        try:
            response = requests.get(url, headers = self.auth)
            for i in response.json()['value']:
                self.groups.append([i['displayName'], i['id']])
        except:
            print("error3")


    def get_usr_groups(self, user):
        url = "https://graph.microsoft.com/v1.0/users/" + user + "/memberOf"
        groups = []
        try:
            response = requests.get(url, headers = self.auth)
            for i in response.json()['value']:
                groups.append(i['displayName'])
        except:
            print("error2")

        return groups

    def change_info(self, user, firstN, lastN, displN, emailAddy):

      
       url = "https://graph.microsoft.com/v1.0/users/" + user
       
       body = {
           "givenName": firstN,
           "surname": lastN,
           "displayName": displN,
           "userPrincipalName": emailAddy
           }

       if emailAddy == "":
           del body['userPrincipalName']
       if firstN == "":
           del body['givenName']
       if lastN == "":
            del body['surname']
       if displN == "":
            del body['displayName']
       try:
           response  = requests.patch(url, json = body, headers = self.auth)
           print(response)

       except:
           print("error")

       

    
    def change_MFA(self):
        print("change mfa")

      
        url = "https://graph.microsoft.com/v1.0/users/{}"
        body = {
                "phoneNumber": "",
                "phoneType": "mobile",
                }
        try:
            response = requests.patch(url, json = body, headers = self.auth)
            #x = response.json()
            print(str(response))
        except:
            print("error validating auth token")


    

    def get_cals(self, user):

        url = "https://graph.microsoft.com/v1.0/users/" + user + "/calendars"

        try:
            response = requests.get(url, headers = self.auth)
            x = response.json()
            print(x)
            cal_list = []
            count = 0
            
            
            for i in x["value"]:
                cal_list.append(x["value"][count]["name"] + "|" + x["value"][count]["id"])
                count+=1
        except:
            print("error validating auth token")

        return cal_list

    #delegate email access via exov2 module  
    def delegate_em(self, manage, sendas, sendonbehalf, forwarding, fromUser, toUser, remove ):
      

       cmd = f"Connect-ExchangeOnline -CertificateThumbPrint '{self.thumb_print}' -AppID '{self.app_id}' -Organization '{self.name}'"
       
       if remove == True:
           if manage == True:
               cmd += "; Remove-MailboxPermission -Identity " + fromUser + " -User " + toUser + " -AccessRights FullAccess" + " -Confirm:$false"
           if sendas == True:
               cmd += "; Remove-RecipientPermission " + fromUser + " -Trustee " + toUser + " -AccessRights SendAs"+ " -Confirm:$false"
           if sendonbehalf == True:
               cmd += "; Set-Mailbox -Identity " + fromUser + " -GrantSendOnBehalfTo $null"+ " -Confirm:$false"
           if forwarding == True:
               cmd += "; Set-Mailbox -Identity "+ fromUser + " -ForwardingAddress $null" + " -Confirm:$false"
       else:
           if manage == True:
               cmd += "; Add-MailboxPermission -Identity " + fromUser + " -User " + toUser + " -AccessRights FullAccess" + " -Confirm:$false"
           if sendas == True:
                cmd += "; Add-RecipientPermission " + fromUser + " -Trustee " + toUser + " -AccessRights SendAs"+ " -Confirm:$false"
           if sendonbehalf == True:
               cmd += "; Set-Mailbox -Identity " + fromUser + " -GrantSendOnBehalfTo " + toUser+ " -Confirm:$false"
           if forwarding == True:
               cmd += "; Set-Mailbox -Identity "+ fromUser + " -ForwardingAddress "+ toUser + " -Confirm:$false"

       x = pxpshell.pxpowershell()
       x.start_process()
       result = x.run(cmd)
       print(result.decode())
        
       x.stop_process()
    
    #delegate calendar permissions
    def delegate_cal(self, fromUser, toUser, remove, cal_name, cal_id, editor, reviewer, owner):
        
        print("TRYING TO " + cal_name  + " " + cal_id)
       # url = "https://graph.microsoft.com/v1.0/users/"
        #headers = {'Authorization': 'Bearer ' + self.token}

        print(self.thumb_print + " " + self.appid + " " + self.name)
        cmd = f"Connect-ExchangeOnline -CertificateThumbPrint '{self.thumb_print}' -AppID '{self.appid}' -Organization '{self.name}'"

       
        if cal_name == "Calendar":
            path = "Calendar"
        else:
            path = "Calendar\\" + cal_name

        if remove == True:
            cmd += "; Remove-MailboxFolderPermission -Identity " + fromUser + ":\\" + path + " -User " + toUser + " -Confirm:$false"
        else:
            if editor == True:
                cmd += "; Add-MailboxFolderPermission -Identity " + fromUser + ":\\" + path + " -User " + toUser + " -AccessRights PublishingEditor -Confirm:$false"
            if reviewer == True:
                cmd += "; Add-MailboxFolderPermission -Identity " + fromUser + ":\\" + path + " -User " + toUser + " -AccessRights Reviewer -Confirm:$false"
            if owner == True:
                cmd += "; Add-MailboxFolderPermission -Identity " + fromUser + ":\\" + path + " -User " + toUser + " -AccessRights Owner -Confirm:$false"
            
       
        x = pxpshell.pxpowershell()
        x.start_process()
        result = x.run(cmd)
        print(result.decode())

        x.stop_process
        
        '''
        cmd = f"Connect-ExchangeOnline -CertificateThumbPrint '{self.thumb_print}' -AppID '{self.appid}' -Organization '{self.name}'"
        if remove == True:
            cmd += "; Remove-MailboxFolderPermission -Identity " + fromUser + ":\Calendar -User " + toUser + " -Confirm:$false"
        else:
            cmd += "; Add-MailboxFolderPermission -Identity " + fromUser + ":\Calendar -User " + toUser + " -AccessRights Editor -Confirm:$false"
        x = pxpshell.pxpowershell()
        x.start_process()
        result = x.run(cmd)
        print(result.decode())
        x.stop_process()
        '''

    #get a list of users in the tenant
    def get_user_list(self):
        count = 0
        url = "https://graph.microsoft.com/v1.0/users"
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.get(url, headers = headers)
        data = response.json()
        UPNs = []
        
        if response.status_code == 200:
            for item in data['value']:
                UPNs.append([data['value'][count]['userPrincipalName'],data['value'][count]['id']] )
                count += 1
            print("UPNs - 200")
            self.UPNs = UPNs
            return UPNs
        else:
            return 0

    #reset the password of a user
    def reset_pw(self, value, force_ch, window, pw):
        
        if(self.check_token()):
            print("Token invalid")
            return 0
        else:
            window.statusWindow.append("Resetting password for " + str(value) + " " + pw)

            data = {
                    "passwordProfile":{
                        "forceChangePasswordNextSignIn": force_ch,
                        "password": pw
                        }
                    }
            auth = {"Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json"}

            url = "https://graph.microsoft.com/v1.0/users/" + value

            try:
                response = requests.patch(url, json=data, headers = auth)
            except Exception as e:
                window.statusWindow.append(e)
        
            if str(response.status_code) == "204":
                window.statusWindow.append("Password for " + str(value) + " successfully reset;force change: " + str(force_ch))
                return 1
            else:
                window.statusWindow.append("Error resetting password for " + value)
                return 0

 

    #check if the api token is valid
    def check_token(self):
        

        #print("Checking if " + self.token + " Is valid")
 
        url = "https://graph.microsoft.com/v1.0/organization"

        try:
             response = requests.get(url, headers = self.auth)
             x = response.json()
             print(x["value"][0]["verifiedDomains"][0])
        except:
             print("error validating auth token")

    #get graph api token 
    def get_token(self):

        print("Getting token for " + self.name)
        
        obj = {  
               "grant_type": "client_credentials",
               "client_secret": self.client_secret, 
               "client_id": self.client_id,
               "scope": "https://graph.microsoft.com/.default"
               }

        url = 'https://login.microsoftonline.com/{' + self.tenant_id + '}/oauth2/v2.0/token'
        x = requests.post(url, obj)
        response = x.json()
        self.token = response["access_token"]
        self.auth = {"Authorization": 'Bearer ' + self.token,
               "Content-Type": "application/json"}
        

    #update the display name of a user
    def update_usr(self):
        try:
            self.check_token()
            first_name = input("Please enter your first name: ")
            while not first_name.isalpha():
                print("Invalid input! First name must contain only letters.")
                first_name = input("Please enter your first name: ")
            last_name = input("Please enter your last name: ")
            while not last_name.isalpha():
                print("Invalid input! Last name must contain only letters.")
                last_name = input("Please enter your last name: ")
            display_name = first_name + " " + last_name

            data   ={
                  "displayName": display_name,
                  "givenName": first_name,
                  "surname": last_name
                    }
      
           
            print(self.curr_user[1])
            url = f"https://graph.microsoft.com/v1.0/users/{self.curr_user[0]}"
            response = requests.patch(url, json = data, headers=self.auth)
            response.raise_for_status()
            print("User information updated successfully!")
        except Exception as e:
            print("Error occured when updating name", e)
                

    def print_tenant(self):
        print(self.name + " " + self.client_secret + " " + self.client_id + " " + self.tenant_id)

    def return_self(self):
        return (self.name)# + " " + self.client_secret + " " + self.client_id + " " + self.tenant_id) 

    def select_user(self):
        if len(self.token) < 2:
            self.get_token()

        if len(self.user_list) < 5:
            print("d")
            self.user_list = self.get_user_list()
        
        count = 0
        UPN = []
        choice = input("Username: ")
        if choice == "0":
            return 2
        print(self.user_list)
        for user in self.user_list:
            
            if choice.lower() in user[0].lower():
                UPN = user
                print("Found match")
                count += 1


        if count == 1:
            self.curr_user = UPN 
            print("Selected " + UPN[0])
        elif count > 1:
            print("Found more than 1 match, try again")
            return 1
        elif count != 1:
            print("No matches found")
            return 1
            

    def __del__(self):
        return 0
