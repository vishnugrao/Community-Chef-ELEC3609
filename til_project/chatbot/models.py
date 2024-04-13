from django.db import models

class CaseInsensitiveCharField(models.CharField):
    def get_prep_value(self, value):
        if value is not None:
            return value.lower().capitalize()
        return value

class Ingredient(models.Model):
    name = CaseInsensitiveCharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name