from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10)  # New field for student ID
    
    def __str__(self):
        return self.user.username
