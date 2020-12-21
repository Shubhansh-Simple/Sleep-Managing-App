#from django.shortcuts     import render
from django.http          import HttpResponse
from django.views.generic import ListView , DetailView , CreateView , UpdateView
from .models              import Sleep
from .forms               import SleepAdminForm


class SleepCreateView( CreateView ):
    model         = Sleep
    template_name = 'sleep_new.html'
    success_url   = '/admin/'
    form_class    = SleepAdminForm

    
    def adding_date( self , data ):
        '''Adding dates with the time for datetime conversion.'''

        return '2001-01-01 ' + data 

    def post( self,request,*args,**kwargs ):
        '''Modifying the input data before validation.'''

        request.POST = request.POST.copy()

        print( 'Before modification POST method data - ',request.POST )

        request.POST['arise_at'] = self.adding_date( request.POST.get('arise_at')  )
        request.POST['sleep_at'] = self.adding_date( request.POST.get('sleep_at')  )

        # function variable.
        noon_sleep_at , noon_arise_at = request.POST.get('noon_sleep_at') , request.POST.get('noon_arise_at')

        if noon_sleep_at and noon_arise_at :
            request.POST['noon_sleep_at'] = self.adding_date( noon_sleep_at )
            request.POST['noon_arise_at'] = self.adding_date( noon_arise_at )

        print('------------------------------')
        print( 'After modification POST method data - ',request.POST )

        form = self.form_class( request.POST )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid( self,form ):
        print('\n\n----------------Form is valid not problem at all---------------- \n\n')

        form_unsave           = form.save( commit=False )
        form_unsave.user_name = self.request.user
        print( 'Form unsave - ',vars( form_unsave ), end='\n\n')

        return super( SleepCreateView,self ).form_valid( form )

    def form_invalid( self,form ):
        print( 'form_invalid error name - ',form.errors.as_json() )

        [ print( 'Form invalid data views.py - ',x,' ',y,' ',type(y) ) for x,y in dict(form.data).items()  ]
        #return render_to_response( form )
        error = form.errors.as_ul()
        return HttpResponse('<h1>{}</h1>'.format(error) )


class SleepUpdateView( UpdateView ):
    model = Sleep
    template_name = 'sleep_edit.html'
    success_url   = '/admin/'
    form_class    = SleepAdminForm

    def adding_date( self , data ):
        '''Adding dates with the time for datetime conversion.'''

        return '2001-01-01 ' + data 


    def post( self,request,*args,**kwargs ):
        '''Modify the data as we do earlier'''

        print( 'Update POST method data - ',request.POST )

        request.POST = request.POST.copy()

        request.POST['arise_at'] = self.adding_date( request.POST.get('arise_at')  )
        request.POST['sleep_at'] = self.adding_date( request.POST.get('sleep_at')  )

        # function variable.
        noon_sleep_at , noon_arise_at = request.POST.get('noon_sleep_at') , request.POST.get('noon_arise_at')

        if noon_sleep_at and noon_arise_at :
            request.POST['noon_sleep_at'] = self.adding_date( noon_sleep_at )
            request.POST['noon_arise_at'] = self.adding_date( noon_arise_at )

        form = self.form_class( request.POST )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid( self,form ):
        form_unsave           = form.save( commit=False )
        form_unsave.user_name = self.request.user

        return super( SleepUpdateView,self ).form_valid( form )

    def form_invalid( self,form ):
        print( 'form_invalid error name - ',form.errors.as_json() )

        [ print( 'Form invalid data views.py - ',x,' ',y,' ',type(y) ) for x,y in dict(form.data).items()  ]
        #return render_to_response( form )
        error = form.errors.as_ul()
        return HttpResponse('<h1>{}</h1>'.format(error) )


