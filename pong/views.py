from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# import requests
# from django.http import JsonResponse
# Create your views here.

@login_required
def redirect(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		print('*************', user_id)
	return HttpResponseRedirect(f'http://localhost:1234/?user_id={user_id}')

# def index(request):
# 	return render(request, 'pong.html')
# def send_data_to_npm(request, **kwargs):
# 	data = {'id': request.user.id}  # Your data to be sent
# 	npm_server_url = 'http://localhost:1234/' # Replace with your npm server URL
	
# 	# Send data to npm server
# 	response = requests.post(npm_server_url, json=data)

# 	if response.status_code == 200:
# 		return HttpResponseRedirect('http://0.0.0.0:%s' % kwargs.get('var'))
# 	else:
# 		return JsonResponse({'message': 'Failed to send data'}, status=500)
