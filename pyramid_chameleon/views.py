from pyramid.view import view_config

## TODO: Add a demo or delete this...
@view_config(route_name='home', renderer='templates/main.pt')
def my_view(request):
    return {'project': 'pyramid_chameleon',
            'title': "pyramid_chameleon"}
