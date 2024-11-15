import argparse
import sys
import json
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from templates.template_default import (
    update_readme_content,
    parse_json_data,
    get_technology_details
)
from utils.custom_formatter import get_logger_formatter

logger = get_logger_formatter()

def validate_json_arg(value: str, field_name: str) -> str:
    """Valida se o argumento é um JSON válido"""
    try:
        json.loads(value)
        return value
    except json.JSONDecodeError:
        logger.error(f"JSON inválido para o campo {field_name}")
        raise argparse.ArgumentTypeError(f"O argumento {field_name} deve ser um JSON válido")

def validate_path(value: str) -> Path:
    """Valida se o caminho existe e é um arquivo README.md"""
    path = Path(value)
    if not path.parent.exists():
        logger.error(f"Diretório não encontrado: {path.parent}")
        raise argparse.ArgumentTypeError(f"O diretório {path.parent} não existe")
    if path.exists() and not path.is_file():
        logger.error(f"O caminho {value} não é um arquivo")
        raise argparse.ArgumentTypeError(f"O caminho {value} deve ser um arquivo")
    return path

def setup_args() -> argparse.ArgumentParser:
    """Configura os argumentos da CLI com flags melhoradas"""
    parser = argparse.ArgumentParser(description="Gerador dinâmico de README")
    
    required = parser.add_argument_group('argumentos obrigatórios')
    required.add_argument(
        "-n", "--project-name",
        required=True,
        help="Nome do projeto"
    )
    required.add_argument(
        "-t", "--type",
        required=True,
        choices=["Backend", "Frontend", "Library", "CLI"],
        help="Tipo do repositório"
    )
    required.add_argument(
        "-l", "--language",
        required=True,
        help="Linguagem do repositório"
    )
    required.add_argument(
        "-v", "--language-version",
        required=True,
        help="Versão da linguagem"
    )
    required.add_argument(
        "-p", "--path",
        type=str,
        required=True,
        help="Caminho completo para o arquivo README.md"
    )
    
    json_args = parser.add_argument_group('argumentos JSON')
    json_args.add_argument(
        "--versions",
        required=True,
        type=lambda x: validate_json_arg(x, "versions"),
        help="JSON com as versões do repositório nos ambientes. Ex: '{\"prod\": \"1.0.0\"}'"
    )
    json_args.add_argument(
        "--data-security",
        required=True,
        type=lambda x: validate_json_arg(x, "data-security"),
        help="JSON com informações de vulnerabilidade. Ex: '{\"CVE-2023\": \"Descrição\"}'"
    )
    json_args.add_argument(
        "--depcheck",
        type=lambda x: validate_json_arg(x, "depcheck"),
        help="JSON com lista de libs inutilizadas. Ex: '[\"lib1\", \"lib2\"]'"
    )
    
    return parser

def load_readme_content(path: Path) -> str:
    """Carrega o conteúdo do README existente ou cria um novo"""
    try:
        if path.exists():
            logger.info(f"Carregando README existente de: {path}")
            return path.read_text(encoding='utf-8')
        else:
            logger.warning(f"README não encontrado em {path}. Criando novo arquivo...")
            path.parent.mkdir(parents=True, exist_ok=True)
            default_content = """
            <div align="center">
            </div>
            """
            path.write_text(default_content, encoding='utf-8')
            return default_content
    except Exception as e:
        logger.error(f"Erro ao carregar/criar README: {str(e)}")
        raise

def save_readme_content(content: str, path: Path) -> None:
    """Salva o conteúdo atualizado do README"""
    try:
        if path.exists():
            backup_path = path.with_suffix('.md.bak')
            path.rename(backup_path)
            logger.info(f"Backup do README criado em: {backup_path}")
        
        path.write_text(content, encoding='utf-8')
        logger.info(f"README atualizado com sucesso em: {path}")
        
        if backup_path.exists():
            backup_path.unlink()
            
    except Exception as e:
        logger.error(f"Erro ao salvar README: {str(e)}")
        if 'backup_path' in locals() and backup_path.exists():
            backup_path.rename(path)
            logger.info("Backup do README restaurado")
        raise

def main() -> None:
    try:
        parser = setup_args()
        args = parser.parse_args()
        
        readme_path = validate_path(args.path)
        
        content = load_readme_content(readme_path)
        
        soup = BeautifulSoup(content, 'html.parser')
        
        logger.info("Iniciando atualização do README...")
        update_readme_content(soup, vars(args))
        
        save_readme_content(str(soup.prettify()), readme_path)
        
        logger.info("Processo concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao processar README: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()