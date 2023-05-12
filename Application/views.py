import random
import string
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import ContactForm
from .models import *
from .forms import *
from django.contrib import messages
import json
from python_flutterwave import payment

flutterwave_api_secret = '###'
payment.token = flutterwave_api_secret

# Create your views here.
def home(request):
    form = ContactForm(request.POST)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Redirect the user to the qualification selection page
            return redirect('qualification', contact_id=contact.id)
    else:
        form = ContactForm()
    return render(request, 'Application/base.html', {'form': form})


def qualification(request, contact_id):
    
    with open('/home/samtech/Desktop/My_Code/Bugema-Univ/programs.json', 'r') as f:
        data = json.load(f)

        try:
            contact = Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            return redirect('home')

        qualifications = data['qualifications']
        selected_qualification_id = request.GET.get('qualification_id', None)

        if selected_qualification_id is not None:
            selected_qualification_id = int(selected_qualification_id)
            filtered_programs = []

            for school in data['schools']:
                for department in school['departments']:
                    department_programs = []
                    for program in department['programs']:
                       if 'qualification_id' in program and program['qualification_id'] == selected_qualification_id:
                        department_programs.append(program)

                    if department_programs:
                        filtered_programs.append({
                            'department_name': department['name'],
                            'programs': department_programs,
                        })

            # Organize the filtered programs by school and department
            schools = []
            program_data = {}
            for school in data['schools']:
                departments = []
                for program_data in filtered_programs:
                    if program_data['department_name'] in [d['name'] for d in school['departments']]:
                        department = [d for d in school['departments'] if d['name'] == program_data['department_name']][0]
                        departments.append({
                            'name': department['name'],
                            'programs': program_data['programs'],
                        })
                if departments:
                    schools.append({
                        'name': school['name'],
                        'departments': departments,
                    })
                    

        else:
            schools = []
            program_data = []

        # Render the template with the organized programs
        context = {
            'contact': contact,
            'schools': schools,
            'qualifications': qualifications,
            'selected_qualification_id': selected_qualification_id,
            'programs': program_data
        }
        return render(request, 'Application/qualification.html', context)


def application(request, contact_id, program_id):
    with open('/home/samtech/Desktop/My_Code/Bugema-Univ/programs.json', 'r') as f:
        data = json.load(f)
        program = None
        try:
            print(f"Contact ID: {contact_id}, Program ID: {program_id}")
            contact = Contact.objects.get(id=contact_id)
            program = Programs.objects.get(id=program_id)
            # program_id = program.id
            # program.save()
            print(f"Contact: {contact}, Program: {program}")
        except (Contact.DoesNotExist, Programs.DoesNotExist):
            #return redirect('qualification')
            print(program)
        
        print(reverse('application', args=[contact_id, program_id]))

        phone_number = contact.phone_number
        email = contact.email

        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                document = form.cleaned_data.get('document')
                # Check if file field is empty
                if not document:
                    form.add_error('document', 'Please select a file.')
                else:
                    tx_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                    
                    # Create a payment request with Flutterwave API
                    response = payment.initiate_payment(tx_ref, amount=50000, customer_email=email, redirect_url='success_url', payment_options='mobilemoneyuganda', customer_phone_number=phone_number, currency='UGX', description='Bugema University Application Fee')
                    print(response)
                    
                    if response[1]['status'] == 'success':
                        Application.objects.create(
                            contact=contact, 
                            program=program, 
                            # program_id = program_id,
                            document=document,
                            name=contact.name,
                            email=contact.email,
                            phone_number=contact.phone_number,
                          
                        )
                        # Render a success message
                        messages.success(request, 'Your application has been submitted.')

                        
                        return redirect(response[1]['data']['link'])
                    
                    else:
                        # Render an error message if payment was not successful
                        messages.error(request, 'There was an error processing your payment. Please try again later.')
                        return redirect('home')
        else:
            form = DocumentForm()

    return render(request, 'Application/application.html', {'form': form, 'contact': contact, 'program': program})

# def application_success(request, contact_id, program_id):
#     transaction_id = request.session.get('trans_id')
#     response = payment.get_payment_details(transaction_id)
    
#     if response['status'] == 'success':
#         print(response)
#         contact = Contact.objects.get(id=contact_id)
#         document = request.FILES.get('document')
#         program = Programs.objects.get(id=int(program_id))
        
#         Application.objects.create(
#             contact=contact, 
#             program=program, 
#             document=document,
#             name=contact.name,
#             email=contact.email,
#             phone_number=contact.phone_number,
#             approved=False,
#         )
        
#         # Render a success message
#         messages.success(request, 'Your application has been submitted.')
#     else:
#         # Render an error message if payment was not successful
#         messages.error(request, 'Please try again later.')
    
#     success_url = reverse('application_success') + f'?contact_id={contact_id}&program_id={program_id}&application_id={application.id}'
#     return redirect(success_url)


