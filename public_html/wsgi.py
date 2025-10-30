
import os
import sys
 
activate_this = os.path.expanduser('~/mysite/venv/bin/activate_this.py')
exec(open(activate_this).read(), {'__file__': activate_this})
 
sys.path.insert(1, os.path.expanduser('~/mysite/public_html/'))
 
from django.core.wsgi import get_wsgi_application
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
 
application = get_wsgi_application()


