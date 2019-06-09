import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField


class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    description = models.TextField(null=True)
    environments = JSONField(null=True, default={})
    requests = JSONField(null=True, default={})
    # Audit Details
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=200)

    class Meta:
        db_table = 'domain'


class JobHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    environment = models.CharField(max_length=200)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(auto_now_add=True)
    output = models.TextField(null=True)
    delivery_log = models.TextField(null=True)
    status = models.CharField(max_length=15, null=True)
    job_data = JSONField(null=True, default={})
    # Audit Details
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=200)

    class Meta:
        db_table = 'job_history'


class InfraDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField(null=True, default={})
    # Audit Details
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=200)

    class Meta:
        db_table = 'infra_details'


class Measure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = JSONField(null=True, default={})
    # Audit Details
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=200)
    modified_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=200)

    class Meta:
        db_table = 'measure'