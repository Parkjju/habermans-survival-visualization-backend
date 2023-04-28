import pandas as pd
from django.db import models

class Patient(models.Model):
    age = models.IntegerField()
    operation_year = models.IntegerField()
    nb_pos_detected = models.IntegerField()
    surv = models.IntegerField()

    def __str__(self):
        return f"Patient {self.pk}"