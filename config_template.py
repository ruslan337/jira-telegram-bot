#!/bin/python3

token='123456789:ABCDE1234567890ABCDE1234567890ABCDE' # Telegram Bot token
jiraserver='https://yourcompanyname.atlassian.net' 
jirauser='jiraUser'
jirapass='jiraUserPassword'
db_dir='/var/local/jira_notifier/' # The app will create some files here, be sure that this app UID has such permessions.
attach_dir=db_dir+'attach/' # Attach files are going to be stored here.
jira_projects=['PROJ1','PROJ2'] # The codes of jour jira projects, that are going to be used by this app.
# Format for users list, who is going to use this app, or who is going to be assignee for the tasks from this bot
# users={ 'user_telegram_chat_id' : {
#			'name':'Birth name or some alias name of user', 
#			'username':'Telegram username. None value is allowed',
#			'project':'Default jira project code for task created by this user. NOT TO THIS USER',
#			'jirauser':'Jira Username',
#			'isAssignee':'All users are allowed to assign the task to this user from this app',
#			'language':'Bot interface language',
#			'priority':'Default priority for tasks created by this user'},
#	 'next_chat_id' : {...},
# }
# See example above
users={ \
     '11111111' : { 'name':'Martian', 'username':'martian337', 'project':'TST',\
                    'jirauser':'admin', 'isAssignee':True, 'language':'ru', 'priority':'Medium'},\
     '22222222' : { 'name':'Fatboy', 'username':None, 'project':'ABC',\
                     'jirauser':'fat.boy', 'isAssignee':True, 'language':'ru', 'priority':'High'},\
     '33333333' : { 'name':'Anthony', 'username':'A_USER', 'project':'ABC',\
                     'jirauser':'anthony.hopkins', 'isAssignee':True, 'language':'ru', 'priority':'Medium'},
}