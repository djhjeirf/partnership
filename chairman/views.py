from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from chairman.models import *


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            #print('In')
        return HttpResponseRedirect('/plots_list')
    else:
        if request.user.is_authenticated():
            is_auth = True
        is_auth = False
        username = request.user.username
        if request.user.is_authenticated():
            is_auth = True
        return render_to_response('login.html', {}, context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def db_page(request):
    return render_to_response('db_tables_list.html', {'username': request.user.username, },
                              context_instance=RequestContext(request))


#######################
#     ADD SECTION     #
#######################


def add_land_category(request):
    land_category = None
    return render_to_response('land_category.html', {'username': request.user.username, 'land_category': land_category},
                              context_instance=RequestContext(request))


def add_use_case(request):
    use_case = None
    return render_to_response('use_case.html', {'username': request.user.username, 'use_case': use_case},
                              context_instance=RequestContext(request))


def add_plot(request):
    plot = None
    lc_list = LandCategory.get_all()
    uc_list = UseCase.get_all()
    o_list = Rightholder.get_all()
    return render_to_response('plot.html', {'username': request.user.username, 'plot': plot, 'lc_list': lc_list,
                                            'uc_list': uc_list, 'o_list': o_list},
                              context_instance=RequestContext(request))


def add_owner(request):
    owner = None
    return render_to_response('owner.html', {'username': request.user.username, 'owner': owner},
                              context_instance=RequestContext(request))


######################
#   CHANGE SECTION   #
######################


def change_land_category(request, id):
    land_category = LandCategory.find(id=id)[0]
    return render_to_response('land_category.html', {'username': request.user.username, 'land_category': land_category},
                              context_instance=RequestContext(request))


def change_use_case(request, id):
    uc = UseCase.find(id=id)[0]
    return render_to_response('use_case.html', {'username': request.user.username, 'use_case': uc},
                              context_instance=RequestContext(request))


def change_plot(request, id):
    plot = LandPlot.find(id=id)[0]
    lc_list = LandCategory.get_all()
    uc_list = UseCase.get_all()
    o_list = Rightholder.get_all()
    plot_to_owners = LandOwnerInformation.find(land_plot=id)
    if plot_to_owners:
        real_owners = []
        for pto in plot_to_owners:
            real_owners.append([Rightholder.find(id=pto.rightholder)[0], pto.document])
    else:
        real_owners = None
    return render_to_response('plot.html', {'username': request.user.username, 'plot': plot, 'lc_list': lc_list,
                                            'uc_list': uc_list, 'o_list': o_list, 'real_owners': real_owners},
                              context_instance=RequestContext(request))


def change_owner(request, id):
    owner = Rightholder.find(id=id)[0]
    return render_to_response('owner.html', {'username': request.user.username, 'owner': owner},
                              context_instance=RequestContext(request))


########################
#    SAVE SECTION     #
#######################


def save_land_category(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id'] != '':
            land_category = LandCategory.find(id=request.POST['id'])[0]
            land_category.set_new_values(**request.POST)
            land_category.save()
        else:
            land_category = LandCategory(**request.POST)
            land_category.save()
        return HttpResponseRedirect('/land_category/' + str(land_category.id))
    return HttpResponseRedirect('/land_categories_list')


def save_use_case(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id'] != '':
            printt(type)
            use_case = UseCase.find(id=request.POST['id'])[0]
            use_case.set_new_values(**request.POST)
            use_case.save()
        else:
            use_case = UseCase(**request.POST)
            use_case.save()
        return HttpResponseRedirect('/use_case/' + str(use_case.id))
    return HttpResponseRedirect('/use_cases_list')


def save_plot(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id'] != '':
            printt(type)
            plot = LandPlot.find(id=request.POST['id'])[0]
            plot.set_new_values(**request.POST)
        else:
            plot = LandPlot(**request.POST)
        plot.land_category = LandCategory.find(name=request.POST['_land_category'])[0].id
        plot.permitted_use = UseCase.find(name=request.POST['_permitted_use'])[0].id
        plot.save()
        owners = request.POST.getlist('owners')
        plot_to_owners = LandOwnerInformation.find(land_plot=plot.id)
        docs = request.POST.getlist('document')
        if plot_to_owners:
            for pto in plot_to_owners:
                pto.delete()
        for i, owner in enumerate(owners):
            owner_id = Rightholder.get_owner_id(owner)
            if owner_id is not None:
                pto = LandOwnerInformation(land_plot=plot.id, rightholder=owner_id, document=docs[i])
                pto.save()
        plot.save()
        return HttpResponseRedirect('/plot/' + str(plot.id))
    return HttpResponseRedirect('/plots_list')


def save_owner(request):
    if request.method == 'POST':
        if 'id' in request.POST and request.POST['id'] != '':
            printt(type)
            owner = Rightholder.find(id=request.POST['id'])[0]
            owner.set_new_values(**request.POST)
            owner.save()
        else:
            owner = Rightholder(**request.POST)
            owner.save()
        return HttpResponseRedirect('/owner/' + str(owner.id))
    return HttpResponseRedirect('/owners_list')


#######################
#   DELETE SECTION    #
#######################


def delete_land_category(request, id):
    lc = LandCategory.find(id=id)[0]
    lc.delete()
    return HttpResponseRedirect('/land_categories_list')


def delete_use_case(request, id):
    uc = UseCase.find(id=id)[0]
    uc.delete()
    return HttpResponseRedirect('/use_cases_list')


def delete_plot(request, id):
    p = LandPlot.find(id=id)[0]
    p.delete()
    return HttpResponseRedirect('/plots_list')


def delete_owner(request, id):
    o = Rightholder.find(id=id)[0]
    o.delete()
    return HttpResponseRedirect('/owners_list/')


#######################
#     LIST SECTION    #
#######################


def list_land_categories(request):
    lc_list = LandCategory.get_all()
    return render_to_response('land_categories_list.html', {'username': request.user.username, 'land_categories': lc_list},
                              context_instance=RequestContext(request))


def list_use_cases(request):
    use_cases = UseCase.get_all()
    return render_to_response('use_cases_list.html', {'username': request.user.username, 'use_cases': use_cases},
                              context_instance=RequestContext(request))


def list_plots(request):
    plots = LandPlot.get_all()
    return render_to_response('plots_list.html', {'username': request.user.username, 'plots': plots},
                              context_instance=RequestContext(request))


def list_owners(request):
    owners = Rightholder.get_all()
    return render_to_response('owners_list.html', {'username': request.user.username, 'owners': owners},
                              context_instance=RequestContext(request))
























