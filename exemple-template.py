from string import Template

fixed_functionalities = ""
markdown_template = Template("""
<!-- Título e logo -->
<div align="center">
  <img src="${logo_url}" alt="Logo do Projeto" style="border-radius: 10px;">
  <h1 style="color: #8e44ad; font-size: 3em;">${project_name}</h1>
  <p style="font-size: 1.2em; color: #9b59b6;">${project_description}</p>
  <hr style="width: 50%; border: 1px solid #9b59b6;">
</div>

<!-- Badges -->
<div align="center">
  <img src="https://img.shields.io/badge/Versão-${version}-9b59b6?style=for-the-badge" alt="Versão">
  <img src="https://img.shields.io/badge/Status-${status}-9b59b6?style=for-the-badge" alt="Status">
</div>

<br>

<!-- Tabela de conteúdo -->
<details>
  <summary style="font-size: 1.2em; color: #8e44ad; font-weight: bold;">📋 Tabela de Conteúdo</summary>
  <ul style="list-style-type: none; padding-left: 20px;">
    <li><a href="#sobre">Sobre</a></li>
    <li><a href="#funcionalidades">Funcionalidades</a></li>
    <li><a href="#instalacao">Instalação</a></li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#contribuicao">Contribuição</a></li>
    <li><a href="#licenca">Licença</a></li>
  </ul>
</details>

---

<!-- Seções -->
<h2 id="sobre" style="color: #8e44ad;">📖 Sobre</h2>
<p>O projeto <strong>${project_name}</strong> é desenvolvido para resolver problemas X e Y com eficiência e escalabilidade.</p>

<h2 id="funcionalidades" style="color: #8e44ad;">✨ Funcionalidades</h2>
<ul style="color: #9b59b6;">
  ${functionalities}
</ul>

<h2 id="instalacao" style="color: #8e44ad;">⚙️ Instalação</h2>
<p>Siga os passos abaixo para instalar o projeto localmente.</p>

```bash
# Clone o repositório
git clone ${repo_url}

# Navegue para a pasta do projeto
cd ${project_folder}

# Instale as dependências
npm install
""")

data = { "logo_url": "https://via.placeholder.com/150x150.png", "project_name": "Nome do Projeto", "project_description": "Uma breve descrição sobre o projeto, de forma atraente e profissional.", "version": "1.0.0", "status": "Em Desenvolvimento", "functionalities": fixed_functionalities, "repo_url": "https://github.com/seu_usuario/nome_do_projeto.git", "project_folder": "nome_do_projeto" }

markdown_content = markdown_template.substitute(data)


with open("README.md", "w", encoding="utf-8") as file: file.write(markdown_content)