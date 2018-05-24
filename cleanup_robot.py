# crontab entry:
# * */4 * * * python cleanup_robot.py <API_KEY>
import girder_client
import sys

gc = girder_client.GirderClient()
gc.authenticate(apiKey=sys.argv[1])
gc.delete('photomorph/expired')
