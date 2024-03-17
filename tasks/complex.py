"""
Реализуйте класс Complex, экземпляры которого представляют собой комплексные
числа.

Конструктор Complex принимает два параметра: real, отражающий вещественную часть
числа, и imag, отражающий множитель числа i. Оба параметра должны поддерживать
позиционные и ключевые аргументы и иметь значение по умолчанию 0.

Экземпляры Complex должны поддерживать следующие операции:

- сложение (+),
- вычитание (-),
- умножение (*),
- деление (/),
- проверка равенства (==, !=).

Результатом всех операций (кроме == и !=) должны быть новые экземпляры Complex,
старые экземпляры при этом не должны изменяться.

Эти операции должны поддерживаться между любыми экземплярами Complex или
встроенных типов int и float вне зависимости от порядка аргументов. Примеры
допустимых операций:

>>> 1 + Complex(1, 2)
Complex(2, 2)

>>> Complex(3, 4) - 0.5
Complex(2.5, 4) 

>>> 3 / Complex(-2, 1)
Complex(-1.2, -0.6)

>>> Complex(5, 1) * Complex(0.4, 0.3)
Complex(1.7, 1.9)

>>> 7.7 == Complex(real=7.7)
True

>>> -1 == Complex(real=-1, imag=4)
False

Строковое представление экземпляров Complex должно иметь вид "a+bi" при
положительных b. При отрицательных знак "+" опускается. Примеры:

>>> print(Complex())
0+0i

>>> print(Complex(1))
1+0i

>>> print(Complex(1, 2))
1+2i

>>> print(Complex(-1, -2))
-1-2i
"""

from __future__ import annotations  # игнорируйте эту строку


class Complex:
    __match_args__ = ("real", "imag")

    def __init__(self, real: float = 0, imag: float = 0):
        self.real = real
        self.imag = imag

    def __add__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)

        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)

        return NotImplemented

    def __radd__(self, other) -> Complex:
        return self + other

    def __sub__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)

        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)

        return NotImplemented

    def __rsub__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(other - self.real, -self.imag)

        if isinstance(other, Complex):
            return Complex(other.real - self.real, other.imag - self.imag)

        return NotImplemented

    def __mul__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)

        if isinstance(other, Complex):
            # (a + bi) * (c + di)   == ac + bci + adi + bdii
            #                       == ac + bd + bci + adi
            #                       == (ac - bd) + (bc + ad)i
            a, b = self.real, self.imag
            c, d = other.real, other.imag
            return Complex(
                real=a * c - b * d,
                imag=b * c + a * d,
            )

        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other) -> Complex:
        if isinstance(other, (int | float)):
            return Complex(self.real / other, self.imag / other)

        if isinstance(other, Complex):
            # (a + bi) / (c + di)   == ((a + bi)(c - di)) / ((c + di)(c - di))
            #                       == ((a + bi)(c - di)) / (cc + dd)
            #                       == (ac + bd)/(cc + dd) + (bc - ad)/(cc + dd)
            a, b = self.real, self.imag
            c, d = other.real, other.imag
            return Complex(
                real=(a * c + b * d) / (c**2 + d**2),
                imag=(b * c - a * d) / (c**2 + d**2),
            )

        return NotImplemented

    def __rtruediv__(self, other) -> Complex:
        c, d = self.real, self.imag

        if isinstance(other, (int | float)):
            a, b = other, 0
        elif isinstance(other, Complex):
            a, b = other.real, other.imag
        else:
            return NotImplemented

        # (a + bi) / (c + di)   == ((a + bi)(c - di)) / ((c + di)(c - di))
        #                       == ((a + bi)(c - di)) / (cc + dd)
        #                       == (ac + bd)/(cc + dd) + (bc - ad)/(cc + dd)
        return Complex(
            real=(a * c + b * d) / (c**2 + d**2),
            imag=(b * c - a * d) / (c**2 + d**2),
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self.real == other and self.imag == 0

        if isinstance(other, Complex):
            return self.real == other.real and self.imag == other.imag

        return NotImplemented

    def __str__(self) -> str:
        real = self.real
        if isinstance(real, float) and real.is_integer():
            real = int(real)
        imag = self.imag
        if isinstance(imag, float) and imag.is_integer():
            imag = int(imag)
        imag_str = f"{imag}i"
        if self.imag >= 0:
            imag_str = f"+{imag_str}"
        return f"{real}{imag_str}"

    __repr__ = __str__
