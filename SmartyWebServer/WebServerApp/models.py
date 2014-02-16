from django.db import models

class SportExercise(models.Model):
    training_date = models.DateField()
    exercise = models.ForeignKey('ExerciseType')
    
    def __unicode__(self):
        return self.exercise.activity + " " + str(self.training_date)

class ExerciseType(models.Model):
    EXERCISES_TYPES = (
        ('Pullups', 'Pullups'),
        ('Bench press', 'Bench press'),
    )

    activity = models.CharField(max_length=50, primary_key=True, choices=EXERCISES_TYPES)
    img_ref = models.CharField(max_length=255, default="NO_IMAGE")

    def __unicode__(self):
        return self.activity
