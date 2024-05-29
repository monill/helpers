from sqlalchemy import create_engine, MetaData
from inflect import engine as inflect_engine
import os


def read_settings(file_path):
    settings = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            settings[key] = value
    return settings


def map_mysql_to_laravel(column_type):
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
    # Busca pelo tipo correspondente no Laravel ou retorna 'string' como padrão
    return mysql_types.get(column_type, 'string')


# Ler as configurações do arquivo settings.txt
settings = read_settings('settings.txt')

# Conectar ao banco de dados
db_url = f"mysql://{settings['DB_USERNAME']}:{settings['DB_PASSWORD']}@{settings['DB_HOST']}:{settings['DB_PORT']}/{settings['DB_DATABASE']}"
engine = create_engine(db_url)
conn = engine.connect()

# Obter metadados do banco de dados
metadata = MetaData()
metadata.reflect(bind=engine)

# Gerar arquivos de migração
p = inflect_engine()
singularize = p.singular_noun

# Criar uma pasta para salvar os arquivos de migração
migration_folder = 'tabelas'
os.makedirs(migration_folder, exist_ok=True)

for table_name, table in metadata.tables.items():
    table_name_singular = singularize(table_name) if singularize(table_name) else table_name
    migration_file_name = os.path.join(migration_folder, f'create_{table_name_singular}_table.php')

    with open(migration_file_name, 'w') as migration_file:
        migration_file.write("<?php\n\n")
        migration_file.write(f"use Illuminate\Support\Facades\Schema;\n")
        migration_file.write(f"use Illuminate\Database\Schema\Blueprint;\n")
        migration_file.write(f"use Illuminate\Database\Migrations\Migration;\n\n")
        migration_file.write(f"class Create{table_name_singular.title()}Table extends Migration\n")
        migration_file.write("{\n")
        migration_file.write(f"    public function up()\n")
        migration_file.write("    {\n")
        migration_file.write(f"        Schema::create('{table_name}', function (Blueprint $table) {{\n")

        for column in table.columns:
            column_type = str(column.type)
            column_type_laravel = map_mysql_to_laravel(column_type)

            migration_file.write(f"            $table->{column_type_laravel.lower()}('{column.name}')")
            if not column.nullable:
                migration_file.write("->nullable(false)")
            if column.primary_key:
                migration_file.write("->primary()")
            migration_file.write(";\n")

        migration_file.write(f"        }});\n")
        migration_file.write(f"    }}\n\n")
        migration_file.write(f"    public function down()\n")
        migration_file.write("    {\n")
        migration_file.write(f"        Schema::dropIfExists('{table_name}');\n")
        migration_file.write(f"    }}\n\n")
        migration_file.write(f"}}\n\n")
