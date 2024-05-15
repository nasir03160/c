from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10)  # New field for student ID
    
    def __str__(self):
        return self.user.username

class ChatLogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    user_input = models.TextField()
    analysis_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Input: {self.user_input[:20]}... | Result: {self.analysis_result[:20]}..."  # Truncate for better display