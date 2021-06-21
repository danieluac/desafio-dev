## Instalação do desafio de  programação

Este desafio usa as seguintes tecnologias:
 - Python: 3.9.5 
   - Framework Django: 3.2.4
 - PostgreSQL: 10
    - psycopg2: 2.9.1 - como drive de conexão ao postgresql
### Passos de Instalação
- Fazer clone deste repositório

  
- Criar o environment ou ambiente virtual do projecto e activa-lo 
    - Use a versão python mencionada acima ou que permita instalar a versão **Django** acima.


- instalar as dependências do projecto em requirements.txt 

    - <code> pip install -r requirements.txt </code>


- Configurar o dados de acesso ao banco de dados no ficheiro especificado a seguir:

  <code>
 - desafio-dev/
   - core/
   - settings.py 
     
---- DATABASES = { 

    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres', // nome do banco de dados a ser usado
            'PASSWORD': 'admin', // senha do usuário a ser usado
            'USER': 'postgres', // nomde do usuario do banco de dados a ser usado 
            'HOST': 'localhost', // host do banco de dados
            'PORT': '5432', // porta de acesso ao banco de dados
    }
}  
    </code>

**Nota: O usuário de banco de dados deve ter todas as permissões necessárias para poder criar /eliminar /actualizar /deletar banco de dados*


- Executar as migrações que vão poder criar as tabelas do banco de dados. Deve ser feito no directório raiz do projecto e com o **environment** activado
    - 1º <code> python manage.py makemigrations </code>
    - 2º <code> python manage.py migrate </code>


- Executar testes automaticos
    - <code> python manage.py test </code>

    
- Executar ou rodar o projecto
    - <code> python manage.py runserver </code>





---    
### Referência

Este projecto foi baseado nas especificações deste desafio: https://github.com/ByCodersTec/desafio-dev
