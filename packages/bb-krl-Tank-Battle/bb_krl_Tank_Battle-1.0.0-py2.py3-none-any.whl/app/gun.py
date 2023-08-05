from random import triangular


class Gun(object):
    """класс отвечает за калибр и длину ствола.
    От калибра зависит урон, и, частично, способность к пробитию брони.
    От длины ствола зависит точность стрельбы.
    класс имеет метод is_on_target -> bool, отвечающий за попадание
    """

    def __init__(self, caliber, barrel_length):
        self.caliber = caliber
        self.barrel_length = barrel_length

    def is_on_target(self) -> bool:
        """метод принимает(?) случаюную величину
        возвращает результат bool
        формула расчета: ({длинна пушки) *{dice}) > 100
        """

        rand = triangular(1.0, 6.0)
        return True if self.barrel_length * rand > 100 else False
