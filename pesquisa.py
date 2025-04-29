import streamlit as st
import psycopg2
from datetime import datetime

# Conectar ao banco PostgreSQL
def conectar():
    return psycopg2.connect(
        host=st.secrets["host"],
        database=st.secrets["database"],
        user=st.secrets["user"],
        password=st.secrets["password"],
        port=st.secrets["port"]
    )

# Criar tabela se não existir
def criar_tabela():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id SERIAL PRIMARY KEY,
            data TIMESTAMP,
            qualidade_atendimento TEXT,
            equipe_atenciosa TEXT,
            tempo_espera TEXT,
            encontrou_produto TEXT,
            variedade_produtos TEXT,
            qualidade_produtos TEXT,
            preco_justo TEXT,
            recomendaria TEXT,
            limpeza_organizacao TEXT,
            sugestao TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Salvar resposta
def salvar_resposta(resposta):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO respostas (
            data, qualidade_atendimento, equipe_atenciosa, tempo_espera, encontrou_produto,
            variedade_produtos, qualidade_produtos, preco_justo, recomendaria,
            limpeza_organizacao, sugestao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.now(),
        resposta['qualidade_atendimento'],
        resposta['equipe_atenciosa'],
        resposta['tempo_espera'],
        resposta['encontrou_produto'],
        resposta['variedade_produtos'],
        resposta['qualidade_produtos'],
        resposta['preco_justo'],
        resposta['recomendaria'],
        resposta['limpeza_organizacao'],
        resposta['sugestao']
    ))
    conn.commit()
    cur.close()
    conn.close()

# Interface Streamlit
def main():
    st.set_page_config(page_title="Pesquisa de Satisfação - Porto Ótica")
    
    st.image("logo.png", caption="Porto Ótica", use_container_width=True)

    st.title("Pesquisa de Satisfação - Porto Ótica")
    st.markdown("Prezado cliente, por favor responda as perguntas abaixo:")

    with st.form("pesquisa_form"):
        resposta = {
            'qualidade_atendimento': st.radio("Como você avalia o atendimento?", ["Excelente", "Bom", "Regular", "Ruim", "Péssimo"]),
            'equipe_atenciosa': st.radio("A equipe foi atenciosa e esclareceu suas dúvidas?", ["Sim", "Não"]),
            'tempo_espera': st.radio("O tempo de espera foi adequado?", ["Muito rápido", "Razoável", "Longo", "Muito longo"]),
            'encontrou_produto': st.radio("Você encontrou facilmente o que procurava?", ["Sim", "Não"]),
            'variedade_produtos': st.radio("Como avalia a variedade de produtos?", ["Excelente", "Boa", "Regular", "Ruim", "Muito ruim"]),
            'qualidade_produtos': st.radio("A qualidade dos produtos atendeu suas expectativas?", ["Sim", "Não"]),
            'preco_justo': st.radio("Os preços são justos?", ["Sim", "Não"]),
            'recomendaria': st.radio("Você recomendaria a loja?", ["Sim", "Não"]),
            'limpeza_organizacao': st.radio("Como avalia a limpeza e organização da loja?", ["Excelente", "Boa", "Regular", "Ruim", "Muito ruim"]),
            'sugestao': st.text_area("Há algo que você gostaria de sugerir ou comentar?")
        }

        submitted = st.form_submit_button("Enviar")

        if submitted:
            try:
                salvar_resposta(resposta)
                st.success("Obrigado! Sua resposta foi registrada com sucesso.")
            except Exception as e:
                st.error(f"Erro ao salvar a resposta: {e}")

if __name__ == "__main__":
    criar_tabela()
    main()
