# jira-telegram-bot
Telegram-bot interface for JIRA
# DEPENDENCIES:
Python library for Telegram Bot API - https://github.com/python-telegram-bot/python-telegram-bot
Python library to work with JIRA APIs - https://jira.readthedocs.io/en/master/
You can install all dependencies running:
 pip3 install python-telegram-bot
 pip3 install jira
#How to use
1)Clone this project, install dependencies
2)Copy file config_template.py to config.py, edit config.py
3)Edit jira-bot.service, copy it to /etc/systemd/system/
4)run systemctl daemon-reload, systemctl start jira-bot
#ToDo list:
* include logger
* enable edit for created tasks
* include english