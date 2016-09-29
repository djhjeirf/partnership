from chairman.data_mapper.model import *


class LandCategory(Model):
    name = TextField('Название')

    def __str__(self):
        return str(self.name)


class UseCase(Model):
    name = TextField('Название')

    def __str__(self):
        return str(self.name)


class LandPlot(Model):
    cadastral_number = TextField('cadastral_number', alt_name="Кадастровый номер", null=False)
    prev_number = TextField('prev_number', alt_name="Предыдущие номер", null=True)
    add_date = DateField('add_date', alt_name="Дата внесения в кадастр")
    land_category = ForeignKey('land_category', model=LandCategory, alt_name="Категория земель")
    permitted_use = ForeignKey('permitted_use', model=UseCase, alt_name="Разрешенное использование")
    land_area = FloatField('land_area', alt_name="Площадь участка")
    cadastral_value = FloatField('cadastral_value', alt_name="Кадастровая стоимость", null=True)
    region = TextField('region', alt_name="Область", null=True)
    district = TextField('district', alt_name="Район", null=True)
    settlement = TextField('settlement', alt_name="Населенный пункт", null=True)

    def __str__(self):
        return str(self.cadastral_number) + ' ' + str(self.region) + ' ' + str(self.district) + ' ' + \
               str(self.settlement)


class Rightholder(Model):
    first_name = TextField('first_name', alt_name="Имя")
    middle_name = TextField('middle_name', alt_name="Отчество")
    last_name = TextField('last_name', alt_name="Фамилия")
    birth_date = DateField('birth_date', alt_name="Дата рождения")
    passport_series = IntegerField('passport_series', alt_name="Серия паспорта")
    passport_number = IntegerField('passport_number', alt_name="Номер паспорта")

    @staticmethod
    def get_owner_id(str):
        args = str.split(' ')
        owners = Rightholder.find(first_name=args[1], middle_name=args[2], last_name=args[0], birth_date=args[3])
        if owners:
            return owners[0].id
        else:
            return None

    def __str__(self):
        return str(self.last_name) + ' ' + str(self.first_name) + ' ' + str(self.middle_name) + ' ' + \
               str(self.birth_date)


class LandUseCase(Model):
    land_plot = ForeignKey('land_plot', model=LandPlot, alt_name="Участок")
    use_case = ForeignKey('use_case', model=UseCase, alt_name="Разрешенное использование")

    def __str__(self):
        return str(self.land_plot) + ' ' + str(self.use_case)


class LandOwnerInformation(Model):
    land_plot = ForeignKey('land_plot', model=LandPlot, alt_name="Участок")
    rightholder = ForeignKey('rightholder', model=Rightholder, alt_name="Правообладатель")
    document = TextField('document', alt_name="Документ подтверждающий права")

    def __str__(self):
        return str(self.land_plot) + ' ' + str(self.rightholder)
    

class RightholderHistory(Model):
    rightholder = ForeignKey('rightholder', model=Rightholder, alt_name="Правообладатель")
    land_plot = ForeignKey('land_plot', model=LandPlot, alt_name="Участок")
    rights_acquisition_date = DateField('rights_acquisition_date', alt_name="Дата приобретения права")
    lapse = DateField('lapse', alt_name="Дата прекращения права")

    def __str__(self):
        return str(self.land_plot) + ' ' + str(self.rightholder)
