import datetime

from django.db import models
from django.contrib.auth.models import User

EDUCATION = (
    ('PHD', 'PHD'),
    ('Degree', 'Degree'),
    ('Diploma', 'Diploma'),
    ('Certificate', 'Certificate'),
    ('High School', 'High School'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Non-Binary', 'Non-Binary'),
)

PAYOUTS = (
    ('One Time', 'One Time'),
    ('Weekly', 'Weekly'),
    ('Fortnight', 'Fortnight'),
    ('Monthly', 'Monthly'),
)


# Create your models here.

class Jobs(models.Model):
    company = models.CharField(max_length=20, default='Local Business')
    title = models.CharField(max_length=20)
    category = models.CharField(max_length=10, default='General')
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=20)
    vacancies = models.IntegerField()
    salary = models.IntegerField()
    payout = models.CharField(max_length=20,
                              choices=PAYOUTS,
                              default='Monthly')
    qualifications = models.CharField(max_length=20, choices=EDUCATION, default='Degree')
    applied = models.IntegerField(default=0)
    date_posted = models.DateField(default=datetime.date.today())

    class Meta:
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title

    @property
    def days(self):
        return (datetime.date.today() - self.date_posted).days


class User_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    dob = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    highQ = models.CharField(max_length=20,
                             choices=EDUCATION,
                             default='Degree', blank=True, null=True)
    institution = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20,
                              choices=GENDER,
                              default='Nairobi', blank=True, null=True)
    dog = models.DateField(blank=True, null=True)
    profile_pic = models.FileField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "User Data"

    def __str__(self):
        return self.user.username


class UserJobs(models.Model):
    user = models.ForeignKey(User_data, on_delete=models.CASCADE)
    job = models.ManyToManyField(Jobs)

    def __str__(self):
        return self.user.user.username
