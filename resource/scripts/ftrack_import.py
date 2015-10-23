import c4d
from c4d import gui
#Welcome to the world of Python
import ftrack_connect_cinema_4d.publish

def main():
    component_id = '80dc2f1e-14a3-4fee-b480-a4a6f66fa60e'
    session = ftrack_connect_cinema_4d.publish._get_api_session()
    component = session.get('Component', component_id)
    version = component['version']
    asset = version['asset']

    versions = session.query('AssetVersion where asset_id is "{}"'.format(asset['id']))
    
    latest_version = None
    for version in versions:
        if not latest_version or version['version'] > latest_version['version']:
            latest_version = version
    
    location = session.pick_location(component)
    file_path = None
    for component in latest_version['components']:
        file_path = location.get_filesystem_path(component)
        break
    
    replace_object(object_id, file_path)
    

if __name__=='__main__':
    main()
