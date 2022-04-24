from flask import render_template
from flask import request
from flask import Flask

app = Flask(__name__)


class LengthException(Exception):
    def __init__(self):
        self.text = 'One or more names is too long'


class SymbolException(Exception):
    def __init__(self):
        self.text = 'One or more symbols are incorrect'


def making_list(names):
    """Making the list of names from the string with names"""
    list_of_names = []
    name = ''
    for x in names:
        if x == ',':
            list_of_names.append(name)
            name = ''
        else:
            name += x
    list_of_names.append(name)
    return list_of_names


def validator(names):
    """Validity check"""
    for name in names:
        if len(name) > 10:
            raise LengthException
        if not name.isalpha():
            raise SymbolException


def making_data(list_of_names):
    """Make good-looking data in a bad-looking function"""
    if len(list_of_names) == 0:
        response = ' Никто не лайкнул это'
    elif len(list_of_names) == 1:
        response = list_of_names[0]
        if list_of_names[0][-1] == 'а' or list_of_names[0][-1] == 'я':
            response += ' лайкнула это'
        else:
            response += ' лайкнул это'
    elif len(list_of_names) == 2:
        response = list_of_names[0] + ' и ' + list_of_names[1] + ' лайкнули это'
    elif len(list_of_names) == 3:
        response = list_of_names[0] + ', ' + list_of_names[1] + \
                   ' и ' + list_of_names[2] + ' лайкнули это'
    elif len(list_of_names) <= 6:
        response = list_of_names[0] + ', ' + list_of_names[1] + \
                   f' и ещё {len(list_of_names) - 2} человека лайкнули это'
    else:
        response = list_of_names[0] + ', ' + list_of_names[1] + \
                   f' и ещё {len(list_of_names) - 2} человек лайкнули это'
    return response


def making_response(data=None, error=False, error_message=None):
    """Making the final response to return it to the user"""
    return render_template('likes.html', data=data, error=error, error_message=error_message)


@app.route('/likes')
def likes():
    """The main function of this program. Accept names of users, which liked something and print a formatted response"""
    try:
        names = request.args.get('names')
        list_of_names = making_list(names)
        if len(names) == 0:
            list_of_names = []
        validator(list_of_names)
        data = making_data(list_of_names)
        return making_response(data)

    except (LengthException, SymbolException) as E:
        return making_response(error=True, error_message=E.text)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
