import argparse
from string import Template

def main(project_name, version, status):
    data = {
        "logo_url": "https://via.placeholder.com/150x150.png",
        "project_name": project_name,
        "project_description": "Uma breve descrição sobre o projeto.",
        "version": version,
        "status": status,
        "functionalities": fixed_functionalities,
        "repo_url": "https://github.com/seu_usuario/nome_do_projeto.git",
        "project_folder": "nome_do_projeto"
    }
    
    markdown_content = markdown_template.substitute(data)
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)
    print("Arquivo README.md gerado com sucesso!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera README.md dinâmico")
    parser.add_argument("--project_name", required=True, help="Nome do projeto")
    parser.add_argument("--version", required=True, help="Versão do projeto")
    parser.add_argument("--status", required=True, help="Status do projeto")
    args = parser.parse_args()
    
    main(args.project_name, args.version, args.status)
