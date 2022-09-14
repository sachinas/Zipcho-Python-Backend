from authentication.models import User
from django.db import models

class userPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post_id = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.post_id

class report(models.Model):
    reason = models.CharField(max_length= 300)
    
    class Meta : 
        db_table = 'report'

class reportPost(models.Model):
    post_id = models.CharField(max_length=100)
    reason = models.ForeignKey(report, on_delete=models.PROTECT,
                             related_name='reportPostReason')
    user =  models.ForeignKey(User, on_delete=models.PROTECT)

