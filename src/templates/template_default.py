from bs4 import BeautifulSoup, Tag
import emoji
import json
from typing import Dict, List, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def get_technology_details(language: str) -> Dict[str, str]:
    tech_details = {
        'python': {
            'icon': '🐍',
            'svg': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg',
            'description': 'Python é uma linguagem de programação de alto nível, interpretada e orientada a objetos.'
        },
        'javascript': {
            'icon': '💛',
            'svg': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg',
            'description': 'JavaScript é uma linguagem de programação interpretada estruturada.'
        }
    }
    return tech_details.get(language.lower(), {
        'icon': '💻',
        'svg': '',
        'description': 'Tecnologia não especificada'
    })

def parse_json_data(json_str: str, field_name: str) -> dict:
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError:
        logger.error(f"Erro ao parsear JSON do campo {field_name}")
        raise
    except Exception as e:
        logger.error(f"Erro ao processar dados do campo {field_name}: {str(e)}")
        raise

def create_badge(label: str, message: str, color: str = "812ac7") -> str:
    label = label.replace(" ", "%20")
    message = message.replace(" ", "%20")
    return f'<img alt="{label}" src="https://img.shields.io/badge/{label}-{message}-{color}?style=for-the-badge"/>'

def get_technology_svg(language: str) -> str:
    tech_details = get_technology_details(language)
    return tech_details['svg']

def get_features_template() -> str:
    return """
    <div id="features-read-only">
        <h2 id="features" style="color: #9b59b6;">✨ Funcionalidades</h2>
        <ul>
            <li><!-- ATENÇÃO: Adicione nesse bloco funcionalidades e finalidades do repositório --></li>
        </ul>
    </div>
    """

def find_insertion_point(soup: BeautifulSoup) -> Optional[Tag]:
    tech_section = soup.find('div', id='section-technologies')
    if tech_section:
        return tech_section

    badges_div = soup.find('div', attrs={'align': 'left'})
    if badges_div:
        return badges_div

    first_h2 = soup.find('h2')
    if first_h2:
        return first_h2.parent

    return None

def validate_features_section(section: Tag) -> bool:
    if not section.has_attr('id') or section['id'] != 'features-read-only':
        return False
        
    h2 = section.find('h2', id='features')
    if not h2 or '✨ Funcionalidades' not in h2.text:
        return False
            
    ul = section.find('ul')
    if not ul:
        return False
            
    return True

def check_and_add_features_section(soup: BeautifulSoup) -> None:
    try:
        features_section = soup.find('div', id='features-read-only')
        
        if not features_section:
            logger.info("Seção de funcionalidades não encontrada. Adicionando...")
            new_features = BeautifulSoup(get_features_template(), 'html.parser')
            
            insertion_point = find_insertion_point(soup)
            if insertion_point:
                insertion_point.insert_after(new_features)
                logger.info("Seção de funcionalidades adicionada com sucesso")
            else:
                body = soup.find('body')
                if body:
                    body.append(new_features)
                else:
                    soup.append(new_features)
                logger.info("Seção de funcionalidades adicionada ao final do documento")
            
        else:
            if not validate_features_section(features_section):
                logger.warning("Seção de funcionalidades encontrada mas com estrutura inválida")
                existing_content = features_section.find('ul').contents if features_section.find('ul') else []
                
                new_features = BeautifulSoup(get_features_template(), 'html.parser')
                if existing_content:
                    new_features.find('ul').contents = existing_content
                
                features_section.replace_with(new_features)
                logger.info("Seção de funcionalidades corrigida mantendo conteúdo existente")
            else:
                logger.info("Seção de funcionalidades existente mantida sem alterações")
                
    except Exception as e:
        logger.error(f"Erro ao processar seção de funcionalidades: {str(e)}")
        raise

def load_template() -> str:
    try:
        template_path = Path(__file__).parent / "template.md"
        if not template_path.exists():
            logger.error(f"Template não encontrado em: {template_path}")
            raise FileNotFoundError(f"Template não encontrado em: {template_path}")
            
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Erro ao carregar template: {str(e)}")
        raise

def update_readme_content(soup: BeautifulSoup, params: dict) -> None:
    try:
        existing_features = soup.find('div', id='features-read-only')
        
        template_content = load_template()
        new_content = BeautifulSoup(template_content, 'html.parser')
        
        if existing_features and validate_features_section(existing_features):
            logger.info("Preservando seção de funcionalidades existente")
            features_section = new_content.find('div', id='features-read-only')
            if features_section:
                features_section.replace_with(existing_features)
        
        sections_to_update = {
            'technologies': update_technology_section,
            'security': update_security_section,
            'environments': update_environments_section,
            'ranking': update_ranking_section,
            'links': update_links_section,
            'installation': update_installation_section,
            'depcheck': update_depcheck_section
        }
        
        update_badges(new_content, params)
        
        for section_name, update_func in sections_to_update.items():
            try:
                update_func(new_content, params)
                logger.info(f"Seção {section_name} atualizada com sucesso")
            except Exception as e:
                logger.error(f"Erro ao atualizar seção {section_name}: {str(e)}")
        
        soup.clear()
        soup.append(new_content)
        
        logger.info("README atualizado com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao atualizar README: {str(e)}")
        raise

def update_badges(soup: BeautifulSoup, params: dict) -> None:
    try:
        language_badge = create_badge(
            f"{params['language']}",
            f"{params['language_version']}",
            "9b59b6"
        )
        badge_elem = soup.find(id='language-version')
        if badge_elem:
            badge_elem['src'] = language_badge
        
        type_badge = create_badge("TIPO", params['type'], "9b59b6")
        badge_elem = soup.find(id='type-project')
        if badge_elem:
            badge_elem['src'] = type_badge
            
    except Exception as e:
        logger.error(f"Erro ao atualizar badges: {str(e)}")
        raise

def update_technology_section(soup: BeautifulSoup, params: dict) -> None:
    tech_details = get_technology_details(params['language'])
    tech_content = f"""
    <p>{tech_details['icon']} {params['language']} {params['language_version']}</p>
    <p>{tech_details['description']}</p>
    <img src="{tech_details['svg']}" alt="{params['language']}" width="30" height="30"/>
    """
    update_section_content(soup, 'technologies', tech_content)

def update_security_section(soup: BeautifulSoup, params: dict) -> None:
    security_data = parse_json_data(params['data_security'], 'security')
    security_content = "<ul>"
    for vuln, details in security_data.items():
        security_content += f"<li><strong>{vuln}:</strong> {details}</li>"
    security_content += "</ul>"
    update_section_content(soup, 'security', security_content)

def update_environments_section(soup: BeautifulSoup, params: dict) -> None:
    versions = parse_json_data(params['versions'], 'environments')
    env_content = """
    <table>
        <tr><th>Ambiente</th><th>Versão</th></tr>
        {}
    </table>
    <p><em>Versões atualizadas em: {}</em></p>
    """.format(
        "".join([f"<tr><td>{env}</td><td>{version}</td></tr>" for env, version in versions.items()]),
        params.get('update_date', 'data não disponível')
    )
    update_section_content(soup, 'environments', env_content)

def update_ranking_section(soup: BeautifulSoup, params: dict) -> None:
    ranking_content = """
    <table>
        <tr><th>Posição</th><th>Desenvolvedor</th><th>Contribuições</th></tr>
        <tr><td>🥇</td><td>Dev 1</td><td>100</td></tr>
        <tr><td>🥈</td><td>Dev 2</td><td>80</td></tr>
        <tr><td>🥉</td><td>Dev 3</td><td>60</td></tr>
    </table>
    """
    update_section_content(soup, 'ranking', ranking_content)

def update_links_section(soup: BeautifulSoup, params: dict) -> None:
    links_content = """
    <ul>
        <li><a href="docs/">📚 Documentação</a></li>
        <li><a href="tests/">🧪 Testes</a></li>
        <li><a href="coverage/">📊 Cobertura</a></li>
    </ul>
    """
    update_section_content(soup, 'links', links_content)

def update_section_content(soup: BeautifulSoup, section_id: str, content: str) -> None:
    section = soup.find(id=section_id)
    if section:
        content_p = section.find('p')
        if content_p:
            content_p.clear()
            content_p.append(BeautifulSoup(content, 'html.parser'))

def update_installation_section(soup: BeautifulSoup, params: dict) -> None:
    try:
        installation_steps = {
            'python': """
                <h3>Requisitos</h3>
                <ul>
                    <li>Python {version}</li>
                    <li>pip (gerenciador de pacotes)</li>
                </ul>
                <h3>Passos para instalação</h3>
                <ol>
                    <li>Clone o repositório</li>
                    <li>Crie um ambiente virtual: <code>python -m venv venv</code></li>
                    <li>Ative o ambiente virtual:
                        <ul>
                            <li>Windows: <code>venv\\Scripts\\activate</code></li>
                            <li>Linux/Mac: <code>source venv/bin/activate</code></li>
                        </ul>
                    </li>
                    <li>Instale as dependências: <code>pip install -r requirements.txt</code></li>
                    <li>Configure as variáveis de ambiente conforme .env.example</li>
                    <li>Execute os testes: <code>python -m pytest</code></li>
                </ol>
            """,
            'javascript': """
                <h3>Requisitos</h3>
                <ul>
                    <li>Node.js {version}</li>
                    <li>npm ou yarn</li>
                </ul>
                <h3>Passos para instalação</h3>
                <ol>
                    <li>Clone o repositório</li>
                    <li>Instale as dependências: <code>npm install</code> ou <code>yarn</code></li>
                    <li>Configure as variáveis de ambiente conforme .env.example</li>
                    <li>Execute os testes: <code>npm test</code> ou <code>yarn test</code></li>
                </ol>
            """
        }

        installation_content = installation_steps.get(
            params['language'].lower(),
            """
                <h3>Requisitos</h3>
                <ul>
                    <li>{language} {version}</li>
                    <li>Dependências listadas no arquivo de projeto</li>
                </ul>
                <h3>Passos para instalação</h3>
                <ol>
                    <li>Clone o repositório</li>
                    <li>Instale as dependências conforme documentação da linguagem</li>
                    <li>Configure as variáveis de ambiente</li>
                    <li>Execute os testes</li>
                </ol>
            """
        ).format(
            language=params['language'],
            version=params['language_version']
        )

        section = soup.find('div', id='section-installation')
        if section:
            content_p = section.find('p', id='content-features')
            if content_p:
                content_p.clear()
                content_p.append(BeautifulSoup(installation_content, 'html.parser'))
                logger.info("Seção de instalação atualizada com sucesso")
            else:
                logger.warning("Elemento content-features não encontrado na seção de instalação")
        else:
            logger.warning("Seção de instalação não encontrada no template")

    except Exception as e:
        logger.error(f"Erro ao atualizar seção de instalação: {str(e)}")
        raise

def update_depcheck_section(soup: BeautifulSoup, params: dict) -> None:
    try:
        if 'depcheck' not in params or not params['depcheck']:
            depcheck_content = "<p>Nenhuma dependência não utilizada encontrada.</p>"
        else:
            try:
                deps = json.loads(params['depcheck'])
                if not deps:
                    depcheck_content = "<p>Nenhuma dependência não utilizada encontrada.</p>"
                else:
                    depcheck_content = """
                    <div class="depcheck-warning">
                        <h4>⚠️ Dependências não utilizadas detectadas:</h4>
                        <ul>
                    """
                    for dep in deps:
                        depcheck_content += f"<li><code>{dep}</code></li>"
                    depcheck_content += """
                        </ul>
                        <p><em>Recomendação: Remova estas dependências para otimizar o projeto.</em></p>
                    </div>
                    """
            except json.JSONDecodeError:
                logger.error("Formato JSON inválido para depcheck")
                depcheck_content = "<p>Erro ao processar dependências.</p>"

        section = soup.find('div', id='section-depcheck')
        if section:
            content_p = section.find('p', id='content-depcheck')
            if content_p:
                content_p.clear()
                content_p.append(BeautifulSoup(depcheck_content, 'html.parser'))
                logger.info("Seção de depcheck atualizada com sucesso")
            else:
                logger.warning("Elemento content-depcheck não encontrado na seção de depcheck")
        else:
            logger.warning("Seção de depcheck não encontrada no template")

    except Exception as e:
        logger.error(f"Erro ao atualizar seção de depcheck: {str(e)}")
        raise