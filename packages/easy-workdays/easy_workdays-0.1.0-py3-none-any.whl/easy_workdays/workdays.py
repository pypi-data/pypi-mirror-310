# -*- coding: utf-8 -*-

from datetime import date
from calendar import monthrange


class WorkDay:
    """
    Рабочий день
    """
    def __init__(self, num=0, day=None, weekend=False, holiday=False, work_num=0):
        """
        :param num: порядковый номер дня в году
        :param day: день года
        :param weekend: выходной?
        :param holiday: праздник?
        :param work_num: номер рабочего дня
        :type num: int
        :type day: date
        :type weekend: bool
        :type holiday: bool
        :type work_num: int
        """
        self.num = num
        self.day = day
        self.weekend = weekend
        self.holiday = holiday
        self.work_num = work_num
        # название дня недели на английском
        self.title = self.day.strftime('%A') if self.day else None

    def __str__(self):
        return 'WorkDay(title={}, num={}, day={}, weekend={}, holiday={}, work_num={})'.format(
            self.title,
            self.num,
            self.day.isoformat() if self.day else None,
            self.weekend,
            self.holiday,
            self.work_num
        )

    def __repr__(self):
        return 'WorkDay(title={}, num={}, day={}, weekend={}, holiday={}, work_num={})'.format(
            self.title,
            self.num,
            self.day.isoformat() if self.day else None,
            self.weekend,
            self.holiday,
            self.work_num
        )


class WorkCalendar:
    """
    Производственный календарь
    Пример использования:
    1. Если для целевого года не указаны праздничные дни, то необходимо их добавить.

    -- Создание и добавление списка праздничных дней --

    holidays = [
        date(2022, 1, 1),
        date(2022, 1, 2),
        date(2022, 1, 3),
        date(2022, 1, 4),
        date(2022, 1, 5),
        date(2022, 1, 6),
        date(2022, 1, 7),
        date(2022, 2, 23),
        date(2022, 3, 7),
        date(2022, 3, 8),
        date(2022, 5, 1),
        date(2022, 5, 2),
        date(2022, 5, 3),
        date(2022, 5, 9),
        date(2022, 5, 10),
        date(2022, 6, 12),
        date(2022, 6, 13),
        date(2022, 11, 4),
    ]
    work_calendar.set_holidays(holidays)

    2. Если какие-то праздничные или выходные дня в вашей организации являются рабочими днями
    и для того чтобы номер рабочего дня при этом выдавался правильный, необходимо указать явно
    какой выходной или праздничный день является рабочим

    -- Создание и добавление списка рабочих дней --

    work_calendar.set_work_days([date(2022, 3, 5), date(2022, 3, 6)])

    3. Получение номера рабочего дня

    print(work_calendar.get_work_day_number(task_date))
    """
    def __init__(self, year=None):
        """
        :param year год в формате 'YYYY'
        :type year: int
        """
        # все дни года list[date]
        self.year_days = list()
        # рабочие и нерабочие дни года list[WorkDay]
        self.year_workdays = dict()

        self.TASK_YEAR = date.today().year if not year else year
        self.init()

    def init(self):
        """Инициализация(заполнение) рабочего календаря"""
        # проходим по каждому месяцу года
        for month in range(1, 13):
            # проходим по каждому дня месяца
            for day in range(1, monthrange(self.TASK_YEAR, month)[1] + 1):
                self.year_days.append(date(self.TASK_YEAR, month, day))

        for i, day in enumerate(self.year_days):
            self.year_workdays[day] = {
                'num': i + 1,
                'day': day,
                'weekend': day.weekday() == 5 or day.weekday() == 6
            }

            self.year_workdays[day] = WorkDay(
                num=i + 1,
                day=day,
                weekend=day.weekday() == 5 or day.weekday() == 6
            )

    def get_day(self, task_date):
        """
        Получить определенный день

        :param task_date: Определенная дата
        :return: Информация о дате
        :type task_date: date
        :rtype: WorkDay
        """
        return self.year_workdays.get(task_date)

    def set_holidays(self, holidays):
        """
        Указать даты праздников

        :param holidays: Даты праздников
        :type holidays: list[date]
        :return: True | False
        :rtype: bool
        """
        if holidays:
            for holiday in holidays:
                self.year_workdays[holiday].holiday = True
            return True
        else:
            return False

    def _set_work_day(self, task_date):
        """
        Указать что день рабочий
        :param task_date: целевая дата
        :type task_date: date
        :rtype: bool
        """
        task_day = self.get_day(task_date)
        task_day.weekend = False
        task_day.holiday = False
        return True

    def set_work_days(self, workdays):
        """
        Указать даты рабочих дней

        :param workdays: Даты праздников
        :type workdays: list[date]
        :return: True | False
        :rtype: bool
        """
        if workdays:
            for workday in workdays:
                self._set_work_day(workday)
            return True
        else:
            return False

    def _get_weekends_count(self, task_date):
        """
        Кол-во выходных в году до целевой даты (не включая целевой даты)
        :param task_date: целевая дата
        :type task_date: date
        :rtype: int
        """
        weekends_count = 0
        for month in range(1, 13):
            for day in range(1, monthrange(self.TASK_YEAR, month)[1] + 1):
                if date(self.TASK_YEAR, month, day) == task_date:
                    return weekends_count
                dday = self.get_day(date(self.TASK_YEAR, month, day))
                if dday.weekend and not dday.holiday:
                    weekends_count += 1
        return weekends_count

    def _get_holidays_count(self, task_date):
        """
        Кол-во праздников в году до целевой даты (не включая целевой даты)
        :param task_date: целевая дата
        :type task_date: date
        :rtype: int
        """
        holidays_count = 0
        for month in range(1, 13):
            for day in range(1, monthrange(self.TASK_YEAR, month)[1] + 1):
                if date(self.TASK_YEAR, month, day) == task_date:
                    return holidays_count
                dday = self.get_day(date(self.TASK_YEAR, month, day))
                if dday.holiday:
                    holidays_count += 1
        return holidays_count

    def get_work_day_number(self, task_date):
        """
        Номер рабочего дня в году
        :param task_date: целевая дата
        :type task_date: date
        :rtype: int
        """
        return self.get_day(task_date).num - self._get_weekends_count(task_date) - self._get_holidays_count(task_date)