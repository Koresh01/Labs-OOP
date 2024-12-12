from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError(_('%s(value) must be positive'), params={"value": value})
    
# Create your models here.
class Currency(models.Model):
    UID = models.CharField('UID', max_length=10, null=False, unique=True)
    NumCode = models.CharField('NumCode', max_length=3, unique=True)
    CharCode = models.CharField('CharCode', max_length=3, unique=True)
    Nominal = models.IntegerField('Nominal', validators=[MinValueValidator(1)])
    Name = models.CharField('Name', max_length=50)
    Value = models.FloatField('Value', validators=[validate_positive])
    Previous = models.FloatField('Previous', validators=[validate_positive])
    
    def __str__(self):
        # return f"{self.id} - {self.UID} - {self.Name} - {self.CharCode} - {self.Nominal} - {self.Name} - {self.Value} - {self.Previous}"
        return self.CharCode
    
    def exchange_to(self, ammount:int, currency):   # גאכ‏üא ט ךמכ-גמ
        if type(currency) != type(self):
            raise TypeError('currency must be of type Currency')
        return ammount * self.Value / self.Nominal / currency.Value * currency.Nominal
    