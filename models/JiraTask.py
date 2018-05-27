from datetime import datetime, time, timedelta
from random import randint
from languages import *
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, File, InputFile

class JiraTask:
    def __init__(self, bot, author, lang, project_list, defaul_project, jira_users, default_priority="Medium"):
        self.bot=bot
        self.lang=lang
        self.jira_users=jira_users
        self.author=author
        self.project=defaul_project
        self.project_list=project_list
        self.priority=default_priority
        self.summary=None
        self.task_to=None
        self.task_text=None
        self.deadline=None
        self.file=[]
        self.task_id=self.author.user_id+str(datetime.now()).replace(' ','_').replace(':','').replace('.','')+str(randint(10000,99999))

    def set_priority(self, update, priority):
        self.priority=priority
        self.author.task_priority_set=False
        keys=InlineKeyboardMarkup([[InlineKeyboardButton(priority, callback_data='priority_change__'+self.task_id+\
                                    '__'+priority_list[self.lang][priority]) for priority in priority_list[self.lang]]])
        self.bot.sendMessage(chat_id=update.message.chat_id, text=priority_was_set_message[self.lang].format(\
                        self.priority), reply_markup=keys)
        keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.lang].values()],[cancel_key[self.lang],send_task_key[self.lang]]], resize_keyboard=True)
        if self.task_text == None:
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[self.lang], reply_markup=keys)
        else:
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[self.lang], reply_markup=keys)
    
    def set_project(self, update, project):
        if project in self.project_list:
            self.author.task_project_set=False
            self.project=self.project_list[project]
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(project, callback_data='project_change__'+
                                    self.task_id+'__'+self.project_list[project]) for project in self.project_list]])
            self.bot.sendMessage(chat_id=update.message.chat_id, text=project_was_set_message[self.lang].format(project), reply_markup=keys)
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.lang].values()],[cancel_key[self.lang],send_task_key[self.lang]]], resize_keyboard=True)
            if self.task_text == None:
                self.bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[self.lang], reply_markup=keys)
            else:
                self.bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[self.lang], reply_markup=keys)
        else:
            self.author.task_project_set=True
            keys=ReplyKeyboardMarkup(keyboard=[[project for project in self.project_list.values()]], resize_keyboard=True)
            self.bot.sendMessage(chat_id=update.message.chat_id, text=project_error_message[self.lang], reply_markup=keys)
    
    def set_deadline(self, update, deadline):
        if deadline.isnumeric():
            self.deadline=int(deadline)
            self.author.task_deadline_set=False
            keyboard=['1','2','3','4','5','10']
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(key, callback_data='deadline_change__'+self.task_id+
                                        '__'+key) for key in keyboard]])
            self.bot.sendMessage(chat_id=update.message.chat_id, text=deadline_was_set_message[self.lang].format(deadline), reply_markup=keys)
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.lang].values()],[cancel_key[self.lang],send_task_key[self.lang]]], resize_keyboard=True)
            if self.task_text == None:
                self.bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[self.lang], reply_markup=keys)
            else:
                self.bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[self.lang], reply_markup=keys)
        else:
            keys=InlineKeyboardMarkup(keyboard=[['1','2','3','4','5','10']],resize_keyboard=True)
            self.author.task_deadline_set=True
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_deadline_message[self.lang], reply_markup=keys)
    
    def set_summary(self, update, summary):
        self.summary=summary
        self.author.task_summary_set=False
        keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.lang].values()],[cancel_key[self.lang],send_task_key[self.lang]]], resize_keyboard=True)
        self.bot.sendMessage(chat_id=update.message.chat_id, text=summary_was_set_message[self.lang], reply_markup=keys)
        if self.task_text is None:
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[self.lang], reply_markup=keys)
        else:
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[self.lang], reply_markup=keys)
    
    def set_task_text(self, update, text):
        if self.task_text is None:self.task_text=''
        self.task_text+=text+'\n'
        keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.lang].values()],[cancel_key[self.lang],send_task_key[self.lang]]], resize_keyboard=True)
        self.bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[self.lang], reply_markup=keys)
    
    def set_assignee(self, update, assignee):
        print(assignee.name)
        self.task_to=assignee
        self.author.task_assignee_set=False
        keys=InlineKeyboardMarkup([[InlineKeyboardButton(name.decode(), callback_data='user_change__'+self.task_id+\
                                    '__'+self.jira_users[name]) for name in self.jira_users]])
        print(keys.to_dict())
        self.bot.sendMessage(chat_id=update.message.chat_id, text=inline_assignee_message[self.lang].format(\
                        assignee.name), reply_markup=keys)
        keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[self.lang].values()],[cancel_key[self.lang],\
                                 send_task_key[self.lang]]], resize_keyboard=True)
        if self.task_text == None:
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[self.lang], reply_markup=keys)
        else:
            self.bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[self.lang], reply_markup=keys)

    def inline_user_change(self, update, user):
        message_id=update.callback_query.message.message_id
        self.task_to=user
        keys=InlineKeyboardMarkup([[InlineKeyboardButton(name.decode(), callback_data='user_change__'+self.task_id+\
                                    '__'+self.jira_users[name]) for name in self.jira_users]])
        self.bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
            text=inline_assignee_message[self.lang].format(user.name), reply_markup=keys)
        self.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[self.lang])
    
    def inline_priority_change(self, update, priority):
        message_id=update.callback_query.message.message_id
        self.priority=priority
        for pr in priority_list[self.lang]:
            if priority_list[self.lang][pr]==priority:new_priority=pr
        keys=InlineKeyboardMarkup([[InlineKeyboardButton(priority, callback_data='priority_change__'+self.task_id+\
                                    '__'+priority_list[self.lang][priority]) for priority in priority_list[self.lang]]])
        self.bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                            text=priority_was_set_message[self.lang].format(new_priority), reply_markup=keys)
        self.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[self.lang])
        
    def inline_deadline_change(self, update, deadline):
        message_id=update.callback_query.message.message_id
        self.deadline=deadline
        keyboard=['1','2','3','4','5','10']
        keys=InlineKeyboardMarkup([[InlineKeyboardButton(key, callback_data='deadline_change__'+self.task_id+
                                    '__'+key) for key in keyboard]])
        self.bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                        text=deadline_was_set_message[self.lang].format(deadline), reply_markup=keys)
        self.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[self.lang])
        
    def inline_project_change(self, update, project):
        message_id=update.callback_query.message.message_id
        self.project=project
        keys=InlineKeyboardMarkup([[InlineKeyboardButton(project, callback_data='project_change__'+
                                    self.task_id+'__'+self.project_list[project]) for project in self.project_list]])
        for pr in self.project_list:
            if self.project_list[pr]==project:project=pr
        self.bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                        text=project_was_set_message[self.lang].format(project), reply_markup=keys)
        self.bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[self.lang])
    
