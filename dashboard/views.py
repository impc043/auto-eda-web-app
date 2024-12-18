from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from .models import Project
from .forms import CreateProjectForm
from django.views.decorators.cache import cache_page
from django.conf import settings

from analyzer import insights, insights_v2
from django.contrib import messages


# Create your views here.
# @login_required(login_url='login')
# def dashboard(request):
#     # profile_ = User.objects.get(username=request.user)
#     # print(profile_.profile.profile_img)
#     pro = request.user.profile.project_set.all()
#     file_path = pro[0].project_file.url
#     b = str(settings.MEDIA_ROOT).replace('\\','\\')+ str(file_path).replace('/','\\').replace('\media', '')
    
#     data_ = pd.read_csv(b)

#     labels_ = list(data_.columns)
#     print(data_.value_counts())
#     data = [10, 20, 30, 40]
  
#     context = {'pro':pro,'labels': labels_, 'data': data}
#     return render(request, 'dashboard/dashboard.html', context)
@login_required(login_url='login')
def dashboard(request):
    pro = request.user.profile.project_set.all()
  
    context = {'pro':pro}
    return render(request, 'dashboard/dashboard_new.html', context)

@login_required(login_url='login')
def create_project(request):
    if request.method == 'POST':
        obj = Profile.objects.get(user__id = request.user.id)
        form = CreateProjectForm(request.POST or None, request.FILES, instance=obj)
        project_file = request.FILES["project_file"]
        if not project_file:
            messages.error(request,'File required for creation of project')
        if form.is_valid():
            project_name = request.POST.get('project_name')
            target_feature = request.POST.get('target_feature')
            project_file = request.FILES["project_file"]
            
            try :
                if not project_file.name.endswith('.csv') :
                    messages.error(request, 'File uploaded is not the type CSV')
                else:
                    form_data = Project(user=obj, project_name= project_name,project_file=project_file, target_feature=target_feature )
                    form_data.save()
                    messages.success(request,'Project Created !')
                    return redirect('user_info')
            except Exception as e:
                form = CreateProjectForm(request.POST or None, request.FILES, instance=obj)
                messages.error(request, 'Unable to upload file,' +repr(e))   
        else:
            messages.error(request, 'Failed, Check the file extension')
    else:
        obj = Profile.objects.get(user__id = request.user.id)
        form = CreateProjectForm(request.POST or None, request.FILES, instance=obj)
    
    context = {'form': form, }
    return render(request, 'dashboard/create_project.html', context )

@login_required(login_url='login')
def delete_project(request, pk):
    project = request.user.profile.project_set.get(id=pk)

    if request.method == 'POST':
        print(request.POST)
        project.delete()
        return redirect('user_info')
    return render(request, 'dashboard/delete_project_confirmation.html', context={'project_name':project })




@login_required(login_url='login')
# @cache_page(60*15)
def user_project(request,pk):
    fp = request.user.profile.project_set.get(id=pk).project_file.url
    target_feature = request.user.profile.project_set.get(id=pk).target_feature
    project_name = request.user.profile.project_set.get(id=pk).project_name
    b = str(settings.MEDIA_ROOT).replace('\\','\\')+ str(fp).replace('/','\\').replace('\media', '')
    
    basic_data_details = insights_v2.Report(b, target_feature).basic_data_details()
    null_count_chart = insights_v2.Report(b, target_feature).nullColChart()
    univariate_barchart_dict = insights_v2.Report(b, target_feature).get_unibarChart()
    univariate_violinchart_ls = insights_v2.Report(b,target_feature).get_univiolinChart()
    univariate_histchart_ls = insights_v2.Report(b, target_feature).get_unihistChart()
    bivariate_boxchart_ls = insights_v2.Report(b, target_feature).get_biboxplot()
    scatterchart_ls = insights_v2.Report(b, target_feature).get_scatterplot()

    print(target_feature)
    context = {'project_name':project_name, 'univariate_barchart_dict': univariate_barchart_dict,
                'null_count_chart' : null_count_chart,
                'basic_data_details' : basic_data_details,
                'univariate_violinchart_ls': univariate_violinchart_ls,
                'univariate_histchart_ls':univariate_histchart_ls,
                'bivariate_boxchart_ls':bivariate_boxchart_ls,
                'scatterchart_ls':scatterchart_ls,
                }
    return render(request, 'dashboard/user_project_v2.html',context) 