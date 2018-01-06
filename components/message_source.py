from config.state_config import Language



message_source = {
    Language.ENG: {
        'error': ':pensive: I\'m really sorry, but there were an error :(',

        'date.hr': ' in *{} hr.*',
        'date.hrs': ' in *{} hrs.*',
        'date.min': ' in *{} min.*',
        'date.same': ' *at the same time*!',

        'task.upcoming': 'Upcoming',
        'task.completed': 'Completed',
        'task.muted': '(:no_bell: Muted)',

        'project.not_selected': ':question: Not selected',

        'filter.unknown': ':confused: Sorry, I could not get your command :(',

        'state.start_state.welcome': 'welcome to task tracking service!*\n'
                                     '\n'
                                     ':black_square_button: Number of *upcoming* tasks: {}\n'
                                     ':white_check_mark: Number of *completed* tasks: {}\n'
                                     ':scroll: *Total* number of tasks: {}\n'
                                     '\n'
                                     ':bulb: _You can proceed to tasks with buttons below_\n'
                                     ':bulb: _Or write me anything You want to track and I will create a new task for You_ :)\n'
                                     '\n'
                                     'Version: 0.{} Alpha\n',

        'state.view_task.inactive': ':pensive: Probably, this is not the task you are looking for.\n'
                                    '\n'
                                    ':bulb: _To update task list, use the buttons below that list. Task you are looking for could be removed_',
        'state.view_task.review': 'Task review',
        'state.view_task': ':pencil: *{}*\n'
                           '\n'
                           '      `{}`\n'  # task description
                           '\n'
                           'Remind date: *{}*\n'
                           'Create date: *{}*\n'
                           'Category: *{}*\n'
                           'Task status: *{}*\n'
                           'Task ID: {}\n'
                           '\n'
                           ':bulb: _Type /date and write datetime to set reminder (e.g. /date 21 dec 13-37)_',

        'state.new_task.created': 'New task has been created. Please, select category from the variants below',
        'state.new_task.not_created': ':pensive: Sorry, I could not create a task for some reason\n'
                                      'Can you try again, please?',

        'state.all_tasks.tasks.upcoming': 'here are your upcoming tasks:*\n',
        'state.all_tasks.tasks.completed': 'congratulations on completing these tasks:*\n',
        'state.all_tasks.tasks.all': 'here are all the tasks you have now:*\n',
        'state.all_tasks.no_tasks_yet': 'I could not find any tasks of that status*\n',
        'state.all_tasks.notes.no_tasks_yet': '\n:bulb: _To create a new task, just write me something_ :)\n',
        'state.all_tasks.notes': '\n:bulb: _To create a new task, just write me something_ :)\n'
                                 ':bulb: _To refresh the list, use buttons on the bottom of the list_',

        'state.edit_date.success': ':bell: *Notification has been set up!*\n'
                                   '\n'
                                   'I will remind you about this task on *{}*\n',
        'state.edit_date.intersect': '\nDon\'t forget that You have task(s) nearby:\n'
                                     '{}',
        'state.edit_date.intersect.notes': '\n:bulb: _To set up another date, just repeat command from above with new date_',
        'state.edit_date.parse_error': ':pensive: Sorry, I could not recognize that datetime :(\n'
                                       '\n'
                                       ':bulb: _To provide valid datetime, use some of these patterns_:\n'
                                       '"/date 13-37", "/date 21 13-37" _or_ "/date 21 dec 13-37"',
        'state.edit_date.reminder': 'you have a reminder!*\n'
                                    '\n'
                                    '      `{}`\n'   # task description
                                    '\n'
                                    'This task was created on {}',

        'state.select_lang': 'please, select language from the variants below*\n'
                             '\n'
                             ':bulb: _Current language is English_',

        'btn.start_state.to_tasks.upcoming.label': ':black_square_button: Proceed to upcoming tasks',
        'btn.start_state.to_tasks.completed.label': ':white_check_mark: View completed tasks',
        'btn.start_state.to_tasks.all.label': ':scroll: View all tasks',
        'btn.start_state.select_lang.label': ':earth_africa: Select language',

        'btn.select_lang.eng.label': 'English',
        'btn.select_lang.eng.result': 'English language selected',
        'btn.select_lang.rus.label': 'Russian',
        'btn.select_lang.rus.result': 'Russian language selected',

        'btn.all_tasks.upcoming': ':black_square_button: Upcoming',
        'btn.all_tasks.completed': ':white_check_mark: Completed',
        'btn.all_tasks.refresh': ':arrows_counterclockwise: Refresh',
        'btn.all_tasks.home': ':house: Home',

        'btn.view_task.delete_task.label': ':x: Remove',
        'btn.view_task.delete_task.result': ':x: Task with ID "{}" has been removed',
        'btn.view_task.disable_notify.label': ':no_bell: Mute',
        'btn.view_task.disable_notify.result': ':no_bell: Notifications have been muted for task "*{}*"',
        'btn.view_task.enable_notify.label': ':bell: Unmute',
        'btn.view_task.enable_notify.result': ':bell: Notifications have been enabled for task "*{}*"',
        'btn.view_task.mark_as_done.label': ':white_check_mark: Done',
        'btn.view_task.mark_as_done.result': ':white_check_mark: Congratulations on completing the task! :clap:',
        'btn.view_task.mark_undone.label': ':black_square_button: Not done',
        'btn.view_task.mark_undone.result': ':black_square_button: Task has been marked as upcoming',
        'btn.view_task.upcoming.label': ':black_square_button: Upcoming',
        'btn.view_task.completed.label': ':white_check_mark: Completed',
        'btn.view_task.all.label': ':clipboard: All',

        'btn.new_task.project.prs.label': ':bust_in_silhouette: Personal',
        'btn.new_task.project.std.label': ':books: Study',
        'btn.new_task.project.wrk.label': ':briefcase: Work',
        'btn.new_task.project.oth.label': ':open_file_folder: Other'
    },

    Language.RUS: {
        'error': ':pensive: Мне очень жаль, но произошла непредвиденная ошибка :(',

        'date.hr': ' в *{} ч.*',
        'date.hrs': ' в *{} ч.*',
        'date.min': ' в *{} мин.*',
        'date.same': ' *в это же время*',

        'task.upcoming': 'Предстоящая',
        'task.completed': 'Выполнено',
        'task.muted': '(:no_bell: Уведомления выключены)',

        'project.not_selected': ':question: Не распределено',

        'filter.unknown': ':confused: Не удалось распознать Вашу команду :(',

        'state.start_state.welcome': 'добро пожаловать в сервис таск-трекинга!*\n'
                                     '\n'
                                     ':black_square_button: *Предстоящих* задач: {}\n'
                                     ':white_check_mark: *Выполнено* задач: {}\n'
                                     ':scroll: *Всего* задач: {}\n'
                                     '\n'
                                     ':bulb: _Перейдите к задачам с помощью кнопок ниже_\n'
                                     ':bulb: _Чтобы создать задачу, просто напишите мне сообщение_ :)\n'
                                     '\n'
                                     'Версия: 0.{} Alpha\n',

        'state.view_task.inactive': ':pensive: Прости, не удалось найти выбранную задачу.\n'
                                    '\n'
                                    ':buld: _Чтобы обновить список задач, используйте кнопки в конце списка_',
        'state.view_task.review': 'Просмотр задачи',
        'state.view_task':  ':pencil: *{}*\n'   # New task has been created / Task review
                            '\n'
                            '      `{}`\n'  # task description
                            '\n'
                            'Время уведомления: *{}*\n'
                            'Задача создана: *{}*\n'
                            'Категория: *{}*\n'
                            'Статус задачи: *{}*\n'
                            'ID задачи: {}\n'
                            '\n'
                            ':bulb: _Введите /date и дату, чтобы включить уведомление (например, /date 21 дек 13-37)_',

        'state.new_task.created': 'Создана новая задача. Пожалуйста, выберите категорию из вариантов ниже',
        'state.new_task.not_created': ':pensive: Простите, не удалость создать задачу\n'
                                      'Попробуйте еще раз, пожайлуйста',

        'state.all_tasks.tasks.upcoming': 'список Ваших предстоящих задач:*\n',
        'state.all_tasks.tasks.completed': 'поздравляю с завршением этих задач:*\n',
        'state.all_tasks.tasks.all': 'список всех имеющихся у Вас задач на данный момент:*\n',
        'state.all_tasks.no_tasks_yet': 'Не найдено задач с выбранным статусом*\n',
        'state.all_tasks.notes.no_tasks_yet': '\n:bulb: _Чтобы создать задачу, просто напишите мне что-нибудь_ :)\n',
        'state.all_tasks.notes': '\n:bulb: _Чтобы создать задачу, просто напишите мне что-нибудь_ :)\n'
                                 ':bulb: _Чтобы обновить список, используйте кнопки управления внизу списка_',

        'state.edit_date.success': ':bell: *Уведомление установлено!*\n'
                                   '\n'
                                   'Я напомню Вам о задаче, когда настанет *{}*\n',
        'state.edit_date.intersect': '\nНе забудьте, что у Вас уже имеются дела вблизи назначенного времени:\n'
                                     '{}',
        'state.edit_date.intersect.notes': '\n:bulb: _Чтобы изменить время уведомления, просто повторите предыдущую команду с новым временем_',
        'state.edit_date.parse_error': ':pensive: Прости, не удалось распознать дату :(\n'
                                       '\n'
                                       ':bulb: _Для установки уведомления, используйте один из этих паттернов_:\n'
                                       '"/date 13-37", "/date 21 13-37" _или_ "/date 21 дек 13-37"',
        'state.edit_date.reminder': 'у меня для Вас уведомление!*\n'
                                    '\n'
                                    '      `{}`\n'   # task description
                                    '\n'
                                    'Эта задача была добавлена {}',

        'state.select_lang': 'выберите, пожалуйста, язык из предложенных вариантов*\n'
                             '\n'
                             ':bulb: Текущий язык: Русский',

        'btn.start_state.to_tasks.upcoming.label': ':black_square_button: Открыть предстоящие задачи',
        'btn.start_state.to_tasks.completed.label': ':white_check_mark: Посмотреть выполненные задачи',
        'btn.start_state.to_tasks.all.label': ':scroll: Посмотреть весь список задач',
        'btn.start_state.select_lang.label': ':earth_africa: Изменить язык',

        'btn.select_lang.eng.label': 'Английский',
        'btn.select_lang.eng.result': 'Выбран английский язык',
        'btn.select_lang.rus.label': 'Русский',
        'btn.select_lang.rus.result': 'Выбран русский язык',

        'btn.all_tasks.upcoming': ':black_square_button: Предстоящие',
        'btn.all_tasks.completed': ':white_check_mark: Выполненные',
        'btn.all_tasks.refresh': ':arrows_counterclockwise: Обновить',
        'btn.all_tasks.home': ':house: Домой',

        'btn.view_task.delete_task.label': ':x: Удалить',
        'btn.view_task.delete_task.result': ':x: Задача с ID "{}" удалена',
        'btn.view_task.disable_notify.label': ':no_bell: Выкл. уведомл.',
        'btn.view_task.disable_notify.result': ':no_bell: Уведомления выключены для задачи "*{}*"',
        'btn.view_task.enable_notify.label': ':bell: Включить',
        'btn.view_task.enable_notify.result': ':bell: Уведомления для задачи "*{}*" включены',
        'btn.view_task.mark_as_done.label': ':white_check_mark: Готово',
        'btn.view_task.mark_as_done.result': ':white_check_mark: Поздравляю с выполнением задачи! :clap:',
        'btn.view_task.mark_undone.label': ':black_square_button: Отменить',
        'btn.view_task.mark_undone.result': ':black_square_button: Задача отмечена, как предстоящая',
        'btn.view_task.upcoming.label': ':black_square_button: Предстоящие',
        'btn.view_task.completed.label': ':white_check_mark: Выполненные',
        'btn.view_task.all.label': ':clipboard: Все',

        'btn.new_task.project.prs.label': ':bust_in_silhouette: Личное',
        'btn.new_task.project.std.label': ':books: Учеба',
        'btn.new_task.project.wrk.label': ':briefcase: Работа',
        'btn.new_task.project.oth.label': ':open_file_folder: Другое'
    }
}