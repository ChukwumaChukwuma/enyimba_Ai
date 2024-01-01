from django.db import models

# Create your models here.

class UserQuery(models.Model):
    query_text = models.TextField()
    response_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query made on {self.created_at}"
