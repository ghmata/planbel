import streamlit as st
import google.generativeai as genai

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
                    model = genai.GenerativeModel('gemini-pro')
                    
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
                    st.success("Plano de Aula Gerado com Sucesso!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # Botão para baixar (Gambiarra funcional no Streamlit para txt)
                    st.download_button(
                        label="📥 Baixar Plano de Aula (TXT)",
                        data=response.text,
                        file_name=f"Plano_Aula_{tema_aula}.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro: {e}")
                    st.error("Verifique se sua API Key está correta.")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Desenvolvido com Python e Streamlit | Totalmente Gratuito</div>", unsafe_allow_html=True)
