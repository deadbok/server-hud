'''
:since: 01/08/2015
:author: oblivion
'''
from socket import getfqdn

from flask import current_app
from flask import render_template


def index():
    '''
    Render the template for the dash board.
    '''
    current_app.logger.debug("Rendering HUD template.")
    return render_template('index.html', hostname=getfqdn())
