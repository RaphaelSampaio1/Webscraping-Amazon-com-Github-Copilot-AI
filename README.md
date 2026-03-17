VIDEO NO YOUTUBE: https://youtu.be/rR11C1iinzo

### ⚠️ Análise do Treinador (Blind Spots)
Antes do código, entenda o que você está ignorando:
1.  **Escalabilidade:** O uso de `time.sleep` com valores fixos é frágil. Em produção, isso causa gargalos ou bloqueios por falta de sincronia real com o DOM.
2.  **Detecção:** Você comentou o `headless`. Rodar com interface gráfica em servidores (como GitHub Actions ou Docker) quebrará o script.
3.  **Custo de Oportunidade:** Você está extraindo dados para um `.xlsx`, mas não implementou um tratamento de erros para CAPTCHAs da Amazon, o que torna o robô inútil em execuções de larga escala sem um serviço de *proxy* ou *solver*.

---

# 🕷️ Amazon Stealth Scraper Pro

![Amazon Webscraping](amazon%20webscraping.jpg)

### 🎯 Visão Geral
Este é um motor de extração de dados de alta performance desenvolvido em **Python**, projetado para minerar informações de produtos na Amazon (ES). O sistema automatiza a navegação, contorna carregamentos dinâmicos e estrutura dados brutos em relatórios executivos prontos para análise de mercado.

### 🚀 Tecnologias Core
*   **Selenium WebDriver:** Orquestração de navegação e interação com elementos dinâmicos.
*   **BeautifulSoup4:** Parsing cirúrgico de HTML para extração de metadados.
*   **OpenPyXL:** Engine de geração de relatórios em formato `.xlsx`.
*   **Python 3.x:** Lógica de backend e automação de processos.

### 🛠️ Arquitetura de Extração
O script opera em um pipeline de quatro estágios:
1.  **Handshake:** Inicialização do driver com bypass de detecção básica (maximized window & no-sandbox).
2.  **Navigation:** Simulação de comportamento humano com delays randômicos para evitar *shadow banning*.
3.  **Data Mining:** Captura de Título, Preço (Inteiro/Fração), URLs de Imagem e Links Diretos.
4.  **Persistence:** Conversão do buffer de memória para estrutura de planilha Excel.

### 📦 Instalação & Uso

```bash
# Clonar o repositório
git clone https://github.com/RaphaelSampaio1/Webscraping-Amazon-com-Github-Copilot-AI.git

# Instalar dependências
pip install -r requirements.txt

# Executar o Scraper
python scraper.py "laptop" 3
```

### 📊 Output (Exemplo)
O resultado é gerado automaticamente como `laptop_products.xlsx`, contendo:
*   **Description:** Nome completo do produto.
*   **Price:** Valor atualizado.
*   **Image Link:** URL da mídia principal.
*   **Product Link:** Link direto para conversão/análise.

### 🛡️ Roadmap de Melhorias
- [ ] Implementação de User-Agent Rotation.
- [ ] Integração com APIs de Anti-Captcha.
- [ ] Suporte a múltiplos domínios (.com, .com.br, .it).
- [ ] Exportação para banco de dados NoSQL (MongoDB).
