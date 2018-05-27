from datetime import datetime, time, timedelta
from models import JiraTask
from random import randint
from languages import *
from config import db_dir
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, File, InputFile
import logging

class User:
    def __init__(self, user_id, name, default_project, jira_users, project_list, jirauser, username=None, isAssignee=True, language='en', priority='Medium'):
        self.user_id=user_id
        self.name=name
        self.project=default_project
        self.jira_users=jira_users
        self.project_list=project_list
        self.jirauser=jirauser
        self.username=username
        self.isAssignee=isAssignee
        self.language=language
        self.priority=priority
        self.reset()

    def init_task(self, bot, update):
        self.bot=bot
        self.task=JiraTask.JiraTask(defaul_project=self.project, default_priority=self.priority,bot=bot, author=self, lang=self.language, project_list=self.project_list, jira_users=self.jira_users)
        self.createtask=True
        self.task_assignee_set=True
        keys=ReplyKeyboardMarkup(keyboard=[[name.decode() for name in self.jira_users],[cancel_key[self.language]]], resize_keyboard=True)
        self.bot.sendMessage(chat_id=update.message.chat_id, text=task_assignee_message[self.language], reply_markup=keys)
        
    def ask_for_summary(self, update):
        self.task_summary_set=True
        keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.language].values()],\
                        [cancel_key[self.language],send_task_key[self.language]]], resize_keyboard=True)
        self.bot.sendMessage(chat_id=update.message.chat_id, text=task_summary_message[self.language], reply_markup=keys)
    
    def ask_for_deadline(self, update):
        keys=ReplyKeyboardMarkup(keyboard=[['1','2','3','4','5','10']],resize_keyboard=True)
        self.task_deadline_set=True
        self.bot.sendMessage(chat_id=update.message.chat_id, text=task_deadline_message[self.language], reply_markup=keys)
    
    def ask_for_priority(self, update):
        keys=ReplyKeyboardMarkup(keyboard=[[priority for priority in priority_list[self.language]],[cancel_key[self.language]]],resize_keyboard=True)
        self.task_priority_set=True
        self.bot.sendMessage(chat_id=update.message.chat_id, text=task_priority_message[self.language], reply_markup=keys)
    
    def ask_project(self, update):
        self.task_project_set=True
        keys=ReplyKeyboardMarkup(keyboard=[[project for project in self.project_list]], resize_keyboard=True)
        self.bot.sendMessage(chat_id=update.message.chat_id, text=task_deadline_message[self.language], reply_markup=keys)

    def create_task(self, update, jira):
        logging.debug("User.create_task: {0}, {1}, {2}".format(self.task.project, self.task.summary, self.task.task_text))
        if self.task.task_text is not None and self.task.task_to is not None:
            if self.task.summary is None:
                self.task.summary=self.name+': '+" ".join(self.task.task_text.split()[:5])
            jf={'project':self.task.project, \
                'summary':self.task.summary, \
                'description':self.task.task_text, \
                'issuetype':{'name':'Task'}, \
                'assignee':{'name':self.task.task_to.jirauser}, \
                'priority':{'name':self.task.priority}\
            }
            if self.task.deadline is not None:
                jf['duedate']=str((datetime.now()+timedelta(days=int(self.task.deadline))).date())
            logging.debug("User.create_task: {0}, {1}, {2}".format(self.task.project, self.task.summary, self.task.task_text))
            issue=jira.create_issue(jf)
            for filename in self.task.file:
                jira.add_attachment(issue=issue, attachment=filename)
            f=open(db_dir+self.task.task_id,'w')
            f.write(issue.id)
            f.close()
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[self.language].values()]], resize_keyboard=True)
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_was_created_message[self.language].format(issue.key,\
                            self.task.task_to.name), reply_markup=keys)
            self.reset()
        else:
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[self.language].values()]], resize_keyboard=True)
            self.bot.sendMessage(chat_id=update.message.chat_id, text=no_text_message[self.language], reply_markup=keys)
        
    def reset(self):
        self.summary=None
        self.task_summary_set=False
        self.task_priority_set=False
        self.task_deadline_set=False
        self.task_project_set=False
        self.task_assignee_set=False
        self.createtask=False
        self.send_task=False
        self.task=None
        self.bot=None