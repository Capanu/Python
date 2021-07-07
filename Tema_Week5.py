class Fractie:

    def cmmdc(a, b):
        cpy_a = a
        cpy_b = b

        while cpy_a != cpy_b:
            if cpy_a> cpy_b:
                cpy_a = cpy_a -cpy_b
            else:
                cpy_b = cpy_b - cpy_a

        return cpy_a

    def cmmc(a,b):
        return a*b // Fractie.cmmdc(a,b)

    def __init__(self, numarator, numitor):
        self.numarator = numarator
        self. numitor = numitor

    def __str__(self):
            return f'{self.numarator}/{self.numitor}'

    def __add__(self, other):
         aux_numitor = Fractie.cmmc(self.numitor, other.numitor)
         aux_numartor= self.numarator * (aux_numitor//self.numitor) + other.numarator* (aux_numitor//other.numitor)
         return Fractie(aux_numartor, aux_numitor)

    def __sub__(self, other):
        aux_numitor = Fractie.cmmc(self.numitor, other.numitor)
        aux_numartor = self.numarator * (aux_numitor // self.numitor) - other.numarator * (aux_numitor // other.numitor)
        return Fractie(aux_numartor, aux_numitor)

    def inverse(self):
        return Fractie(self.numitor, self.numarator)


fr1 = Fractie(4, 10)
fr2 = Fractie(3, 200)
print(f'\n\nFractiile sunt  {fr1}, {fr2}:')
print(f'Adunare {fr1} cu {fr2}: ' + str(fr1.__add__(fr2)))
print(f'Scadere din  {fr1} cu {fr2}: ' + str(fr1.__sub__(fr2)))
print(f'Invers  {fr1}: ' + str(fr1.inverse()))
print(f'Invers  {fr2}: ' + str(fr2.inverse()))


fr1 = Fractie(4, 15)
fr2 = Fractie(3, 75)
print(f'\n\nFractiile sunt  {fr1}, {fr2}:')
print(f'Adunare {fr1} cu {fr2}: ' + str(fr1.__add__(fr2)))
print(f'Scadere din  {fr1} cu {fr2}: ' + str(fr1.__sub__(fr2)))
print(f'Invers  {fr1}: ' + str(fr1.inverse()))
print(f'Invers  {fr2}: ' + str(fr2.inverse()))