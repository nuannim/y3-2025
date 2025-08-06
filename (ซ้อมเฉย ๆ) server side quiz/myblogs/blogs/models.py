from django.db import models

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)

class author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=150)

class blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    like = models.IntegerField()
    created_by = models.ForeignKey(author, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    category = models.ManyToManyField(category)

class comment(models.Model):
    comment = models.CharField(max_length=200)
    blog = models.ForeignKey(blog, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


    

