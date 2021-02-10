from flask import Flask, jsonify, request, render_template
from .codex import CodEX
from flask_cors import CORS


def create_app():
	app = Flask(__name__)
	CORS(app)

	codex = CodEX()

	@app.route('/')
	def get_all_languages():
		return jsonify({'languages':codex.get_available_languages()})

	@app.route('/<language>', methods=['POST'])
	def execute(language):
		try:
			if language not in codex.get_available_languages():
				resp = jsonify({'status':'error','error':'Language not available'})

			if 'code' not in request.json:
				resp = jsonify({'status':'error','error':'requires code to execute'})

			inputs = request.json.get('input','')

			status, output = codex.execute(language, request.json['code'], inputs)
			if status == 'success':
				data = {
					'status':'success',
					'stdout': output['output'][0],
					'stderr': output['output'][1]
				}

			elif status == 'compilation':
				data = {
					'status':'compilation error',
					'stdout': output['output'],
					'stderr': output['error']
				}
			elif status == 'runtime':
				data = {
					'status':'runtime error',
					'stdout': output['output'],
					'stderr': output['error']
				}
			elif status == 'internal':
				data = {
					'status':'internal error'
				}
				print(output)

			resp = jsonify(data)
		except Exception as e:
			print(e)
			resp = jsonify({'status':'internal error'})
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp

	@app.route('/ide')
	def ide():
		return render_template('ide.html')

	return app