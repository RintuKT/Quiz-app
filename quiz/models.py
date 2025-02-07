from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Course(models.Model):
    COURSE_CHOICES = [
        ('10_KERALA', '10th Kerala Syllabus'),
        ('10_CBSE', '10th CBSE'),
        ('PLUS_ONE', '+1'),
        ('PLUS_TWO', '+2'),
    ]
    
    name = models.CharField(max_length=20, choices=COURSE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

class Subject(models.Model):
    SUBJECT_TYPES = [
        ('LANGUAGE', 'Language'),
        ('SCIENCE', 'Science'),
        ('MATHEMATICS', 'Mathematics'),
    ]
    
    name = models.CharField(max_length=100)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'course']

    def __str__(self):
        return f"{self.name} ({self.get_subject_type_display()} - {self.course})"

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    positive_points = models.IntegerField(default=1)
    negative_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"

class UserSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'question']]

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    registration_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            # Generate a unique registration number
            last_profile = UserProfile.objects.order_by('-registration_number').first()
            if last_profile and last_profile.registration_number.startswith('REG'):
                last_number = int(last_profile.registration_number[3:])
                self.registration_number = f'REG{str(last_number + 1).zfill(6)}'
            else:
                self.registration_number = 'REG000001'
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for every new User."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
