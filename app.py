import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Planejador BNCC 2.0",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS PERSONALIZADA (Para visual moderno) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO PARA CONVERTER MARKDOWN EM HTML ---
def markdown_to_html(markdown_text, tema, serie, componente):
    """Converte o plano de aula em HTML estilizado"""
    
    # Template HTML profissional
    html_template = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plano de Aula - {tema}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 10px;
        }}
        
        .header {{
            text-align: center;
            border-bottom: 4px solid #4CAF50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #7f8c8d;
            font-size: 1.2em;
        }}
        
        .metadata {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 5px solid #4CAF50;
        }}
        
        .metadata p {{
            margin: 8px 0;
            color: #555;
        }}
        
        .metadata strong {{
            color: #2c3e50;
        }}
        
        h2 {{
            color: #4CAF50;
            font-size: 1.8em;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        h3 {{
            color: #2c3e50;
            font-size: 1.4em;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 30px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        .bncc-code {{
            background: #e8f5e9;
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #2e7d32;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Plano de Aula</h1>
            <div class="subtitle">Baseado na BNCC</div>
        </div>
        
        <div class="metadata">
            <p><strong>Tema:</strong> {tema}</p>
            <p><strong>Série/Ano:</strong> {serie}</p>
            <p><strong>Componente Curricular:</strong> {componente}</p>
            <p><strong>Data de Geração:</strong> {datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
        </div>
        
        <div class="content">
            {markdown_text}
        </div>
        
        <div class="footer">
            <p>Plano de Aula gerado automaticamente pelo Planejador BNCC 2.0</p>
            <p>Desenvolvido com Python, Streamlit e Google Gemini AI</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Conversões básicas de Markdown para HTML
    html_content = markdown_text
    
    # Negrito
    import re
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Itálico
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    
    # Títulos
    html_content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # Listas não ordenadas
    html_content = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'(<li>.*?</li>\n?)+', r'<ul>\g<0></ul>', html_content, flags=re.DOTALL)
    
    # Listas ordenadas
    html_content = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # Parágrafos
    html_content = re.sub(r'\n\n', r'</p><p>', html_content)
    html_content = f'<p>{html_content}</p>'
    
    # Destaque para códigos BNCC (exemplo: EF01LP01)
    html_content = re.sub(r'\b(EF\d{2}[A-Z]{2}\d{2})\b', r'<span class="bncc-code">\1</span>', html_content)
    
    # Insere o conteúdo no template
    final_html = html_template.replace('{markdown_text}', html_content)
    
    return final_html

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=80)
    st.title("Configuração da Aula")
    
    # Campo para API Key (Para segurança, o usuário insere a chave)
    api_key = st.text_input("Insira sua Google Gemini API Key", type="password")
    st.caption("Obtenha sua chave gratuitamente no Google AI Studio.")
    
    st.markdown("---")
    
    # Dados da Turma
    nivel_ensino = st.selectbox(
        "Nível de Ensino",
        ["Educação Infantil", "Ensino Fundamental I (1º ao 5º)", "Ensino Fundamental II (6º ao 9º)", "Ensino Médio"]
    )
    
    serie_ano = st.text_input("Série/Ano (Ex: 3º Ano)", "1º Ano")
    
    componente = st.selectbox(
        "Componente Curricular (Matéria)",
        ["Língua Portuguesa", "Matemática", "Ciências", "História", "Geografia", "Artes", "Educação Física", "Inglês", "Projeto de Vida", "Outro"]
    )
    
    tema_aula = st.text_input("Tema da Aula / Assunto", "O Ciclo da Água")
    
    duracao = st.slider("Duração (minutos)", 30, 120, 50)
    
    # Estratégias e Metodologias
    metodologia = st.selectbox(
        "Estratégia Pedagógica",
        ["Aula Expositiva Dialogada", "Gamificação", "Sala de Aula Invertida", "Aprendizagem Baseada em Projetos (PBL)", "Rotação por Estações", "Estudo de Caso"]
    )
    
    recursos = st.multiselect(
        "Recursos Disponíveis",
        ["Projetor/Datashow", "Celulares/Tablets", "Quadro e Giz", "Material Impresso", "Internet", "Jogos de Tabuleiro", "Materiais Recicláveis"],
        ["Quadro e Giz"]
    )

    objetivo_extra = st.text_area("Observações ou Objetivos Específicos (Opcional)")

    btn_gerar = st.button("✨ GERAR PLANO DE AULA")

# --- ÁREA PRINCIPAL ---
st.markdown('<div class="main-header">Planejador de Aulas Inteligente <br> <span style="font-size: 1.5rem">Baseado na BNCC</span></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("👈 Por favor, insira sua API Key na barra lateral para começar.")
    st.info("Este sistema é gratuito e utiliza a IA do Google. Seus dados não são salvos.")
else:
    # Configuração da IA
    genai.configure(api_key=api_key)
    
    if btn_gerar:
        if not tema_aula:
            st.error("Por favor, informe o tema da aula.")
        else:
            with st.spinner('Consultando a BNCC e estruturando sua aula... Aguarde...'):
                try:
                    # --- CRIAÇÃO DO PROMPT PROFISSIONAL ---
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    
                    prompt_sistema = f"""
                    Você é um Coordenador Pedagógico Especialista na BNCC (Base Nacional Comum Curricular) do Brasil.
                    Sua tarefa é criar um Plano de Aula detalhado, prático e tecnicamente correto.
                    
                    DADOS DA AULA:
                    - Nível: {nivel_ensino}
                    - Série: {serie_ano}
                    - Componente: {componente}
                    - Tema: {tema_aula}
                    - Duração: {duracao} minutos
                    - Metodologia Ativa: {metodologia}
                    - Recursos: {", ".join(recursos)}
                    - Obs: {objetivo_extra}

                    ESTRUTURA OBRIGATÓRIA DA RESPOSTA (Use Markdown):
                    1. **Cabeçalho Técnico**: Resumo dos dados.
                    2. **Alinhamento BNCC**:
                       - Identifique e cite os **Códigos Alfanuméricos** da BNCC mais adequados para este tema e série (Ex: EF01LP01).
                       - Descreva a Habilidade correspondente.
                       - Cite as Competências Gerais ou Específicas envolvidas.
                    3. **Objetivos de Aprendizagem**:
                       - Geral.
                       - Específicos (pelo menos 3).
                    4. **Desenvolvimento da Aula (Passo a Passo com tempos estimados)**:
                       - Introdução/Engajamento.
                       - Desenvolvimento/Exploração (Aplicação da metodologia {metodologia}).
                       - Sistematização/Fechamento.
                    5. **Avaliação**: Como verificar o aprendizado.
                    6. **Adaptação**: Uma sugestão para inclusão (alunos com dificuldades ou deficiência).
                    """

                    response = model.generate_content(prompt_sistema)
                    
                    # Exibição do Resultado
                    st.success("✅ Plano de Aula Gerado com Sucesso!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # Gerar HTML
                    html_content = markdown_to_html(
                        response.text,
                        tema_aula,
                        serie_ano,
                        componente
                    )
                    
                    # Criar colunas para os botões de download
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="📥 Baixar Plano em HTML",
                            data=html_content,
                            file_name=f"Plano_Aula_{tema_aula.replace(' ', '_')}.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.download_button(
                            label="📄 Baixar Plano em TXT",
                            data=response.text,
                            file_name=f"Plano_Aula_{tema_aula.replace(' ', '_')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    st.info("💡 Dica: O arquivo HTML pode ser aberto em qualquer navegador e impresso diretamente!")
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
                    st.error("Verifique se sua API Key está correta.")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Desenvolvido com Python e Streamlit | Totalmente Gratuito</div>", unsafe_allow_html=True)
