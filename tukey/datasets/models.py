from django.db import models

class DataSet(models.Model):
	#the ark_key should probably be automatically created based on prefix/num, possibly a trigger? for now, managed in the code.
    ark_key = models.CharField(max_length=500, primary_key=True)
    prefix = models.CharField(max_length=10)
    num = models.IntegerField()

class Key(models.Model):
    key_name = models.CharField(max_length=1000, primary_key=True)
    public = models.BooleanField()

class KeyValue(models.Model):
    dataset = models.ForeignKey(DataSet)
    key = models.ForeignKey(Key)
    value = models.TextField(blank=True)
