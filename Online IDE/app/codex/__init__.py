from .Docker import Docker, LanguageNotSupported, TimeLimitExceeded, CodeCompliationError, CodeRuntimeError, InternalError, ExecutionError
from uuid import uuid4
from .settings import BASE_MOUNTPOINT
from os import path, mkdir
from .utils import lang_exec
from shutil import rmtree

class CodEX:
	docker = Docker()
	def __init__(self):
		self.languages = self.docker.get_all_language()

	def get_available_languages(self):
		return self.languages

	def execute(self, language, code, inputs=''):
		if language not in self.languages:
			return (-1, 'Language not supported')

		lang_utils = lang_exec[language]

		folder_name = str(uuid4())
		folder = path.join(BASE_MOUNTPOINT, folder_name)
		mkdir(folder)

		code_file = path.join(folder, lang_utils['filename'])
		self._write_file_content(code_file, code)

		input_file = path.join(folder, 'inp.txt')
		self._write_file_content(input_file, inputs)

		try:
			output = ('success', {'output':self.docker.run_container(language, lang_utils, folder)})
			rmtree(folder)
			return output
		except CodeCompliationError as e:
			print(e)
			print(e.error)
			print(e.output)
			rmtree(folder)
			return ('compilation', {'output':e.output, 'error':e.error})
		except CodeRuntimeError as e:
			print(e)
			print(e.error)
			print(e.output)
			rmtree(folder)
			return ('runtime', {'output':e.output, 'error':e.error})
		except Exception as e:
			rmtree(folder)
			return ('internal', {'error':e})

	def _write_file_content(self, file_path, content):
		with open(file_path, 'w') as f:
			f.write(content)

