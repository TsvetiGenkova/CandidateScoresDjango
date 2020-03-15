from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Candidate(models.Model):
    
    name = models.TextField()
    candidate_ref = models.CharField(primary_key=True, max_length=8, validators=[RegexValidator("^[a-zA-Z0-9]{8}$", message="Reference is invalid")])

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.candidate_ref + " : " + self.name

    def scores(self):
        return Score.objects.filter(candidate=self)

      
class Score(models.Model):
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    score = models.FloatField(validators=[MinValueValidator(0.0, message="Score can't be less than 0.0"), 
                                         MaxValueValidator(100.0, message="Score can't be more than 100.0")])  
                                             
    class Meta:
        ordering = ('score',) 
    
    def __str__(self):
        return str(self.score)