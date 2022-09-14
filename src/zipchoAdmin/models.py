from django.db import models

class gender(models.Model):
    gender = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.gender)

class interest(models.Model):
    interest = models.CharField(max_length=100)

    def __str__(self):
        return str(self.interest)

class category(models.Model):
    interest = models.ForeignKey(interest, on_delete=models.PROTECT)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.category)

class language(models.Model):
    language = models.CharField(max_length=150)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.language)

class country(models.Model):
    country = models.CharField(max_length=150)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.country)

class identityDocument(models.Model):
    document = models.CharField(max_length=250)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.document)

class verificationLink(models.Model):
    linkType = models.CharField(max_length=250)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.linkType)
    
class userVerificationDocs(models.Model):
    userId = models.IntegerField(null=False)
    identityDocument = models.ForeignKey(identityDocument, on_delete=models.PROTECT)
    docPath = models.FileField(upload_to='identityDocuments', default =None, null=True)
    userVerificationLinkId = models.IntegerField(null=True)

class userVerificationLinks(models.Model):
    userVerificationDocs = models.IntegerField(null=True)

    firstLink = models.IntegerField(null=True)
    firstLinkPath = models.CharField(max_length=400,null=True)
    
    secondLink = models.IntegerField(null=True)
    secondLinkPath = models.CharField(max_length=400,null=True)
    
    thirdLink = models.IntegerField(null=True)
    thirdLinkPath = models.CharField(max_length=400,null=True)
    
    fourthLink = models.IntegerField(null=True)
    fourthLinkPath = models.CharField(max_length=400,null=True)
    
    fifthLink = models.IntegerField(null=True)
    fifthLinkPath = models.CharField(max_length=400,null=True)

