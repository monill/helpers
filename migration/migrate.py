import os
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError
from inflect import engine as inflect_engine


def read_settings(file_path):
    """ Lê as configurações do arquivo settings.txt """
    settings = {}
    if not os.path.exists(file_path):
        print(f"Erro: O arquivo {file_path} não foi encontrado.")
        sys.exit(1)

    with open(file_path, 'r') as file:
        for line in file:
            try:
                key, value = line.strip().split('=')
                settings[key] = value
            except ValueError:
                print(f"Aviso: Linha inválida no arquivo de configuração: {line.strip()}")

    required_keys = ["DB_USERNAME", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_DATABASE"]
    for key in required_keys:
        if key not in settings:
            print(f"Erro: '{key}' não foi encontrado no settings.txt")
            sys.exit(1)

    return settings


def test_db_connection(engine):
    """ Testa a conexão com o banco de dados antes de continuar """
    try:
        with engine.connect() as conn:
            print("✅ Conexão com o banco de dados estabelecida com sucesso!")
            # result = conn.execute("SHOW TABLES").fetchall()
            # print(f"🔍 Tabelas encontradas: {result}")
            # if not result:
            #     print("⚠️ Nenhuma tabela encontrada no banco de dados.")
    except SQLAlchemyError as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")
        sys.exit(1)


def map_mysql_to_laravel(column_type):
    """ Mapeia tipos do MySQL para equivalentes no Laravel """
    mysql_types = {
        'VARCHAR': 'string',
        'CHAR': 'char',
        'TEXT': 'text',
        'TINYTEXT': 'text',
        'MEDIUMTEXT': 'mediumText',
        'LONGTEXT': 'longText',
        'INTEGER': 'integer',
        'SMALLINT': 'smallInteger',
        'MEDIUMINT': 'mediumInteger',
        'BIGINT': 'bigInteger',
        'TINYINT': 'tinyInteger',
        'DECIMAL': 'decimal',
        'NUMERIC': 'decimal',
        'FLOAT': 'float',
        'DOUBLE': 'double',
        'BOOLEAN': 'boolean',
        'DATE': 'date',
        'TIME': 'time',
        'DATETIME': 'dateTime',
        'TIMESTAMP': 'timestamp',
        'YEAR': 'year',
        'BINARY': 'binary',
        'VARBINARY': 'binary',
        'BLOB': 'binary',
        'TINYBLOB': 'binary',
        'MEDIUMBLOB': 'binary',
        'LONGBLOB': 'binary',
        'ENUM': 'enum',
        'SET': 'set'
    }
    return mysql_types.get(column_type, 'string')


# 🔹 Ler configurações do arquivo settings.txt
settings = read_settings('settings.txt')

# 🔹 Criar string de conexão usando pymysql
db_url = f"mysql+pymysql://{settings['DB_USERNAME']}:{settings['DB_PASSWORD']}@{settings['DB_HOST']}:{settings['DB_PORT']}/{settings['DB_DATABASE']}"

# 🔹 Criar engine do SQLAlchemy
try:
    engine = create_engine(db_url)
    test_db_connection(engine)  # Testa a conexão antes de continuar
except SQLAlchemyError as e:
    print(f"❌ Erro ao criar a engine do SQLAlchemy: {e}")
    sys.exit(1)

# 🔹 Obter metadados do banco de dados
metadata = MetaData()
try:
    with engine.connect() as conn:
        metadata.reflect(bind=conn)
    print(f"📌 Tabelas carregadas: {list(metadata.tables.keys())}")
except SQLAlchemyError as e:
    print(f"❌ Erro ao carregar metadados: {e}")
    sys.exit(1)

# 🔹 Criar a pasta de migração, se não existir
migration_folder = settings['DB_DATABASE']
os.makedirs(migration_folder, exist_ok=True)

# 🔹 Inflector para singularizar nomes de tabelas
p = inflect_engine()
singularize = p.singular_noun

# 🔹 Gerar arquivos de migração para cada tabela
for table_name, table in metadata.tables.items():
    # print(f"Tabela encontrada: {table_name}")  # Verifique o nome da tabela
    table_name_singular = singularize(table_name) if singularize(table_name) else table_name
    # print(f"Tabela singularizada: {table_name_singular}")  # Verifique a tabela singularizada
    migration_file_name = os.path.join(migration_folder, f'create_{table_name_singular}_table.php')

    try:
        with open(migration_file_name, 'w') as migration_file:
            migration_file.write("<?php\n\n")
            migration_file.write(f"use Illuminate\\Support\\Facades\\Schema;\n")
            migration_file.write(f"use Illuminate\\Database\\Schema\\Blueprint;\n")
            migration_file.write(f"use Illuminate\\Database\\Migrations\\Migration;\n\n")
            migration_file.write(f"class Create{table_name_singular.title()}Table extends Migration\n")
            migration_file.write("{\n")
            migration_file.write("    public function up()\n")
            migration_file.write("    {\n")
            migration_file.write(f"        Schema::create('{table_name}', function (Blueprint $table) {{\n")

            for column in table.columns:
                column_type = str(column.type).upper()  # Converter para maiúsculo
                column_type_laravel = map_mysql_to_laravel(column_type)

                migration_file.write(f"            $table->{column_type_laravel.lower()}('{column.name}')")
                if not column.nullable:
                    migration_file.write("->nullable(false)")
                if column.primary_key:
                    migration_file.write("->primary()")
                migration_file.write(";\n")

            migration_file.write("        });\n")
            migration_file.write("    }\n\n")
            migration_file.write("    public function down()\n")
            migration_file.write("    {\n")
            migration_file.write(f"        Schema::dropIfExists('{table_name}');\n")
            migration_file.write("    }\n")
            migration_file.write("}\n")

        print(f"✅ Arquivo de migração criado: {migration_file_name}")

    except Exception as e:
        print(f"❌ Erro ao criar o arquivo de migração para {table_name}: {e}")
