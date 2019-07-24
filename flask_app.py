from flask import Flask,Response
from analysis import loadData, showRatingDistribution
data = loadData()
app = Flask(__name__, static_url_path='', static_folder='.')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

@app.route("/vis/<platform>")
def hello(platform):
	df = data.get(platform, None)
	response = ''
	# return "Got the platform type '{}', and rating '{}'.".format(platform,rating)
	if df is not None:
 		response = showRatingDistribution(df[['name','rating']],platform).to_json()

	return Response(response,
 		mimetype = 'application/json',
 		headers = {
 		'Cache-Control': 'no-cache',
	 	'Access-Control-Allow-Origin': '*'
 		}
 	)
if __name__ == '__main__':
	app.run(port=8000)