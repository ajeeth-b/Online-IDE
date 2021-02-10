lang_exec = {
	'python3':{
		'filename':'main.py',
		'image':{'lang-python3'},
		'build_cmd':None,
		'run_cmd': ['python3', 'main.py']
	},

	'c':{
		'filename':'main.c',
		'image':{'lang-c'},
		'build_cmd':['gcc', 'main.c'],
		'run_cmd': []
	}
}