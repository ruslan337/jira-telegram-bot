#!/bin/python3

# Written by Ruslan Murzalin (rus_m_ok@mail.ru)

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# DEPENDENCIES:

# Python library for Telegram Bot API - https://github.com/python-telegram-bot/python-telegram-bot
# Python library to work with JIRA APIs - https://jira.readthedocs.io/en/master/

# You can install all dependencies running:
# pip3 install python-telegram-bot
# pip3 install jira

from config import *
from languages import *
from telegram.ext import Updater, CommandHandler, Job, CallbackQueryHandler, RegexHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, File, InputFile
from datetime import datetime, time, timedelta
import urllib, re, os, logging
from random import randint
from jira import JIRA
from copy import deepcopy
from init import init_dirs
from models import User

jira=JIRA(server=jiraserver, basic_auth=(jirauser, jirapass))

def show_list(bot, update):
    global jira
    issue_list=jira.search_issues(jsq="status = 'To Do'")
    for issue in issue_list:
        try:
            f=open(jira_notifier_db_dir+str(issue.id), 'r')
            resolution=f.read()
            f.close()
            if (issue.raw['fields']['resolution'] is None and resolution=='None') or \
              (issue.raw['fields']['resolution'] is not None and issue.raw['fields']['resolution']['name'] == resolution):
                pass
            else:
                pass
        except FileNotFound as e:
            pass
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode="HTML")

def show_help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=message, parse_mode="HTML")

def start(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action='typing')
    sender=str(update.message.from_user.id)
    users[sender].reset()
    lang=users[sender].language
    keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[lang].values()]], resize_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text=hello_message[lang], reply_markup=keys)
    #keys=InlineKeyboardMarkup([[InlineKeyboardButton(comm, callback_data=comm) for comm in init_commands[lang].values()]])
    #bot.sendMessage(chat_id=update.message.chat_id, text=hello_message[lang], reply_markup=keys)

def inline_update(bot, update):
    sender=users[str(update.callback_query.from_user.id)]
    (action,task_id,new_data)=update.callback_query.data.split('__')
    message_id=update.callback_query.message.message_id
    lang=sender.language
    if task_id==sender.task.task_id:
        if action=='user_change': sender.task.inline_user_change(update, user=users[new_data])
        elif action=='priority_change': sender.task.inline_priority_change(update, priority=new_data)
        elif action=='deadline_change': sender.task.inline_deadline_change(update, deadline=new_data)
        elif action=='project_change': sender.task.inline_project_change(update, project=new_data)
        else:
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=error_message[lang])
    else:
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=task_was_created_error[lang])

def file_upload(bot, update):
    sender=users[str(update.message.from_user.id)]
    lang=sender.language
    if sender.task.task_id!=None:
        if update.message.voice!=None:
            f=update.message.voice.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            sender.task.file.append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        elif update.message.document!=None:
            f=update.message.document.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            sender.task.file.append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        elif update.message.video!=None:
            f=update.message.video.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            sender.task.file.append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        elif update.message.photo!=None:
            photo=update.message.photo.pop()
            f=photo.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            sender.task.file.append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=file_type_error[lang])
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=no_task_error[lang])

def task_router(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action='typing')
    text=update.message.text
    sender=str(update.message.from_user.id)
    if sender in users:
        sender=users[sender]
        lang=sender.language
        task=sender.task
        if sender.createtask:
            if text==cancel_key[lang]:
                start(bot, update)
            elif text==task_commands[lang]['summary']: 
                sender.ask_for_summary(update)
            elif text==task_commands[lang]['priority']: 
                sender.ask_for_priority(update)
            elif text==task_commands[lang]['deadline']: 
                sender.ask_for_deadline(update)
            elif text==task_commands[lang]['project']: 
                sender.ask_project(update)
            elif text==send_task_key[lang]: 
                sender.create_task(update, jira)
            elif sender.task_assignee_set and (text.encode() in jira_users): 
                sender.task.set_assignee(update=update, assignee=users[jira_users[text.encode()]])
            elif sender.task_priority_set and (text in priority_list[lang]):
                sender.task.set_priority(update=update, priority=text)
            elif sender.task_project_set: 
                sender.task.set_project(update=update, project=text)
            elif sender.task_deadline_set:
                sender.task.set_deadline(update=update, deadline=text)
            elif sender.task_summary_set: 
                sender.task.set_summary(update=update, summary=text)
            elif sender.task.task_to is not None: 
                sender.task.set_task_text(update=update, text=text)
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text=error_message[lang], reply_markup=keys)
        else:
            if text.encode(encoding='utf_8', errors='strict')==cancel_key[lang].encode(encoding='utf_8', errors='strict'):start(bot, update)
            elif text==init_commands[lang]['list']: list_tasks(bot, update)
            elif text==init_commands[lang]['task']: sender.init_task(bot, update)
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text=error_message[lang], reply_markup=keys)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=no_authorization_message[lang])


init_dirs()
#logging.basicConfig(filename=log_dir+'main.log', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logging.info("Starting the service")
updater=Updater(token=token)
dispatcher=updater.dispatcher

jira_users={}
users={}
for user in user_list:
    if user_list[user]['jirauser']!=None and user_list[user]['isAssignee']:
        jira_users[user_list[user]['name'].encode()]=user

projects={}
jp=jira.projects()
for project in jp:
    if project.key in jira_projects:projects[project.raw['name']]=project.key

for user in user_list:
    users[user]=User.User(user_id=user,\
                     name=user_list[user]['name'],\
                     default_project=user_list[user]['project'],\
                     jira_users=jira_users,\
                     project_list=projects,\
                     jirauser=user_list[user]['jirauser'],\
                     username=user_list[user]['username'],\
                     isAssignee=user_list[user]['isAssignee'],\
                     language=user_list[user]['language'],\
                     priority=user_list[user]['priority'])

logging.debug("Users were initialized!")
start_handler=CommandHandler('start', start)
list_handler=CommandHandler('list', show_list)
help_handler=CommandHandler('help', show_help)
task_CRUD_handler=RegexHandler(r'.*', task_router)
inline_handler=CallbackQueryHandler(inline_update)
document_handler=MessageHandler(Filters.document, file_upload)
photo_handler=MessageHandler(Filters.photo, file_upload)
voice_handler=MessageHandler(Filters.voice, file_upload)

dispatcher.add_handler(document_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(voice_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(task_CRUD_handler)
dispatcher.add_handler(inline_handler)

updater.start_polling()
