counter = 0

def getNeededRESTpaths():
    from JuMonC.handlers.base import api_version_path
    return [api_version_path + "/CoECSim/counter"]


def registerPath(path):
    from flask import jsonify, make_response
    
    from JuMonC.handlers.base import check_version, RESTAPI
    from JuMonC.authentication import scopes
    from JuMonC.authentication.check import check_auth
    
    
    @RESTAPI.route(path, methods=["GET"])
    @check_version
    @check_auth(scopes["see_links"])
    def plugin_example_counter(version):
        global counter
        
        counter = counter + 1
        return make_response(jsonify({"Visits": counter}), 200)
    