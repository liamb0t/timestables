from flask import url_for
from flask_mail import Message
from bibim import mail
from wtforms.validators import ValidationError

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='noreplay@demo.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('main.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email. 
'''
    mail.send(msg)

def send_verification_email(user):
    token = user.get_verification_token()
    msg = Message('Verifiy Your Account', 
                  sender='bibimhak@demo.com', 
                  recipients=[user.email])
    msg.body = f'''Please visit the following link to verify your email address:
{url_for('main.confirm_email', token=token, _external=True)}

If you did not make this request, then simply ignore this email. 
'''
    mail.send(msg)

def file_max_size(max_size):
    max_bytes = max_size*1024*1024
    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(f"File size must be less than {max_size}MB")
        field.data.seek(0)
    return file_length_check

def total_files_max_size(max_size):
    max_bytes = max_size * 1024 * 1024
    
    def files_total_length_check(form, field):
        total_size = 0
        
        for file in field.data:
            total_size += len(file.read())
            file.seek(0)  # Reset the position of the current file after reading
        
        if total_size > max_bytes:
            raise ValidationError(f"Total size of all files must be less than {max_size}MB")
    
    return files_total_length_check

prompts = [
    "Share a funny or surprising misunderstanding you've had due to language differences.",
    "What's the most interesting Korean food you've tried since moving here?",
    "Describe a memorable experience you've had exploring South Korea outside of teaching.",
    "What's the most surprising thing you've learned about Korean culture?",
    "Share a picture of a beautiful place you've visited in South Korea and tell us why it's special.",
    "What's your favorite Korean word or phrase, and why does it stand out to you?",
    "How have you celebrated a Korean holiday? Share your experiences and photos if you have any.",
    "What K-Pop song is currently stuck in your head?",
    "Describe the most interesting conversation you've had with a local.",
    "Which Korean city or region is your favorite and why?",
    "Have you tried learning any Korean traditional crafts or arts? Share your experiences.",
    "What's your favorite Korean drama or movie and why?",
    "Share a story about a unique transportation experience you've had in South Korea.",
    "Tell us about your favorite local restaurant or café in your city.",
    "Have you picked up any Korean habits or customs since living here?",
    "Describe the quirkiest cultural difference you've encountered in South Korea.",
    "If you could bring one aspect of Korean culture back to your home country, what would it be and why?",
    "Share an experience where you tried traditional Korean clothing (Hanbok).",
    "What Korean technology or gadget have you found most useful or interesting?",
    "Tell us about a Korean festival or event you've attended. What was it like?",
    "Share a recent lesson plan you've used in your classroom and how it went.",
    "Have you tried any new teaching strategies or techniques lately? Tell us about it.",
    "What are some of the biggest challenges you face as an English teacher in Korea?",
    "How do you incorporate Korean culture into your English lessons?",
    "Share a funny or interesting story from your time teaching in Korea.",
    "How do you keep your students motivated to learn English?",
    "What are your favorite resources for teaching English as a foreign language?",
    "Have you attended any professional development workshops or conferences recently? What did you learn?",
    "How do you use technology in your English lessons?",
    "What advice would you give to new English teachers in Korea?"
]
