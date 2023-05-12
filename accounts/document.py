from pikepdf import PdfReader

# Load the existing PDF form
template_path = 'static/documents/Rugaaju Wicliff_ Admission0001 _1_.pdf'
pdf_reader = PdfReader(template_path)

# Get the form fields
form_fields = pdf_reader.pages[0].Fields

# Print the form fields
for field_name in form_fields:
    print(field_name)
