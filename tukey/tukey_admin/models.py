# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Login(models.Model):
    #id =  models.IntegerField(db_column='userid')
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255, unique=True, blank=True)
    password = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'login'

class LoginEnabled(models.Model):
    userid = models.IntegerField()
    class Meta:
        db_table = u'login_enabled'

class LoginOpenid(models.Model):
    #id =  models.IntegerField(db_column='openid')
    userid = models.ForeignKey(Login, null=True, db_column='userid', blank=True)
    openid = models.CharField(max_length=255, primary_key=True)
    class Meta:
        db_table = u'login_openid'

class LoginShibboleth(models.Model):
    #id =  models.IntegerField(db_column='eppn')
    userid = models.ForeignKey(Login, db_column='userid')
    eppn = models.CharField(max_length=30, primary_key=True)
    class Meta:
        db_table = u'login_shibboleth'

