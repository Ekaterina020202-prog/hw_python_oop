class InfoMessage:
    """
    Информационное сообщение о тренировке.
    Обозначения:
    training_type: Тип тренировки;
    duration: Длительность тренировки;
    distance: Дистанция, пройденная во время тренировки;
    speed: Средняя скорость движения во время тренировки;
    calories: Количество затраченных калорий во время тренировки.
    """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        """
        Создает экземпляр класса InfoMessage.
        """
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """
        Возвращает информационное сообщение о выполненной тренировке.
        """
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """
    Базовый класс тренировки.
    LEN_STEP: Длина шага
    M_IN_KM: Количество метров в одном километре.
    MIN_IN_H: Количество минут в одном часе.
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        """
        Создает экземпляр класса Training.
        Обозначения:
        action: Действие, которое выполнялось во время тренировки;
        duration: Длительность тренировки;
        weight: Вес человека, выполнявшего тренировку.
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """
        Возвращает дистанцию в км, пройденную во время тренировки.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """
        Возвращает среднюю скорость движения и называем её mean_speed.
        """
        training_distance = self.get_distance()
        mean_speed = training_distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """
        Возвращает количество затраченных калорий.
        """
        pass  # Метод будет реализован в дочерних классах.

    def show_training_info(self) -> InfoMessage:
        """
        Возвращает информационное сообщение о выполненной тренировке.
        """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """
    Тренировка: бег.
    """

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """
        Возвращает количество затраченных калорий во время бега.
        """
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * self.get_mean_speed()
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.MIN_IN_H)
                    )

        return calories


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    """

    CALORIES_WEIGHT_MULTIPLIER_WALK = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER_WALK: float = 0.029
    CM_IN_M: int = 100
    POW_COEF: int = 2
    KMH_IN_MSEC: float = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        """
        Создает экземпляр класса SportsWalking.
        Обозначения:
        action: Действие, которое выполнялось во время тренировки;
        duration: Длительность тренировки;
        weight: Вес человека, выполнявшего тренировку.
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Возвращает кол-во затраченных калорий во время спортивной ходьбы.
        """
        mean_speed = self.get_mean_speed() * self.KMH_IN_MSEC
        training_time_in_minutes = self.duration * self.MIN_IN_H
        height = self.height / self.CM_IN_M
        return ((self.CALORIES_WEIGHT_MULTIPLIER_WALK * self.weight
                 + (mean_speed ** self.POW_COEF / height)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER_WALK * self.weight)
                * training_time_in_minutes)


class Swimming(Training):
    """
    Тренировка: плавание.
    """

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT_SWIM = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER_SWIM = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        """
        Создает экземпляр класса Swimming.
        length_pool: Длина бассейна.
        count_pool: Сколько раз пользователь переплыл бассейн.
        duration: Длительность тренировки.
        weight: Вес человека, выполнявшего тренировку.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """
        Возвращает среднюю скорость движения.
        """
        mean_speed = ((self.length_pool * self.count_pool)
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """
        Возвращает кол-во потраченных калорий во время плавания.
        """
        mean_speed = self.get_mean_speed()
        return (((mean_speed + self.CALORIES_MEAN_SPEED_SHIFT_SWIM)
                 * self.CALORIES_MEAN_SPEED_MULTIPLIER_SWIM)
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """
    Читает данные полученные от датчиков.
    """
    workout_codes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_codes[workout_type](*data)


def main(training: Training) -> None:
    """
    Главная функция.
    """
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
