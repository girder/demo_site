# crontab entry:
# * */4 * * * python cleanup_robot.py <API_KEY>
import girder_client
import sys

gc = girder_client.GirderClient(apiUrl='https://algorithms.kitware.com/api/v1')
gc.authenticate(apiKey=sys.argv[1])
gc.delete('photomorph/expired')
