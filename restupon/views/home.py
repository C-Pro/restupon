from pyramid.view import view_config

@view_config(route_name='home', renderer='index.html')
def my_view(request):
    return {'project': '.'}
