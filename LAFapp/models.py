from django.db import models

# Create your models here.
class Items(models.Model):
	ID = models.AutoField(auto_created = True, primary_key=True, verbose_name="ID")
	status = models.CharField(null=False,blank=True)
	description = models.TextField(null=True,blank=True)
	location = models.TextField(null=True,blank=True)
	email = models.EmailField(null=False,blank=True)
	date = models.DateField(null=True,blank=True)

	def __str__(self):
		return f"{self.status}"
