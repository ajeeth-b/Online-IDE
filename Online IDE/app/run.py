from codex import CodEX

container = CodEX()
print(container.get_available_languages())

res = container.execute('python3', 'print("Hello World")')
print(res)


res = container.execute('c', '''#include <stdio.h>

void main(){
	int a;
	scanf("%d", &a);
	printf("Hello world -   %d", a);
}''', '123')
print(res)

# d = Docker()
# print(d.get_all_language())
# print(d.has_language('python3'))
# print(d.run_container('python3', lang_exec['python3'], '/mnt/g/Python/flask/UnForge-exec/test1/app/codex/test/', '/code'))