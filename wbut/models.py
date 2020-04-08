from django.db import models


# Create your models here.
class BasicDetails(models.Model):
    name = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20,primary_key=True)
    college = models.CharField(max_length=100)

    class Meta:
        db_table = "basicDetails"


class SemesterOverview(models.Model):
    basicDetails = models.ForeignKey(BasicDetails, on_delete=models.CASCADE)
    semester = models.IntegerField()
    ygpa = models.CharField(max_length=20)
    cgpa = models.CharField(max_length=20)
    status = models.CharField(max_length=10)

    class Meta:
        db_table = "semOverview"
        unique_together = ('basicDetails', 'semester')


class Result(models.Model):
    basicDetails = models.ForeignKey(BasicDetails, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=10)
    subject_name = models.CharField(max_length=150)
    letter_grade = models.CharField(max_length=1)
    points = models.IntegerField()
    credit = models.FloatField()
    credit_points = models.FloatField()
    semester = models.CharField(max_length=20)

    class Meta:
        db_table = "result"


class College(models.Model):
    collegeCode = models.IntegerField(primary_key=True)
    collegeName = models.CharField(max_length=250)

    class Meta:
        db_table = "colleges"


