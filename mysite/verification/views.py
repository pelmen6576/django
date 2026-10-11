from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Person,Questions,Answers
def index(request):

    if request.method=='POST':
        nickname=request.POST.get('nickname')
        password=request.POST.get('password')
        verification=request.POST.get('verification')
        if verification=='зарегаться' and not Person.objects.filter(nickname=nickname) and 0<len(nickname)<=10:
                
            name=request.POST.get('name')
            age=request.POST.get('age')
            if name and age and password:
                Person.objects.create(name=name,age=age,nickname=nickname,password=password)
        elif verification=='войти':
            print('67')
            if Person.objects.all().filter(nickname=nickname, password=password):
                request.session['user_id']=Person.objects.get(nickname=nickname).id
                return redirect('/about')
    return render(request,'index.html')

def about(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    nickname=Person.objects.get(id=request.session['user_id']).nickname
    if request.method=='POST':
        request.session.flush()
        return redirect('/')
    return render(request,'about.html', context={'nickname':nickname , 'questions':Questions.objects.all(),'len':len(Questions.objects.all())})

def create_question(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    nickname=Person.objects.get(id=request.session['user_id']).nickname
    if request.method=='POST':
        create=request.POST.get('create_question')
        if create=='отмена':
            return redirect('/about')
        if create=='отправить':
            question=request.POST.get('question')
            if question!='':

                Questions.objects.create(questions=question,id_persons=Person.objects.get(id=request.session['user_id']),date=timezone.now().date())
                return redirect('/about')

    return render(request,'create_question.html',context={'nickname':nickname})

def view_question(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    nickname=Person.objects.get(id=request.session['user_id']).nickname
    id=request.GET.get('id')
    if request.method=='POST':
        answer=request.POST.get('answer')
        Answers.objects.create(id_questions=Questions.objects.get(id=id),date=timezone.now().date(),id_persons=Person.objects.get(id=request.session['user_id']),answers=answer)
        return redirect(f"/about/question?id={id}")
    answers=Answers.objects.all().filter(id_questions=id)
    return render(request,'view_question.html',context={'nickname':nickname,'i':Questions.objects.get(id=id),'answers':answers,'len':len(answers)})

def my_questions(request):
    nickname=Person.objects.get(id=request.session['user_id']).nickname
    questions=Questions.objects.filter(id_persons=request.session['user_id'])
    return render(request,'about.html',context={'nickname':nickname,'questions':questions,'len':len(questions)})


    