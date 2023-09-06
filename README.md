This is a Graph API + Exov2 integration. This is the user interface portion. Eventually, it will pull ticket information from Connectwise for automation purposes. 

It requires list.txt, each line of which should look like this

Domain_name|Client_secret|Application_Id|Tenant_id|Object_ID|Certificate_thumbprint|0

2 App registrations are needed in Azure. One for graph, and one for the powershell module. The powershell one needs to be setup with a certificate and be given Exchange.ManageAsApp permission. The Graph app needs the following permissions

![image](https://github.com/niartemev/365Integration/assets/118090664/5f39c757-8bef-4933-a645-2793512eac5c)



![image](https://github.com/niartemev/365Integration/assets/118090664/0fb15dd1-49db-4aa4-b602-4aa2aa80ff0d)
