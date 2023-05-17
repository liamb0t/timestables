import secrets
import os 
from flask import current_app
from bibim import db
from bibim.models import File

def get_file_size(file_path):

    bytes = os.path.getsize(file_path)
    kb = bytes / 1024
    mb = bytes / (1024 * 1024)
    gb = mb / 1024

    return (int(gb), "GB") if mb > 1000 else (int(mb), "MB") if kb > 1000 else (int(kb), "KB")

def save_file(form_file, material):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    fn = random_hex + f_ext
    path = os.path.join(current_app.root_path, 'uploads', fn)
    form_file.save(path)
    upload = File(filename=fn, filepath=path, filetype=f_ext, files_material=material)
    db.session.add(upload)

def get_publishers(level):
    if level == 'elementary':
        return [('0', 'Select a textbook'), ('Daegyo', 'Daegyo'), ('Cheonjae', 'Cheonjae'), ('YBM KIM', 'YBM Kim'), ('YBM Choi', 'YBM Choi'), ('Dong-A', 'Dong-A')]
    elif level == 'middle':
        return [('0', 'Select a textbook'), ('1', 'Dong-A Lee'), ('2', 'Dong-A Kim'), ('3', 'YBM Kim'), ('4', 'YBM Choi'), ('5', 'Dong-A')]
    else:
        return
    
def get_grades(level):
    if level == 'elementary':
        return [('0', 'Select Grade'), ('1', '1st Grade'), ('2', '2nd Grade'), 
                ('3', '3rd Grade'), ('4', '4th Grade'), ('5', '5th Grade'), ('6', '6th Grade')]
    elif level == 'middle':
        return [('0', 'Select a textbook'), ('1', 'Dong-A Lee'), ('2', 'Dong-A Kim'), ('3', 'YBM Kim'), ('4', 'YBM Choi'), ('5', 'Dong-A')]
    else:
        return

textbooks_elem = {
    'Daegyo': {
        '3': {
            "Lesson 1": "Hello, I'm Jinu",
            "Lesson 2": "What's This?",
            "Story Time 1": "",
            "Lesson 3": "Stand Up, Please",
            "Lesson 4": "It's Big",
            "Story Time 2": "",
            "Lesson 5": "How Many Carrots?",
            "Lesson 6": "I Like Chicken",
            "Story Time 3": "",
            "Culture Project 1": "",
            "Lesson 7": "I Have a Pencil",
            "Lesson 8": "I'm Ten Years Old",
            "Story Time 4": "",
            "Lesson 9": "What Color Is It?",
            "Lesson 10": "Can You Skate?",
            "Lesson 11": "It's Snowing",
            "Story Time 5": "",
            "Culture Project 2": ""
        },
        '4': {
            "Lesson 1": "How Are You?",
            "Lesson 2": "This Is My Sister",
            "Story Time 1": "",
            "Lesson 3": "What Time Is It?",
            "Lesson 4": "He Is a Firefighter",
            "Story Time 2": "",
            "Lesson 5": "Is This Your Bag?",
            "Lesson 6": "What Day Is It?",
            "Story 3": "",
            "Culture Project 1": "",
            "Lesson 7": "Let's Play Soccer",
            "Lesson 8": "It's On the Desk",
            "Story Time 4": "",
            "Lesson 9": "Line Up, Please",
            "Lesson 10": "How Much Is It?",
            "Lesson 11": "What Are You Doing?",
            "Story Time 5": "",
            "Culture Project 2": ""
        },
        '5': {
            "Lesson 1": "Where Are You From?",
            "Lesson 2": "Whose Drone Is This?",
            "Lesson 3": "Please Try Some",
            "Story Time 1": "",
            "Lesson 4": "What's Your Favorite Subject?",
            "Lesson 5": "I Get Up At Seven",
            "Lesson 6": "Can I Take a Picture?",
            "Story Time 2": "",
            "Culture Project 1": "",
            "Lesson 7": "What Did You Do During Your Vacation?",
            "Lesson 8": "She Has Long Curly Hair",
            "Lesson 9": "Is Emily There?",
            "Story Time 3": "",
            "Lesson 10": "Where Is the Market?",
            "Lesson 11": "I Want to Be a Photographer",
            "Lesson 12": "I Will Join the Ski Camp",
            "Story Time 4": ""
        },
        '6': {
            "Lesson 1": "What Grade Are You In?",
            "Lesson 2": "Do You Know Anything About Hanok?",
            "Lesson 3": "When Is Earth Day?",
            "Reading Time 1": "",
            "Lesson 4": "How Much Are These Pants?",
            "Lesson 5": "What's Wrong?",
            "Lesson 6": "I'm Going to Go on a Trip",
            "Reading Time 2": "",
            "Culture Project 1": "",
            "Lesson 7": "You Should Wear a Helmet",
            "Lesson 8": "How Can I Get to the Museum?",
            "Lesson 9": "How Often Do You Exercise?",
            "Reading Time 3": "",
            "Lesson 10": "Emily Is Faster Than Yuna",
            "Lesson 11": "Why Are You Happy?",
            "Lesson 12": "Would You Like to Come to My Graduation?",
            "Reading Time 4": "",
            "Culture Project 2": ""
        },
    }
}



textbooks_middle = {
    'DongA Yun': {
        'grade 1': {
            'Lesson 1': 'Heart to Heart',
            'Lesson 2': 'Have Fun at School',
            'Lesson 3': 'Wisdom in Stories',
            'Lesson 4': 'Small Things, Big Differences',
            'Lesson 5': 'Styles Around the World',
            'Lesson 6': 'People at Work',
            'Lesson 7': 'Discover Korea',   
            'Lesson 8': 'Dream Together, Reach Higher',
            'Special Lesson': 'Kitchen Science'
        },
        'grade 2': {
            'Lesson 1': 'My Happy Everyday Life',
            'Lesson 2': 'Enjoying Local Culture',
            'Lesson 3': 'Ideas for Saving the Earth',
            'Lesson 4': 'The Amazing World of Animals',
            'Lesson 5': 'Living Healthily and Safely',
            'Lesson 6': 'Different People, Different Views',
            'Lesson 7': 'Life in Space',
            'Lesson 8': 'Pride of Korea',
            'Special Lesson': 'Creative Ideas in Stories'
        },
        'grade 3': {
            'Lesson 1': 'Follow Your Dream',
            'Lesson 2': 'Food for the Heart',
            'Lesson 3': 'Stories of English Words and Expressions',
            'Lesson 4': 'Be a Smarter Sender',
            'Lesson 5': 'The Team Behind the Team',
            'Lesson 6': 'Stories for All Time',
            'Lesson 7': 'Technology in our Lives',
            'Lesson 8': 'The Joseon Dynasty Through Paintings',
            'Special Lesson': 'Finding the Good in You'
        }
    },
    'DongA Lee': {
        'grade 1': {
            'Lesson 1': 'An Exciting New World',
            'Lesson 2': 'Be Healthy, Be Happy!',
            'Lesson 3': 'How Do I Look?',
            'Lesson 4': 'Catch the Sun',
            'Special Lesson 1': 'Three Bottles, Three Lives',
            'Lesson 5': 'Art for All',
            'Lesson 6': 'Dream High, Fly High!',
            'Lesson 7': "Money Doesn't Grow on Trees",
            'Lesson 8': 'The Way to Korea',
            'Special Lesson 2': "Charlotte's Web"
        },
        'grade 2': {
            'Lesson 1': 'Can We Talk?',
            'Lesson 2': 'Close to You',
            'Lesson 3': 'The Music Goes On',
            'Lesson 4': 'Go For It!',
            'Special Lesson 1': 'Summer on a Stick',
            'Lesson 5': 'Come One, Come All',
            'Lesson 6': 'Into Outer Space',
            'Lesson 7': 'Can I Trust It?',
            'Lesson 8': 'Be Like Sherlock!',
            'Special Lesson 2': 'Frindle'
        },
        'grade 3': {
            'Lesson 1': "I Can't but We Can",
            'Lesson 2': 'Go Green',
            'Lesson 3': 'Heal the World',
            'Lesson 4': 'Open a Book, Open Your Mind',
            'Lesson 5': 'Believe in Yourself',
            'Lesson 6': 'Make the World Beautiful',
            'Lesson 7': 'Feel the Wonder',
            'Lesson 8': 'Up to You',
            'Special Lesson': 'Picture the Future'
        }
    }     
}
    