# reports-ga
Script para gerar relatórios baseado em reportes mensais do Google Analytics

Criar 3 pastas no /:

* ga-accesses: Pasta com arquivos csv dos acessos extraídos do Google Analytics
* ga-downloads: Pasta com arquivos csv dos downloads extraídos do Google Analytics
* reports: reportes do resultado da junção dos reportes de inputs
* urls: Pasta com arquivos csv com urls a serem consideradas na geração do reporte final. Eles podem ser de dois tipos ** accesses** e **downloads**.
As URLs referentes a Acessos tem que ficar em arquivos com o nome da seguinte forma **accesses-[alguma coisa]**.
As URLs referentes a Downloads(*.pdf, *.zip, etc) tem que ficar em arquivos com o nome da seguinte forma **downloads-[alguma coisa]**.
Para ambos arquivos, o conteúdo do arquivos CSV terá que ter o seguinte formato:

~~~
IdPag,URL
1,/pt-br/noticias
~~~