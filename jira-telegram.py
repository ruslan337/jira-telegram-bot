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
import urllib, re, os
from random import randint
from jira import JIRA
from copy import deepcopy
from config import users as clean_users

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
    global users
    global clean_users
    sender=str(update.message.from_user.id)
    users[sender]=deepcopy(clean_users[sender])
    lang=users[sender]['language']
    keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[lang].values()]], resize_keyboard=True)
    bot.sendMessage(chat_id=update.message.chat_id, text=hello_message[lang], reply_markup=keys)
    #keys=InlineKeyboardMarkup([[InlineKeyboardButton(comm, callback_data=comm) for comm in init_commands[lang].values()]])
    #bot.sendMessage(chat_id=update.message.chat_id, text=hello_message[lang], reply_markup=keys)

def task_create(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action='typing')
    text=update.message.text
    global jira_users, jira, projects
    sender=str(update.message.from_user.id)
    if sender in users:
        lang=users[sender]['language']
        if text==cancel_key[lang]:start(bot, update)
        elif text==init_commands[lang]['list']:
            answer=''
            if users[sender]['jirauser'] is not None:
                answer+='<b>'+jirauser_assignee_list[lang].format(users[sender]['name'])+':</b>\n'
                issues=jira.search_issues('assignee={0} and status!=Done'.format(users[sender]['jirauser']))
                for issue in issues:answer+='• <a href="'+jiraserver+'/browse/'+issue.key+'">'+\
                str(issue.key)+'</a> (<i>'+issue.raw['fields']['status']['name']+'</i>) '+issue.raw['fields']['summary']+'\n'
                answer+='\n<b>'+jirauser_author_list[lang].format(users[sender]['name'])+':</b>\n'
                issues=jira.search_issues('reporter={0} and status!=Done'.format(users[sender]['jirauser']))
                for issue in issues:answer+='• <a href="'+jiraserver+'/browse/'+issue.key+'">'+\
                str(issue.key)+'</a> (<i>'+issue.raw['fields']['status']['name']+'</i>) '+issue.raw['fields']['summary']+'\n'
                bot.sendMessage(chat_id=update.message.chat_id, text=answer, parse_mode='HTML')
                keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[lang].values()]], resize_keyboard=True)
                bot.sendMessage(chat_id=update.message.chat_id, text=hello_message[lang], reply_markup=keys)
        elif text==init_commands[lang]['task']:
            users[sender]['task_id']=sender+str(datetime.now()).replace(' ','_').replace(':','').replace('.','')+str(randint(10000,99999))
            users[sender]['createtask']=True
            keys=ReplyKeyboardMarkup(keyboard=[[name for name in jira_users],[cancel_key[lang]]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=task_assignee_message[lang], reply_markup=keys)
        elif text in jira_users and users[sender]['createtask']:
            users[sender]['task_to']=jira_users[text]
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(name, callback_data='user_change__'+users[sender]['task_id']+\
                                        '__'+jira_users[name]) for name in jira_users]])
            bot.sendMessage(chat_id=update.message.chat_id, text=inline_assignee_message[lang].format(\
                            users[users[sender]['task_to']]['name']), reply_markup=keys)
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],\
                                     send_task_key[lang]]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[lang], reply_markup=keys)
        elif text == task_commands[lang]['summary'] and users[sender]['createtask']:
            users[sender]['set_summary']=True
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],send_task_key[lang]]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=task_summary_message[lang], reply_markup=keys)
        elif text==task_commands[lang]['priority'] and users[sender]['createtask']:
            keys=ReplyKeyboardMarkup(keyboard=[[priority for priority in priority_list[lang]],[cancel_key[lang]]],resize_keyboard=True)
            users[sender]['set_priority']=True
            bot.sendMessage(chat_id=update.message.chat_id, text=task_priority_message[lang], reply_markup=keys)
        elif text==task_commands[lang]['deadline'] and users[sender]['createtask']:
            keys=ReplyKeyboardMarkup(keyboard=[['1','2','3','4','5','10']],resize_keyboard=True)
            users[sender]['set_deadline']=True
            bot.sendMessage(chat_id=update.message.chat_id, text=task_deadline_message[lang], reply_markup=keys)
        elif text==task_commands[lang]['project'] and users[sender]['createtask']:
            users[sender]['set_project']=True
            keys=ReplyKeyboardMarkup(keyboard=[[project for project in projects]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=task_deadline_message[lang], reply_markup=keys)
        elif text==send_task_key[lang] and users[sender]['createtask']:
            if users[sender]['task_text'] is not None and users[sender]['task_to'] is not None:
                if users[sender]['summary'] is None:
                    users[sender]['summary']=users[sender]['name']+': '+" ".join(users[sender]['task_text'].split()[:5])
                jf={'project':users[sender]['project'], \
                    'summary':users[sender]['summary'], \
                    'description':users[sender]['task_text'], \
                    'issuetype':{'name':'Task'}, \
                    'assignee':{'name':users[users[sender]['task_to']]['jirauser']}, \
                    'priority':{'name':users[sender]['priority']}\
                }
                if users[sender]['deadline'] is not None:
                    jf['duedate']=str((datetime.now()+timedelta(days=int(users[sender]['deadline']))).date())
                issue=jira.create_issue(jf)
                for filename in users[sender]['file']:
                    jira.add_attachment(issue=issue, attachment=filename)
                f=open(db_dir+users[sender]['task_id'],'w')
                f.write(issue.id)
                f.close()
                keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[lang].values()]], resize_keyboard=True)
                bot.sendMessage(chat_id=update.message.chat_id, text=task_was_created_message[lang].format(issue.key,\
                                users[users[sender]['task_to']]['name']), reply_markup=keys)
                users[sender]=deepcopy(clean_users[sender])
            else:
                keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in init_commands[lang].values()]], resize_keyboard=True)
                bot.sendMessage(chat_id=update.message.chat_id, text=no_text_message[lang].format(issue.key, users[users[sender]['task_to']]['name']), reply_markup=keys)
        elif users[sender]['set_priority'] and users[sender]['createtask'] and (text in priority_list[lang]):
            users[sender]['priority']=text
            users[sender]['set_priority']=False
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(priority, callback_data='priority_change__'+users[sender]['task_id']+\
                                        '__'+priority_list[lang][priority]) for priority in priority_list[lang]]])
            bot.sendMessage(chat_id=update.message.chat_id, text=priority_was_set_message[lang].format(\
                            users[sender]['priority']), reply_markup=keys)
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],send_task_key[lang]]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[lang], reply_markup=keys)
        elif users[sender]['set_project'] and users[sender]['createtask']:
            if text in projects:
                users[sender]['project']=projects[text]
                users[sender]['set_project']=False
                keys=InlineKeyboardMarkup([[InlineKeyboardButton(project, callback_data='project_change__'+
                                        users[sender]['task_id']+'__'+projects[project]) for project in projects]])
                bot.sendMessage(chat_id=update.message.chat_id, text=project_was_set_message[lang].format(text), reply_markup=keys)
                keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],send_task_key[lang]]], resize_keyboard=True)
                bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[lang], reply_markup=keys)
            else:
                users[sender]['set_project']=True
                keys=ReplyKeyboardMarkup(keyboard=[[project for project in projects.values()]], resize_keyboard=True)
                bot.sendMessage(chat_id=update.message.chat_id, text=project_error_message[lang], reply_markup=keys)
        elif users[sender]['set_deadline'] and users[sender]['createtask']:
            if text.isnumeric():
                users[sender]['set_deadline']=False
                users[sender]['deadline']=int(text)
                keyboard=['1','2','3','4','5','10']
                keys=InlineKeyboardMarkup([[InlineKeyboardButton(key, callback_data='deadline_change__'+users[sender]['task_id']+
                                            '__'+key) for key in keyboard]])
                bot.sendMessage(chat_id=update.message.chat_id, text=deadline_was_set_message[lang].format(text), reply_markup=keys)
                keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],send_task_key[lang]]], resize_keyboard=True)
                bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[lang], reply_markup=keys)
            else:
                keys=InlineReplyKeyboardMarkup(keyboard=[['1','2','3','4','5','10']],resize_keyboard=True)
                users[sender]['set_deadline']=True
                bot.sendMessage(chat_id=update.message.chat_id, text=task_deadline_message[lang], reply_markup=keys)
        elif users[sender]['set_summary'] and users[sender]['createtask']:
            users[sender]['summary']=text
            users[sender]['set_summary']=False
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],send_task_key[lang]]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=summary_was_set_message[lang], reply_markup=keys)
            if users[sender]['task_text'] is None:
                bot.sendMessage(chat_id=update.message.chat_id, text=task_create_message[lang], reply_markup=keys)
        elif users[sender]['createtask'] and users[sender]['task_to'] is not None:
            if users[sender]['task_text'] is None:users[sender]['task_text']=''
            users[sender]['task_text']+=text+'\n'
            keys=ReplyKeyboardMarkup(keyboard=[[comm for comm in task_commands[lang].values()],[cancel_key[lang],send_task_key[lang]]], resize_keyboard=True)
            bot.sendMessage(chat_id=update.message.chat_id, text=task_is_ready_message[lang], reply_markup=keys)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=error_message[lang].format(issue.key, users[users[sender]['task_to']]['name']), reply_markup=keys)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=no_authorization_message[lang])

def inline_update(bot, update):
    global users
    sender=str(update.callback_query.from_user.id)
    (action,task_id,new_data)=update.callback_query.data.split('__')
    message_id=update.callback_query.message.message_id
    lang=users[sender]['language']
    if task_id==users[sender]['task_id']:
        if action=='user_change':
            users[sender]['task_to']=new_data
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(name, callback_data='user_change__'+task_id+\
                                        '__'+jira_users[name]) for name in jira_users]])
            bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                text=inline_assignee_message[lang].format(users[new_data]['name']), reply_markup=keys)
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[lang])
        elif action=='priority_change':
            users[sender]['priority']=new_data
            for pr in priority_list[lang]:
                if priority_list[lang][pr]==new_data:new_priority=pr
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(priority, callback_data='priority_change__'+users[sender]['task_id']+\
                                        '__'+priority_list[lang][priority]) for priority in priority_list[lang]]])
            bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                                text=priority_was_set_message[lang].format(new_priority), reply_markup=keys)
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[lang])
        elif action=='deadline_change':
            users[sender]['deadline']=new_data
            keyboard=['1','2','3','4','5','10']
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(key, callback_data='deadline_change__'+users[sender]['task_id']+
                                        '__'+key) for key in keyboard]])
            bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                            text=deadline_was_set_message[lang].format(new_data), reply_markup=keys)
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[lang])
        elif action=='project_change':
            users[sender]['project']=new_data
            keys=InlineKeyboardMarkup([[InlineKeyboardButton(project, callback_data='project_change__'+
                                        users[sender]['task_id']+'__'+projects[project]) for project in projects]])
            project=new_data
            for pr in projects:
                if projects[pr]==new_data:project=pr
            bot.editMessageText(chat_id=update.callback_query.message.chat.id, message_id=message_id, \
                            text=project_was_set_message[lang].format(project), reply_markup=keys)
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update_is_ok_message[lang])
        else:
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=error_message[lang])
    else:
        bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=task_was_created_error[lang])

def file_upload(bot, update):
    global users
    sender=str(update.message.from_user.id)
    lang=users[sender]['language']
    if users[sender]['task_id']!=None:
        if update.message.voice!=None:
            f=update.message.voice.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            users[sender]['file'].append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        elif update.message.document!=None:
            f=update.message.document.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            users[sender]['file'].append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        elif update.message.video!=None:
            f=update.message.video.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            users[sender]['file'].append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        elif update.message.photo!=None:
            photo=update.message.photo.pop()
            f=photo.get_file()
            filename=f.download(custom_path=attach_dir+f.file_path.split('/').pop())
            users[sender]['file'].append(filename)
            bot.sendMessage(chat_id=update.message.chat_id, text=file_accepted_message[lang])
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text=file_type_error[lang])
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=no_task_error[lang])

updater=Updater(token=token)
dispatcher=updater.dispatcher

try:
    os.mkdir(db_dir)
except:
    pass
try:
    os.mkdir(attach_dir)
except:
    pass

jira_users={}
for user in users:
    if users[user]['jirauser']!=None and users[user]['isAssignee']:jira_users[users[user]['name']]=user
for user in clean_users:
    clean_users[user]['set_summary']=False
    clean_users[user]['summary']=None
    clean_users[user]['set_priority']=False
    clean_users[user]['task_to']=None
    clean_users[user]['createtask']=False
    clean_users[user]['set_deadline']=False
    clean_users[user]['deadline']=None
    clean_users[user]['set_project']=False
    clean_users[user]['send_task']=False
    clean_users[user]['task_id']=None
    clean_users[user]['task_text']=None
    clean_users[user]['file']=[]
users=deepcopy(clean_users)

projects={}
jp=jira.projects()
for project in jp:
    if project.key in jira_projects:projects[project.raw['name']]=project.key

start_handler=CommandHandler('start', start)
list_handler=CommandHandler('list', show_list)
help_handler=CommandHandler('help', show_help)
task_create_handler=RegexHandler(r'.*', task_create)
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
dispatcher.add_handler(task_create_handler)
dispatcher.add_handler(inline_handler)

updater.start_polling()
