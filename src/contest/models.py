from django.db import models

class contest_type(models.Model):
    contest_type = models.CharField(max_length=200, null=False)
    is_active= models.BooleanField(default=True)

    class Meta: 
        db_table = 'contest_type'

'''class contest(models.Model):
    '''