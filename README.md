# jira-telegram-bot
Telegram-bot interface for JIRA <br />
![Alt Text](https://github.com/ruslan337/jira-telegram-bot/blob/master/20180518_121727.gif)
# Dependencies:
* Python library for Telegram Bot API - https://github.com/python-telegram-bot/python-telegram-bot <br />
* Python library to work with JIRA APIs - https://jira.readthedocs.io/en/master/ <br />

<b>You can install all dependencies running:</b><br />
* pip3 install python-telegram-bot <br />
* pip3 install jira
# How to use
1) Clone this project, install dependencies
2) Copy file config_template.py to config.py, edit config.py
3) Edit jira-bot.service, copy it to /etc/systemd/system/
4) run systemctl daemon-reload, systemctl start jira-bot
# ToDo list:
* include logger
* enable edit for created tasks
* imrove english
* priview and comments for task
* notificattions about tasks
