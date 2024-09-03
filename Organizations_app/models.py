from django.db import models

# Create your models here.
class Organisation(models.Model):
    name = models.CharField(max_length=255, null=False)
    status = models.IntegerField(default=0, null=False)
    personal = models.BooleanField(default=False, null=True)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    def __str__(self):
        return self.name
    
class User(models.Model):
    email = models.CharField(max_length=255,unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    profile = models.JSONField(default=dict, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    def __str__(self):
        return self.email
    
class Member(models.Model):
    org_id = models.ForeignKey('Organisation', on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE, null=False)
    status = models.IntegerField(default=0, null=False)
    settings = models.JSONField(default=dict, null=True)
    created_at = models.BigIntegerField(null=True)
    updated_at = models.BigIntegerField(null=True)

    def __str__(self):
        return f"Member of {self.org_id.name}"
    
class Role(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    org_id = models.ForeignKey('Organisation', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name