from __future__ import division
from ast import If
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,FileResponse, JsonResponse
from django.http import Http404
from django.contrib import messages

from .models import *
from django.contrib.sessions.models import Session
from datetime import timezone, datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
#from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator

from django.conf import settings
import os

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string

# from wsgiref.util import FileWrapper
# from django.db.models import Sum
# from django.db.models import Avg
# from django.db.models import Count
from django.db.models import Max
from django.db.models import Min
# from django.db.models.functions import Round,Cast
from django.db.models.query_utils import Q
from django.db.models import Q,F

from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

import xlwt

import uuid #unique id

import datetime #as dt
import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.views.generic.base import TemplateView
from django.views.generic import View

# @login_required
def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user =authenticate(username=username, password=password)
        if user is not None:
            request.session['logedin']=True
            request.session['username']=username
            request.session['authorities']=user.authorities
            login(request,user)
            return redirect("home")
        else:
            failed='Invalid username or password !!!'
            error={
                'failed':failed,'username':username,
            }
            return render(request,'index.html',error)

    else:
        return render(request,'index.html')

def logout(request):
    if request.session.has_key('username'):
        username=request.session['username']
        request.session.flush()
        logout(request)
        logged="your now inactive please login again"
        return render(request,'index.html',{'logged':logged})
    else:
        request.session.flush()
        return redirect('index')

 

def home(request):
    if request.session.has_key('username'):
        username=request.session['username']
        authorities=request.session['authorities']
        if authorities=='student':
           student = Mockexam.objects.filter(username_id=username).first()
           return render(request,'student/index.html',{'student':student,})
        elif authorities=='staff' or 'admin':
            results=Mockexam.objects.all()
            accounts=Person.objects.filter(authorities='student')
            return render(request,'staff/index.html',{'results':results,'accounts':accounts})
            
        else:
            messages.success(request,'You are authenticated as '+str(username)+', but you are not authorized to access this page. Please contact 0623240200 | 0715672276 (K1 OFFICE) ')
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 
  

def upload(request):
    if request.session.has_key('username'):
        username=request.session['username']
        authorities=request.session['authorities']
        if authorities=='admin':
            if(request.method=='POST'):
                if  request.FILES['myfile'] :
                    dpcheck=request.FILES['myfile']
                    excelfileupload = request.FILES['myfile']
                        
                    i=0
                    j=0
                    l=[]
                    if not dpcheck.name.endswith('xlsx'):
                        messages.warning(request,'upload excel file!!,  (xlsx) that end with .xlsx')
                        return render(request,'staffs/upload.html')
                    else:

                        fs = FileSystemStorage('media/'+str(datetime.datetime.now().strftime('%Y')))
                        filename = fs.save(excelfileupload.name, excelfileupload)
                        marksexcel="media/"+str(datetime.datetime.now().strftime('%Y'))+"/"+filename
                        excelheadler = pd.read_excel(marksexcel)
                        dbframe = excelheadler
                        password ='mtc123456'
                        for dbframe in dbframe.itertuples():
                            if Person.objects.filter(username=str(dbframe.adnumber)).exists():
                                j=j+1
                                l.append(dbframe.adnumber)
                            else:
                                ma =Person.objects.create_user(password=password,username=str(dbframe.adnumber),fullname=str(dbframe.fullname),
                                option=str(dbframe.option),sex=str(dbframe.sex),authorities='student')
                                ma.save()
                                i=i+1
                        messages.warning(request,str(i)+' successifully Uploaded')
           
                        return render(request,'staff/upload.html',{'l':l,'j':j,'i':i})
            else:

                return render(request,'staff/upload.html')
        else:
            messages.success(request,'You are authenticated as '+str(username)+', but you are not authorized to access this page. Please contact 0623240200 | 0715672276 (K1 OFFICE)')
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 


def marks(request):
    if request.session.has_key('username'):
        username=request.session['username']
        authorities=request.session['authorities']
        if authorities=='admin':
            if(request.method=='POST'):
                if  request.FILES['myfile'] :
                    dpcheck=request.FILES['myfile']
                    excelfileupload = request.FILES['myfile']
                        
                    i=0
                    j=0
                    l=[]
                    if not dpcheck.name.endswith('xlsx'):
                        messages.warning(request,'upload excel file!!,  (xlsx) that end with .xlsx')
                        return render(request,'staffs/marks.html')
                    else:

                        fs = FileSystemStorage('media/marks/'+str(datetime.datetime.now().strftime('%Y')))
                        filename = fs.save(excelfileupload.name, excelfileupload)
                        marksexcel="media/marks/"+str(datetime.datetime.now().strftime('%Y'))+"/"+filename
                        excelheadler = pd.read_excel(marksexcel)
                        dbframe = excelheadler
                         
                        for dbframe in dbframe.itertuples():
                            if Mockexam.objects.filter(username_id=str(dbframe.adnumber)).exists():
                                j=j+1
                                l.append(dbframe.adnumber)
                            else:
                                ma =Mockexam(username_id=str(dbframe.adnumber),subject={'COMP':str(dbframe.COMP),'MATH':str(dbframe.MATH),'EDU':str(dbframe.EDU),'GS':str(dbframe.GS)},
                                grade={'COG':str(dbframe.COG),'MG':str(dbframe.MG),'EG':str(dbframe.EG),'GSG':str(dbframe.GSG)},
                                point=9, division=str(dbframe.DIV))
                                ma.save()
                                i=i+1
                        messages.warning(request,str(i)+' successifully Uploaded')
           
                        return render(request,'staff/marks.html',{'l':l,'j':j,'i':i})
            else:
                return render(request,'staff/marks.html')
        else:
            messages.success(request,'You are authenticated as '+str(username)+', but you are not authorized to access this page. Please contact 0623240200 | 0715672276 (K1 OFFICE)')
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
  


def bestandpoorupload(request):
    if request.session.has_key('username'):
        username=request.session['username']
        authorities=request.session['authorities']
        if authorities=='admin' :
            if(request.method=='POST'):
                if  request.FILES['myfile'] :
                    dpcheck=request.FILES['myfile']
                    excelfileupload = request.FILES['myfile']  
                    i=0
                    j=0
                    l=[]
                    if not dpcheck.name.endswith('xlsx'):
                        messages.warning(request,'upload excel file!!,  (xlsx) that end with .xlsx')
                        return render(request,'staffs/upload.html')
                    else:

                        fs = FileSystemStorage('media/bestpoor/'+str(datetime.datetime.now().strftime('%Y')))
                        filename = fs.save(excelfileupload.name, excelfileupload)
                        marksexcel="media/bestpoor/"+str(datetime.datetime.now().strftime('%Y'))+"/"+filename
                        excelheadler = pd.read_excel(marksexcel)
                        dbframe = excelheadler
                        
                        for dbframe in dbframe.itertuples():
                            if BestandPoor.objects.filter(username=str(dbframe.ADNUMBER)).exists():
                                j=j+1
                                l.append(dbframe.ADNUMBER)
                            else:
                            
                                if dbframe.OPTION=='CBE':
                                    ma =BestandPoor(username=str(dbframe.ADNUMBER),fullname=str(dbframe.FULLNAME),
                                    option=str(dbframe.OPTION),sex=str(dbframe.SEX),chem=dbframe.CHEM,bio=dbframe.BIO,
                                    edu=dbframe.EDU,bam=dbframe.BAM,gs=dbframe.GS)
                                    ma.save()
                                    i=i+1
                                elif dbframe.OPTION=='CME':
                                    ma =BestandPoor(username=str(dbframe.ADNUMBER),fullname=str(dbframe.FULLNAME),
                                    option=str(dbframe.OPTION),sex=str(dbframe.SEX),chem=dbframe.CHEM,
                                    math=dbframe.MATH,edu=dbframe.EDU,gs=dbframe.GS)
                                    ma.save()
                                    i=i+1  
                                elif dbframe.OPTION=='PME':
                                    ma =BestandPoor(username=str(dbframe.ADNUMBER),fullname=str(dbframe.FULLNAME),
                                    option=str(dbframe.OPTION),sex=str(dbframe.SEX),phy=dbframe.PHY,
                                    math=dbframe.MATH,edu=dbframe.EDU,gs=dbframe.GS)
                                    ma.save()
                                    i=i+1    
                                elif dbframe.OPTION=='PBE':
                                    ma =BestandPoor(username=str(dbframe.ADNUMBER),fullname=str(dbframe.FULLNAME),
                                    option=str(dbframe.OPTION),sex=str(dbframe.SEX),phy=dbframe.PHY,bio=dbframe.BIO,
                                    edu=dbframe.EDU,bam=dbframe.BAM,gs=dbframe.GS)
                                    ma.save()
                                    i=i+1    
                                elif dbframe.OPTION=='PCE':
                                    ma =BestandPoor(username=str(dbframe.ADNUMBER),fullname=str(dbframe.FULLNAME),
                                    option=str(dbframe.OPTION),sex=str(dbframe.SEX),phy=dbframe.PHY,chem=dbframe.CHEM,
                                    edu=dbframe.EDU,bam=dbframe.BAM,gs=dbframe.GS)
                                    ma.save()
                                    i=i+1     
                                elif dbframe.OPTION=='MCE':
                                    ma =BestandPoor(username=str(dbframe.ADNUMBER),fullname=str(dbframe.FULLNAME),
                                    option=str(dbframe.OPTION),sex=str(dbframe.SEX),
                                    math=dbframe.MATH,edu=dbframe.EDU,comp=dbframe.COMP,gs=dbframe.GS)
                                    ma.save()
                                    i=i+1         
                        messages.warning(request,str(i)+' successifully Uploaded')
           
                        return render(request,'staff/bestandpoorupload.html',{'l':l,'j':j,'i':i})
            else:
                
                return render(request,'staff/bestandpoorupload.html')
        else:
            messages.success(request,'You are authenticated as '+str(username)+', but you are not authorized to access this page. Please contact 0623240200 | 0715672276 (K1 OFFICE)')
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 


def results(request):
    if request.session.has_key('username'):
        username=request.session['username']
        authorities=request.session['authorities']
        if authorities=='admin' or authorities=='staff':
            
            malelist=Person.objects.values_list('username', flat=True)
            getmalelist=list(malelist)
            male=Person.objects.filter(sex='M',authorities='student',username__in=getmalelist)
            mdata=Mockexam.objects.filter(username_id__in=male)
            mone=Mockexam.objects.filter(username_id__in=male,point__in=[3,4,5,6,7,8,9])
            mtwo=Mockexam.objects.filter(username_id__in=male,point__in=[10,11,12])
            mthree=Mockexam.objects.filter(username_id__in=male,point__in=[13,14,15,16,17])
            mfour=Mockexam.objects.filter(username_id__in=male,point__in=[18,19])
            mzero=Mockexam.objects.filter(username_id__in=male,point__in=[20,21])
           
            femalelist=Person.objects.values_list('username', flat=True)
            getfemalelist=list(femalelist)
            female=Person.objects.filter(sex='F',authorities='student',username__in=getfemalelist)
            fdata=Mockexam.objects.filter(username_id__in=female)
            fone=Mockexam.objects.filter(username_id__in=female,point__in=[3,4,5,6,7,8,9])
            ftwo=Mockexam.objects.filter(username_id__in=female,point__in=[10,11,12])
            fthree=Mockexam.objects.filter(username_id__in=female,point__in=[13,14,15,16,17])
            ffour=Mockexam.objects.filter(username_id__in=female,point__in=[18,19])
            fzero=Mockexam.objects.filter(username_id__in=female,point__in=[20,21])

            tone=fone.count()+mone.count()   
            ttwo=ftwo.count()+mtwo.count()
            tthree=fthree.count()+mthree.count()
            tfour=ffour.count()+mfour.count()
            tzero=fzero.count()+mzero.count() 
            tmale=mone.count()+mtwo.count()+mthree.count()+mfour.count()+mzero.count()
            tfemale=fone.count()+ftwo.count()+fthree.count()+ffour.count()+fzero.count()
            tall= tmale+tfemale
            maphy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="A").count()
            mbphy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="B").count()
            mcphy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="C").count()
            mdphy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="D").count()
            mephy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="E").count()
            msphy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="S").count()
            mfphy=Mockexam.objects.filter(username_id__in=male,grade__PG__iexact="F").count() 
            faphy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="A").count()
            fbphy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="B").count()
            fcphy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="C").count()
            fdphy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="D").count()
            fephy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="E").count()
            fsphy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="S").count()
            ffphy=Mockexam.objects.filter(username_id__in=female,grade__PG__iexact="F").count() 
            #end of phys
            machem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="A").count()
            mbchem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="B").count()
            mcchem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="C").count()
            mdchem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="D").count()
            mechem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="E").count()
            mschem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="S").count()
            mfchem=Mockexam.objects.filter(username_id__in=male,grade__CG__iexact="F").count() 
            fachem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="A").count()
            fbchem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="B").count()
            fcchem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="C").count()
            fdchem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="D").count()
            fechem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="E").count()
            fschem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="S").count()
            ffchem=Mockexam.objects.filter(username_id__in=female,grade__CG__iexact="F").count()
            #endof chemistry
            mabio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="A").count()
            mbbio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="B").count()
            mcbio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="C").count()
            mdbio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="D").count()
            mebio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="E").count()
            msbio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="S").count()
            mfbio=Mockexam.objects.filter(username_id__in=male,grade__BG__iexact="F").count() 
            fabio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="A").count()
            fbbio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="B").count()
            fcbio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="C").count()
            fdbio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="D").count()
            febio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="E").count()
            fsbio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="S").count()
            ffbio=Mockexam.objects.filter(username_id__in=female,grade__BG__iexact="F").count()
            #endof BIOLOGY
            mamath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="A").count()
            mbmath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="B").count()
            mcmath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="C").count()
            mdmath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="D").count()
            memath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="E").count()
            msmath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="S").count()
            mfmath=Mockexam.objects.filter(username_id__in=male,grade__MG__iexact="F").count() 
            famath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="A").count()
            fbmath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="B").count()
            fcmath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="C").count()
            fdmath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="D").count()
            femath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="E").count()
            fsmath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="S").count()
            ffmath=Mockexam.objects.filter(username_id__in=female,grade__MG__iexact="F").count()
            #endof MATHEMATICS
            maedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="A").count()
            mbedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="B").count()
            mcedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="C").count()
            mdedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="D").count()
            meedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="E").count()
            msedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="S").count()
            mfedu=Mockexam.objects.filter(username_id__in=male,grade__EG__iexact="F").count() 
            faedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="A").count()
            fbedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="B").count()
            fcedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="C").count()
            fdedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="D").count()
            feedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="E").count()
            fsedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="S").count()
            ffedu=Mockexam.objects.filter(username_id__in=female,grade__EG__iexact="F").count()
            #endof EDUCATION
            mags=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="A").count()
            mbgs=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="B").count()
            mcgs=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="C").count()
            mdgs=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="D").count()
            megs=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="E").count()
            msgs=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="S").count()
            mfgs=Mockexam.objects.filter(username_id__in=male,grade__GSG__iexact="F").count() 
            fags=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="A").count()
            fbgs=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="B").count()
            fcgs=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="C").count()
            fdgs=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="D").count()
            fegs=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="E").count()
            fsgs=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="S").count()
            ffgs=Mockexam.objects.filter(username_id__in=female,grade__GSG__iexact="F").count()
            #endof EGENERAL STUDY
            mabam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="A").count()
            mbbam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="B").count()
            mcbam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="C").count()
            mdbam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="D").count()
            mebam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="E").count()
            msbam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="S").count()
            mfbam=Mockexam.objects.filter(username_id__in=male,grade__BAG__iexact="F").count() 
            fabam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="A").count()
            fbbam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="B").count()
            fcbam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="C").count()
            fdbam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="D").count()
            febam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="E").count()
            fsbam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="S").count()
            ffbam=Mockexam.objects.filter(username_id__in=female,grade__BAG__iexact="F").count()
            #endof EGENERAL STUDY 

            macomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="A").count()
            mbcomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="B").count()
            mccomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="C").count()
            mdcomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="D").count()
            mecomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="E").count()
            mscomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="S").count()
            mfcomp=Mockexam.objects.filter(username_id__in=male,grade__COG__iexact="F").count() 
            facomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="A").count()
            fbcomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="B").count()
            fccomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="C").count()
            fdcomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="D").count()
            fecomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="E").count()
            fscomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="S").count()
            ffcomp=Mockexam.objects.filter(username_id__in=female,grade__COG__iexact="F").count()
            #endof EGENERAL STUDY
            
            mambo={'mone':mone.count(),'mtwo':mtwo.count(),'mthree':mthree.count(),'mfour':mfour.count(),'mzero':mzero.count(),
                'fone':fone.count(),'ftwo':ftwo.count(),'fthree':fthree.count(),'ffour':ffour.count(),'fzero':fzero.count(),
                'tone':tone,'ttwo':ttwo,'tthree':tthree,'tfour':tfour,'tzero':tzero,'tall':tall,'tmale':tmale,'tfemale':tfemale,
                # 'mdata':mdata,'fdata':fdata,'male':male,'female':female,
                'maphy':maphy,'mbphy':mbphy,'mcphy':mcphy,'mdphy':mdphy,'mephy':mephy,'msphy':msphy,'mfphy':mfphy,  'faphy':faphy,'fbphy':fbphy,'fcphy':fcphy,'fdphy':fdphy,'fephy':fephy,'fsphy':fsphy,'ffphy':ffphy,
                'machem':machem,'mbchem':mbchem,'mcchem':mcchem,'mdchem':mdchem,'mechem':mechem,'mschem':mschem,'mfchem':mfchem,  'fachem':fachem,'fbchem':fbchem,'fcchem':fcchem,'fdchem':fdchem,'fechem':fechem,'fschem':fschem,'ffchem':ffchem,
                'mabio':mabio,'mbbio':mbbio,'mcbio':mcbio,'mdbio':mdbio,'mebio':mebio,'msbio':msbio,'mfbio':mfbio,  'fabio':fabio,'fbbio':fbbio,'fcbio':fcbio,'fdbio':fdbio,'febio':febio,'fsbio':fsbio,'ffbio':ffbio,
                'mamath':mamath,'mbmath':mbmath,'mcmath':mcmath,'mdmath':mdmath,'memath':memath,'msmath':msmath,'mfmath':mfmath,   'famath':famath,'fbmath':fbmath,'fcmath':fcmath,'fdmath':fdmath,'femath':femath,'fsmath':fsmath,'ffmath':ffmath,
                'maedu':maedu,'mbedu':mbedu,'mcedu':mcedu,'mdedu':mdedu,'meedu':meedu,'msedu':msedu,'mfedu':mfedu,   'faedu':faedu,'fbedu':fbedu,'fcedu':fcedu,'fdedu':fdedu,'feedu':feedu,'fsedu':fsedu,'ffedu':ffedu,
                'mags':mags,'mbgs':mbgs,'mcgs':mcgs,'mdgs':mdgs,'megs':megs,'msgs':msgs,'mfgs':mfgs,             'fags':fags,'fbgs':fbgs,'fcgs':fcgs,'fdgs':fdgs,'fegs':fegs,'fsgs':fsgs,'ffgs':ffgs,
                'mabam':mabam,'mbbam':mbbam,'mcbam':mcbam,'mdbam':mdbam,'mebam':mebam,'msbam':msbam,'mfbam':mfbam,   'fabam':fabam,'fbbam':fbbam,'fcbam':fcbam,'fdbam':fdbam,'febam':febam,'fsbam':fsbam,'ffbam':ffbam,
                'macomp':macomp,'mbcomp':mbcomp,'mccomp':mccomp,'mdcomp':mdcomp,'mecomp':mecomp,'mscomp':mscomp,'mfcomp':mfcomp,   'facomp':facomp,'fbcomp':fbcomp,'fccomp':fccomp,'fdcomp':fdcomp,'fecomp':fecomp,'fscomp':fscomp,'ffcomp':ffcomp,
                }
                
            return render(request,'staff/results.html',mambo)
        else:
            messages.success(request,'You are authenticated as '+str(username)+', but you are not authorized to access this page. Please contact 0623240200 | 0715672276 (K1 OFFICE)')
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    

def bestandpoor(request):
    if request.session.has_key('username'):
        username=request.session['username']
        authorities=request.session['authorities']
        if authorities=='staff' or 'admin':
            accountsall=Person.objects.filter(authorities='student')
            resultsschoolwise=Mockexam.objects.all().order_by('point')[0:10]
            student=Mockexam.objects.values_list('username_id',flat=True).order_by('point')[0:10]
            studentlist=list(student)
            accounts=Person.objects.filter(authorities='student',username__in=studentlist)

            resultsschoolwisepoor=Mockexam.objects.all().order_by('point').reverse()[0:11]
            studentpoor=Mockexam.objects.values_list('username_id',flat=True).order_by('point').reverse()[0:11]
            studentlistpoor=list(studentpoor)
            accountspoor=Person.objects.filter(authorities='student',username__in=studentlistpoor)
            
            #start of phy
            bestphy=BestandPoor.objects.filter(phy__isnull=False).order_by('phy').reverse()[:8]
            poorphy=BestandPoor.objects.filter(phy__isnull=False).order_by('phy')[:10]
            #start of chem
            bestchem=BestandPoor.objects.filter(chem__isnull=False).order_by('chem').reverse()[:6]
            poorchem=BestandPoor.objects.filter(chem__isnull=False).order_by('chem')[:10]
            #start of bio
            bestbio=BestandPoor.objects.filter(bio__isnull=False).order_by('bio').reverse()[:6]
            poorbio=BestandPoor.objects.filter(bio__isnull=False).order_by('bio')[:10]
            #start of math
            bestmath=BestandPoor.objects.filter(math__isnull=False).order_by('math').reverse()[:8]
            poormath=BestandPoor.objects.filter(math__isnull=False).order_by('math')[:10]
            #start of edu
            bestedu=BestandPoor.objects.filter(edu__isnull=False).order_by('edu').reverse()[:10]
            pooredu=BestandPoor.objects.filter(edu__isnull=False).order_by('edu')[:10]
            #start of bam
            bestbam=BestandPoor.objects.filter(bam__isnull=False).order_by('bam').reverse()[:1]
            poorbam=BestandPoor.objects.filter(bam__isnull=False).order_by('bam')[:10]
            #start of comp
            bestcomp=BestandPoor.objects.filter(comp__isnull=False).order_by('comp').reverse()[:1]
            poorcomp=BestandPoor.objects.filter(comp__isnull=False).order_by('comp')[:7]
            #start of gs
            bestgs=BestandPoor.objects.filter(gs__isnull=False).order_by('gs').reverse()[:2]
            poorgs=BestandPoor.objects.filter(gs__isnull=False).order_by('gs')[:10]
            data={'resultsschoolwise':resultsschoolwise,'accounts':accounts,
            'resultsschoolwisepoor':resultsschoolwisepoor,'accountspoor':accountspoor,
           'bestphy':bestphy,'poorphy':poorphy,'bestchem':bestchem,'poorchem':poorchem,'bestbio':bestbio,'poorbio':poorbio,
           'bestmath':bestmath,'poormath':poormath,'bestedu':bestedu,'pooredu':pooredu,'bestcomp':bestcomp,'poorcomp':poorcomp,
          'bestbam':bestbam,'poorbam':poorbam,'bestgs':bestgs,'poorgs':poorgs,
            }
            return render(request,'staff/bestandpoor.html',data)
            
        else:
            messages.success(request,'You are authenticated as '+str(username)+', but you are not authorized to access this page. Please contact 0623240200 | 0715672276 (K1 OFFICE)')
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 
