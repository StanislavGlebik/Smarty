#encoding=utf-8

from WebServerApp.models import *

from django.contrib.auth.models import User

pullupps_exercise = ExerciseType(activity='Pullups')
pullupps_exercise.save()

bench_exercise = ExerciseType(activity='Bench press')
bench_exercise.save()

sportExercise = SportExercise(training_date="2012-02-02", exercise=pullupps_exercise)
sportExercise.save()

sportExercise = SportExercise(training_date="2012-03-02", exercise=bench_exercise)
sportExercise.save()
