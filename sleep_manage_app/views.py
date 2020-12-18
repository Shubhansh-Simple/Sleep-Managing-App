from django.shortcuts     import render
from django.http          import HttpResponse
from django.views.generic import ListView , DetailView , CreateView , UpdateView
from .models              import Sleep
from .forms               import SleepAdminForm


def hello_function( request ):
    return render( request, 'hello.html', {} )


class SleepCreateView( CreateView ):
    model         = Sleep
    template_name = 'sleep_new.html'
    success_url   = '/admin/'
    form_class    = SleepAdminForm
    #fields        = '__all__'

    def post( self,request,*args,**kwargs ):

        request.POST = request.POST.copy()
        request.POST['arise_at'] = '2001-01-01 ' + request.POST.get('arise_at') 
        request.POST['sleep_at'] = '2001-01-01 ' + request.POST.get('sleep_at')

        form = self.form_class( request.POST )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid( self,form ):
        print('\n\n----------------Form is valid not problem at all---------------- \n\n')

        form_unsave                    = form.save( commit=False )
        form_unsave.user_name = self.request.user
        #form_unsave.save()
        print( 'Form unsave - ',form_unsave, end='\n\n')

        return super( SleepCreateView,self ).form_valid( form )

    def form_invalid( self,form ):
        print( 'form_invalid error name - ',form.errors.as_json() )

        [ print( 'Form invalid data views.py - ',x,' ',y,' ',type(y) ) for x,y in dict(form.data).items()  ]
        #return render_to_response( form )
        error = form.errors.as_ul()
        return HttpResponse('<h1>{}</h1>'.format(error) )





