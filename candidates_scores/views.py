from django.shortcuts import render
from candidates_scores.models import Candidate, Score


def home(request):
    return render(request, 'candidates_scores/home.html')

def candidates(request):
    context = {'candidates': Candidate.objects.all() }

    return render(request, 'candidates_scores/candidates.html', context)
