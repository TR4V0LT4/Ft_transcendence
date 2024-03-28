from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def redirect(request, **kwargs):
    return HttpResponseRedirect('http://localhost:%s' % kwargs.get('var'))