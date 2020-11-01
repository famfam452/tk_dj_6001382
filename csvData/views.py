from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.urls import reverse
from django.contrib import messages
import io,csv

from . import urls
from .forms import Nameform,FileCSVform
from .method import NaiiveBaye
# Create your views here.
def index(request):
    if request.method == 'POST':
        request_POST = request.POST
        form = Nameform(request_POST)
        if request_POST['your_name'] != '' and form.is_valid():
            file_form = FileCSVform()
            return render(request,'frontend/next.html',{'nameof':form.cleaned_data['your_name'],'fileform':file_form})
    else:
        form = Nameform()
    return render(request,'frontend/index.html',{'form': form})

def csv_upload(request):
    if request.method == 'GET':
        return redirect('index')
    elif request.method == 'POST':
        csv_file = request.FILES['CSV_file']
        if csv_file.name.endswith('.csv'):
            if csv_file.multiple_chunks() != True:
                data_read = csv_file.read().decode('UTF-8-SIG')
            else:
                for realine in csv_file.chunks():
                    data_read = realine.decode('UTF-8-SIG')
            data_set = data_read.splitlines()
            if data_set != [] and len(data_set) > 1:
                attribute = data_set[0]
                set_attr = attribute.split(',')
                for s,setA in enumerate(set_attr):
                    set_attr[s] = setA.strip() 
                row_instance = []
                for row in data_set[1:]:
                    row_split = row.split(',')
                    row_instance.append(row_split)
                context = {'Attribute':set_attr,'DataInstance':row_instance}
                if request.POST['nameOf']:
                    context.update({'nameof':request.POST['nameOf']})
                return render(request,'frontend/table.html',context)
    messages.error(request,"Only CSV file and more than one attribute")
    return redirect('index')

def select_class(request):
    if request.method == 'POST':
        RP = request.POST
        set_attr = RP.getlist('attribute[]')
        i = int(RP['counters'])
        classLabel = RP['classLabel']
        nameof = RP['nameof']
        row_instance = []
        for j in range(0,i):
            y = RP.getlist("instance["+str(j)+"][]")
            row_instance.append(y)
        Nb = NaiiveBaye(set_attr,row_instance)
        context = {'Attribute':set_attr,
        'DataInstance':row_instance,
        'Class':classLabel,
        'NameOf':nameof,
        'Selector':Nb.create_chosen_Dict(classLabel),
        'Attribute2':Nb.create_chosen_attribute(classLabel)}
        return JsonResponse(context,status=200)
    return JsonResponse({'msg':'No'},status=400)

def calculator(request):
    if request.method == 'POST':
        RP = request.POST
        set_attr = RP.getlist('attribute[]')
        i = int(RP['counters'])
        classLabel = RP['classLabel']
        nameof = RP['nameof']
        row_instance = []
        for j in range(0,i):
            y = RP.getlist("instance["+str(j)+"][]")
            row_instance.append(y)
        Nb = NaiiveBaye(set_attr,row_instance)
        input_ = RP.getlist('input[]')
        attribute2 = RP.getlist('attibute2[]')
        instances = {}
        for n,ik in enumerate(input_):
            instances.update({attribute2[n]:ik})
        compair_result = Nb.compair_prob(instances,classLabel)
        best_result = Nb.find_best_result(compair_result)
        context = {
        'Attribute':set_attr,
        'DataInstance':row_instance,
        'Class':classLabel,
        'NameOf':nameof,
        'Selector':Nb.create_chosen_Dict(classLabel),
        'Attribute2':Nb.create_chosen_attribute(classLabel),
        'result_all':compair_result,
        'the_best':best_result
        }
        return JsonResponse(context,status=200)
    return JsonResponse({'msg':'No'},status=400)