from abc import ABC, abstractmethod


class Formated(ABC):
    @abstractmethod
    def formate_time(self, time: str) -> list:
        ...

    @abstractmethod
    def formate_date(self, date: str) -> list:
        ...


class FormatedDateTime(Formated):
    def formate_time(self, time: str) -> list:
        """
        Обработка исходной строчки и превращение ее в удобную для анализа и превращения в datetime

        :param time: Исходная строчка формата xx:xx
        :return:
        """
        hour, minute = time.split(":")

        return int(hour), int(minute)

    def formate_date(self, date: str) -> list:
        year, mouth, day = tuple(map(int, date.split("-")))

        assert mouth <= 12 and mouth >= 1, "Число месяца должно быть в диапазоне 1-12"
        assert day <= 31 and day >= 1, "Число дня должно быть в диапазоне 1-31"

        return (year, mouth, day)