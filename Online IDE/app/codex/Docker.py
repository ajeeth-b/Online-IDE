from docker import from_env
from docker.errors import APIError

class LanguageNotSupported(Exception):
	pass

class InternalError(Exception):
	pass

class TimeLimitExceeded(Exception):
	pass

class ExecutionError(Exception):
	def __init__(self, output, error):
		self.output = output
		self.error = error

class CodeCompliationError(Exception):
	def __init__(self, output, error):
		self.output = output
		self.error = error

	def __str__(self):
		return "CompliationError : "+ str(self.error)

class CodeRuntimeError(Exception):
	def __init__(self, output, error):
		self.output = output
		self.error = error

	def __str__(self):
		return "RuntimeError : "+ str(self.error)

class Docker:
	client = from_env()

	def __init__(self):
		# self.client = from_env()
		self.languages = self.get_all_language()

	def get_all_language(self):
		return [self._strip_image_name(img.tags[0]) for img in self.client.images.list() if self._is_language_image(img.tags)]

	def _is_language_image(self, tags):
		return tags and tags[0].startswith('lang-')

	def _strip_image_name(self, image):
		image = image.split(':')[0]
		return image.replace("lang-", "")

	def has_language(self, language):
		return language in self.languages

	def get_image_name(self, language):
		return 'lang-'+language

	def run_container(self, lang, lang_exec, src_dir, mountpoint = '/code'):
		if not self.has_language(lang):
			raise LanguageNotSupported("Language not supported")

		image = self.get_image_name(lang)
		volumes = {
			src_dir:{
				'bind':mountpoint, 
				'mode':'rw'
				}
			}
		container = self.client.containers.run(image, 'sleep 300s', volumes=volumes, detach=True)

		container = self._update_container(container)
		if container.status != 'running':
			raise InternalError('Error in starting container')

		try:
			if lang_exec['build_cmd']:
				self._build(container, lang_exec['build_cmd'])
			output = self._exec(container, lang_exec['run_cmd'])
			self._kill_container(container)
			return output
		except Exception as e:
			self._kill_container(container)
			raise e

	def _build(self, container, build_cmd : list):

		try:
			exit_code, output = container.exec_run(['sh', '/script/build.sh'] + build_cmd, demux=True)
		except APIError as e:
			if e.explanation == 'Container '+str(container.id) + ' is not running':
				raise TimeLimitExceeded()
			print(e, e.explanation)
			raise InternalError()
		if exit_code is None:
			raise ExecutionError(output[0], output[1])
		if output[1]:
			raise CodeCompliationError(output[0], output[1])

	def _exec(self, container, run_cmd):

		try:
			exit_code, output = container.exec_run(['sh', '/script/run.sh']+ run_cmd, demux=True)
		except APIError as e:
			if e.explanation == 'Container '+str(container.id) + ' is not running':
				raise TimeLimitExceeded()
			print(e, e.explanation)
			raise InternalError()

		if exit_code is None:
			print('from exec', exit_code)
			raise ExecutionError(output[0], output[1])
		if output[1]:
			raise CodeRuntimeError(output[0], output[1])
		return output

	def _kill_container(self, container):
		container = self._update_container(container)
		if container.status != 'exited':
				container.kill()

	def _update_container(self, container):
		return self.client.containers.get(container.id)
