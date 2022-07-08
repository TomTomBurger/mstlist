from django.db import models

# Create your models here.
class Group(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    name = models.CharField('グループ名', max_length=30)

class Member(models.Model):

    full_name = models.CharField('名前', max_length=20)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    auth = models.BooleanField(
        '権限A',
        default=False,
    ) 

class player(models.Model):
    age = models.IntegerField()
    name = models.CharField('名前', max_length=20)
    position = models.CharField('ポジション', max_length=20)
    team = models.CharField('チーム', max_length=20)

class Septictank(models.Model):
    cd = models.BigIntegerField('得意先コード', primary_key=True)
    name = models.CharField('名称', max_length=50)
    tel = models.CharField('TEL', max_length=13)

    def __str__(self):
        return self.name

class Sagyo(models.Model):
    cd = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    cd = models.ForeignKey(to=Septictank, on_delete=models.CASCADE, to_field='cd')
    sagyoCd = models.ForeignKey(to=Sagyo, on_delete=models.CASCADE, to_field='cd')
    yDate = models.DateField('予定日')
    yId = models.IntegerField('予定ID')
    tCD = models.IntegerField('担当者コード', default=0)

    def get_MaxId(model):
        schedule = Schedule
        id = 0
        
        try:
            id = schedule.objects.filter(cd=model.cd_id, sagyoCd=model.sagyoCd).latest('yId').yId
        except schedule.DoesNotExist:
            id = 0

        id += 1
        return id

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cd', 'sagyoCd', 'yDate', 'yId'], name='unique_stock')
        ]