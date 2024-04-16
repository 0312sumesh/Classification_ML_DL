from django.shortcuts import render, HttpResponse
from .forms import UserRegistrationForm
from django.contrib import messages
from .models import UserRegistrationModel, UserXRayModel
from django.core.files.storage import FileSystemStorage

# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHome.html', {})


def UserMachineLearning(request):
    from .utility.MachineLearingUtility import process_svm
    svm_accracy, knn_accuracy, ann_accuracy = process_svm()
    return render(request, 'users/usersml.html',{'svm': svm_accracy, 'knn': ann_accuracy, 'ann': ann_accuracy})



def upload_xray_form(request):
    return render(request, 'users/UserXRayForm.html',{})


def UserXRayImageActions(request):
    if request.method == 'POST':
        myfile = request.FILES['file']
        if not myfile.name.endswith('.bmp'):
            messages.error(request, 'THIS IS NOT A bmp  FILE')
            return render(request, 'users/UserXRayForm.html', {})
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        from .utility.test_xray import process_xray_image
        filename, output_image, upper_image, lower_image = process_xray_image(filename)
        username = request.session['loggeduser']
        email = request.session['email']
        UserXRayModel.objects.create(username=username, email=email, filename=fs.url(filename), croped=fs.url(output_image), upper_image=fs.url(upper_image),lower_image=fs.url(lower_image))
        messages.success(request, 'Image Processed Success')
        print("File Image Name " + uploaded_file_url)
        return render(request, "users/UserXRayForm.html", {'path': uploaded_file_url})


def UserCropped(request):
    username = request.session['loggeduser']
    data = UserXRayModel.objects.filter(username=username)
    return render(request, "users/UserViewResults.html",{'data': data})
