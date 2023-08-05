import sys
print('__init__')
print('__init__.__name__', __name__)
print('__init__.__package__', __package__)
print('sys.path', sys.path)

def joke():
    print (u'How do you tell HTML from HTML5?'
            u'Try it out in Internet Explorer.'
            u'Does it work?'
            u'No?'
            u'It\'s HTML5.')