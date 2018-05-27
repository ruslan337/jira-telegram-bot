# -*- coding: utf-8 -*-
init_commands = { 'ru':{'task':u'Создать', 'list':u'Текущие задачи'},\
                  'en':{'task':'Create', 'list':'List'},}
task_commands = { 'ru':{'deadline':u'Срок', 'summary':u'Тема', 'priority':u'Приоритет', 'project':u'Тип'},\
                  'en':{'deadline':'Deadline', 'summary':'Summary', 'priority':'Priority', 'project':'Project'},}
task_create_message = { 'ru':u'Опишите вашу проблему. Опционально, вы можете прикрепить файлы, указать тему задачи(краткое пояснение), \
желаемый срок исполнения, тип задачи и важность задачи',\
                        'en':'Describe your task. Optional, you can attach files, set the summary, deadline and priority.'}
task_is_ready_message = {'ru':u'Задача готова к отправке, нажмите "Отправить", для отправки задачи. \
Предварительно, вы можете указать заголовок, срок, тип и важность задачи.',\
                         'en':'Task is ready to be assigned, press "Send", when you are ready.\
Preliminarily, you can set the summary(topic), deadline, priority and project.'}
task_assignee_message = { 'ru':u'Кому вы хотите назначить задачу?',\
                          'en':'Who is going to be an assignee?'}
file_accepted_message = { 'ru':u'Файл будет добавлен к задаче.',\
                          'en':'File is going to be attached to the task.'}
file_type_error = { 'ru':u'Неизвестный тип файла.',\
                          'en':'Unknown filetype.'}
inline_assignee_message = { 'ru':u'Вы назначаете задачу пользователю {0}',\
                            'en':'You are assigning task to the user {0}' }
no_task_error = {'ru':u'Чтобы прикрепить к задаче файл, нажмете "Создать", а потом отправляйте файл.',
                 'en':'If you want to attach the file to a task, You have to press "Create" first.'}
task_summary_message = { 'ru':u'Вкратце опишите вашу проблему.',\
                         'en':'Give a short summary to your task.'}
summary_was_set_message = {'ru':u'Вы указали тему (описание) вашей задачи. Если вы хотите поменять его, повторно нажмите на кнопку "Тема"',\
                           'en':'You set the topic (summary) of your task. If you want to change it, please press "Summary" button again.'}
task_deadline_message = {'ru':u'Укажите желаемый срок выполнения задачи в днях',\
                         'en':'Set the deadline for this task in days'}
deadline_was_set_message = {'ru':u'Срок исполения задачи: {0} дней',\
                            'en':'The deadline of the task is: {0} days'}
priority_list = { 'ru': {u'Низкий':'Low',u'Средний':'Medium',u'Высокий':'High'},
                  'en': {'Low':'Low', 'Medium':'Medium', 'High':'High'} }
task_priority_message = {'ru':u'Выбирете приоритет задачи',\
                        'en':'Choose the the priority for the task'}
priority_was_set_message = {'ru':u'Задача будет создана с приоритетом: {0}',\
                           'en':'The task is going to be created with {0} priority'}
task_project_message = {'ru':u'Выбирете тип задачи',\
                        'en':'Chose the project for the task'}
project_was_set_message = {'ru':u'Вы выбрали тип задачи: {0}',\
                           'en':'The project is: {0}'}
project_error_message = {'ru':u'Вы выбрали некорректный тип задачи. Выберите тип из списка.',\
                         'en':'Incorrect project!! Chose the project from the list.'}
update_is_ok_message = {'ru':u'Изменения сохранены',\
                        'en':'Updates are saved'}
no_text_message = {'ru':u'Вы не описали вашу задачу. Пожалуйста, отправьте мне(Боту) суть вашей проблемы и нажмите "-ОТПРАВИТЬ-"',\
                   'en':'You did not discrebed your task. Please, send to me (to Bot) description of your problem and press "-SEND-"'}
error_message = { 'ru':u'что-то пошло не так! Убидитесь, что все данные введены в правильном формате и попробуйте повторить операцию.',\
                  'en':'something is wrong! Ensure, all data was sent correctly and try angain.'}
hello_message = { 'ru':u'Чем обязаны?',\
                  'en':'How can I help you?'}
task_was_created_error = { 'ru':u'Не возможно редактировать задачи после создания.', \
                           'en':u'Your are not allowed to edit tasks, as it was already sent to Assigne.' }
no_authorization_message = { 'ru':u'У вас недостаточно привилегий для данной операции. Обратитесь к администратору системы.',\
                             'en':'You are not allowed to perform this type of operations. Ask it to the system administrator.'}
task_was_created_message = { 'ru':u'Задача {0} отправлена пользователю {1}',\
                             'en':'Task {0} was sent to the user {1}' }
jirauser_assignee_list = { 'ru':u'Задачи назначенные на пользователя {0} ', \
                            'en':'Tasks to the user {0}' }
jirauser_author_list = { 'ru':u'Задачи от пользователя {0} ', \
                            'en':'Tasks from the user {0}' }

cancel_key = {'ru':u'-ОТМЕНА-',\
              'en':'-CANCEL-'}
send_task_key = {'ru':u'-ОТПРАВИТЬ-',\
                 'en':'-SEND-'}