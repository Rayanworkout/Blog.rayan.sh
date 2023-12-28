from django.db import models
from datetime import datetime
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()
    
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    tags = models.ManyToManyField("Tag")
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title.capitalize()

    def serialize_full(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "category": self.category.name,
            "tags": [tag.name for tag in self.tags.all()],
            "creation_date": self.creation_date.strftime("%B %d, %Y"),
        }

    def serialize_short(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category.name,
            "tags": [tag.name for tag in self.tags.all()],
            "creation_date": self.creation_date.strftime("%B %d, %Y"),
        }

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()
        super().save(*args, **kwargs)



class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name.capitalize()
    
    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name.capitalize()
