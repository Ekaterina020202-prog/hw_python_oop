# Constants
LEN_STEP = 0.65
LEN_STROKE = 1.38
M_IN_KM = 1000
# Новые константы
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79
CALORIES_MEAN_SPEED_MULTIPLIER_WALK = 0.035
CALORIES_MEAN_SPEED_MULTIPLIER_SWIM = 2
CALORIES_MEAN_SPEED_SHIFT_SWIM = 1.1
SECONDS_PER_MINUTE = 60


class InfoMessage:

    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f' Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')

    def show_training_info(self):
        print(self.get_message())


class Training:

    def __init__(self, action: int, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return (self.action * LEN_STEP) / M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self):
        pass  # Будет реализовано в дочерних классах


class Running(Training):

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / M_IN_KM * (self.duration
                    * SECONDS_PER_MINUTE))
        return calories


class SportsWalking(Training):

    def __init__(self, action: int, duration: float,
                 weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((CALORIES_MEAN_SPEED_MULTIPLIER_WALK * self.weight
                    + (self.get_mean_speed() ** 2 / self.height)
                    * 0.029 * self.weight)
                    * (self.duration * SECONDS_PER_MINUTE))
        return calories


class Swimming(Training):

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = 2  # переопределение атрибута LEN_STEP

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / M_IN_KM
                / (self.duration * SECONDS_PER_MINUTE))

    def get_spent_calories(self) -> float:
        calories = (CALORIES_MEAN_SPEED_MULTIPLIER_SWIM
                    * self.weight * (self.duration * SECONDS_PER_MINUTE)
                    + CALORIES_MEAN_SPEED_SHIFT_SWIM * self.get_mean_speed())
        return calories


def read_package(workout_type: str, data: list) -> Training:
    workout_mapping = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in workout_mapping:
        workout_class = workout_mapping[workout_type]
        return workout_class(*data)
    else:
        return None


def main(training: Training):
    if training is not None:
        info = InfoMessage(training.__class__.__name__, training.duration,
                           training.get_distance(), training.get_mean_speed(),
                           training.get_spent_calories())
        info.show_training_info()
    else:
        print("Неизвестный тип тренировки")


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
