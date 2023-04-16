from django.db import models
from django.utils import timezone

# Create your models here.


class Pages(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    html = models.TextField()
    css = models.TextField()
    preview_link = models.TextField()
    Block_chin_blockNo = models.CharField(max_length=50)
    trans_detial = models.CharField(max_length=50)
    ipfs = models.CharField(max_length=100)


class Blog(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, default='UnTitled')
    description = models.CharField(
        max_length=200, default="Author not provied any description")
    content = models.CharField(
        max_length=2000, default="Author not provied any description")
    blog_profile_img = models.CharField(
        max_length=2000, default="https://www.equalityhumanrights.com/sites/default/files/styles/listing_image/public/default_images/blog-teaser-default-full_5.jpg?itok=YOsTg-7X")
    categories = models.CharField(max_length=200)
    updated_date = models.DateField(default=timezone.now)
    Block_chin_blockNo = models.CharField(max_length=50)
    trans_detial = models.CharField(max_length=50)


class ChatMessage(models.Model):
    prompt = models.CharField(max_length=255)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt} - {self.response}"
