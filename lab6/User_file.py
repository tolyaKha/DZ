import pymysql as MySQLdb
from users.models import Fight, Boxer
from django.shortcuts import render
from django.http import HttpResponseRedirect


class Connection:

    def __init__(self, user, password, db, host='localhost'):
        self.user = user
        self.host = host
        self.password = password
        self.db = db
        self._connection = None

    @property
    def connection(self):
        return self._connection

    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        if not self._connection:
            self._connection = MySQLdb.connect(
                host = self.host,
                user=self.user,
                passwd=self.password,
                db=self.db
            )

    def disconnect(self):
        if self._connection:
            self._connection.close()


class myFight:

    def __init__(self, db_connection, id, idFight, date, time, boxer1, boxer2, idBoxer1, idBoxer2):
        self.db_connection = db_connection
        self.id = id
        self.idFight = idFight
        self.date = date
        self.time = time
        self.boxer1 = boxer1
        self.boxer2 = boxer2
        self.idBoxer1 = idBoxer1
        self.idBoxer2 = idBoxer2

    def save(self):
        c = self.db_connection.cursor()
        c.execute("INSERT INTO users_fight (id, idFight, date, time, boxer1, boxer2, idBoxer1, idBoxer2)"
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                  (self.id, self.idFight, self.date, self.time, self.boxer1,
                   self.boxer2, self.idBoxer1, self.idBoxer2))
        self.db_connection.commit()
        c.close()


def NewFight(request):
    errors = []
    if request.method == 'POST':
        idFight = request.POST.get('idFight')
        if not idFight:
            errors.append('Введите idFight')
        date = request.POST.get('date')
        if not date:
            errors.append('Введите дату')
        time = request.POST.get('time')
        if not time:
            errors.append('Введите время')
        boxer1 = request.POST.get('boxer1')
        if not boxer1:
            errors.append('Введите первого боксера')
        boxer2 = request.POST.get('boxer2')
        if not boxer2:
            errors.append('Введите второго боксера')
        idBoxer1 = request.POST.get('idBoxer1')
        if not idBoxer1:
            errors.append('Введите idBoxer1')
        idBoxer2 = request.POST.get('idBoxer2')
        if not idBoxer2:
            errors.append('Введите idBoxer2')
        else:
            if len(errors) == 0:
                idFight1 = Fight.objects.filter(idFight=idFight)
                idBoxer1_1 = Boxer.objects.filter(idBoxer=idBoxer1)
                idBoxer2_1 = Boxer.objects.filter(idBoxer=idBoxer2)
                if len(idFight1) != 0:
                    errors.append('Бой с таким id уже сужествует')
                    return render(request, 'newFight.html', {'errors': errors, 'idFight': idFight, 'date': date,
                                                             'time': time, 'boxer1': boxer1, 'boxer2': boxer2,
                                                             'idBoxer1': idBoxer1, 'idBoxer2': idBoxer2})
                elif len(idBoxer1_1) == 0:
                    errors.append('Боксер1 с таким id не сужествует')
                    return render(request, 'newFight.html', {'errors': errors, 'idFight': idFight, 'date': date,
                                                             'time': time, 'boxer1': boxer1, 'boxer2': boxer2,
                                                             'idBoxer1': idBoxer1, 'idBoxer2': idBoxer2})
                elif len(idBoxer2_1) == 0:
                    errors.append('Боксер2 с таким id не сужествует')
                    return render(request, 'newFight.html', {'errors': errors, 'idFight': idFight, 'date': date,
                                                             'time': time, 'boxer1': boxer1, 'boxer2': boxer2,
                                                             'idBoxer1': idBoxer1, 'idBoxer2': idBoxer2})
        con = Connection("admin", "12345", "first_db")
        with con:
            fight = myFight(con.connection, idFight, idFight, date, time, boxer1, boxer2, idBoxer1, idBoxer2)
            fight.save()
        return HttpResponseRedirect('/fights/')
    return render(request, 'newFight.html', {'errors': errors})
