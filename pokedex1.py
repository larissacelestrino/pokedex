import streamlit as st
import mysql.connector
import pandas as pd
from typing import Optional


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "pokemon"

def create_table():
    sql = """
     CREATE TABLE IF NOT EXISTS pokemon (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nome VARCHAR(50) NOT NULL UNIQUE,
       tipo1 VARCHAR(50) NOT NULL,
       tipo2 VARCHAR(50),
       treinador VARCHAR(100),
       foto TEXT)"""
    
    execute_query(sql)
def create_table1():

    sql = """
     CREATE TABLE IF NOT EXISTS treinadores (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nome VARCHAR(50) NOT NULL UNIQUE,
       cidade VARCHAR(50) NOT NULL)"""
    
    execute_query(sql)

@st.cache_resource(ttl=3600)
def init_connection():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        return mydb
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao MySQL: {err}. Verifique as credenciais no script!")
        return None


def execute_query(query: str, params: Optional[tuple] = None, fetch_data: bool = False):
    mydb = init_connection()
    if mydb is None:
        return None if fetch_data else False

    cursor = None
    try:
        cursor = mydb.cursor()
        cursor.execute(query, params)

        if fetch_data:
            data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return pd.DataFrame(data, columns=columns)
        else:
            mydb.commit()
            return True

    except mysql.connector.Error as err:
        if mydb.is_connected():
            mydb.rollback()
        st.error(f"Erro na execução da query: {err}")
        return None if fetch_data else False

    finally:
        if cursor:
            cursor.close()


def insert_pokemon(nome, tipo1, tipo2, treinador, foto):
    sql = "INSERT INTO pokemon (nome, tipo1, tipo2, treinador, foto) VALUES (%s, %s, %s, %s, %s)"
    values = (nome, tipo1, tipo2, treinador, foto)
    st.cache_data.clear()
    return execute_query(sql, values)

def insert_treinador(nome, cidade):
    sql = "INSERT INTO treinadores (nome, cidade) VALUES (%s, %s)"
    values = (nome, cidade)
    st.cache_data.clear()
    return execute_query(sql, values)

def select_pokemons():
    sql = """
    SELECT 
        P.nome, 
        P.tipo1, 
        P.tipo2, 
        T.nome AS nome_treinador, 
        T.cidade AS cidade_treinador, 
        P.foto
    FROM pokemon AS P
    LEFT JOIN treinadores AS T 
        ON P.treinador = T.nome 
    ORDER BY P.nome ASC
    """
    st.cache_data.clear() 
    return execute_query(sql, fetch_data=True)

def imagem(uploaded_file):
    if uploaded_file is None:
        return None
    
    file_path = f"{uploaded_file.name}"
    
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Erro ao salvar o arquivo: {e}. Verifique as permissões de pasta.")
        return None

def formulario1_cadastro():

    with st.form("form_treinador_cadastro", clear_on_submit=True):
        nome = st.text_input("Nome do treinador")
        cidade = st.text_input("cidade do treinador")
        submit_button = st.form_submit_button("Cadastrar")
        if submit_button:
            if nome and cidade:
                if insert_treinador(nome.strip().capitalize(), cidade.strip().capitalize()):
                    st.success(f"treinador **{nome.strip().capitalize()}** cadastrado!")
            else:
                st.warning("Preencha o nome do treinador e da cidade.")

def select_treinadores():
    sql = "SELECT nome FROM treinadores ORDER BY nome ASC"
    df = st.cache_data(execute_query)(sql, fetch_data=True)
    
    if df is not None and not df.empty:
        nomes = df['nome'].tolist()
        return ["Selecione treinador "] + nomes
    else:
        return ["Sem cadastro de treinadores "]

def formulario_cadastro():
    tipos_pokemon = [
        "Normal", "Fogo", "Água", "Grama", "Elétrico", "Gelo", "Lutador",
        "Venenoso", "Terra", "Voador", "Psíquico", "Inseto", "Pedra",
        "Fantasma", "Dragão", "Aço", "Fada", "Sombrio", "Nenhum"
    ]
    
    lista_treinadores = select_treinadores()

    with st.form("form_pokemon_cadastro", clear_on_submit=True):
        nome = st.text_input("Nome do Pokémon", max_chars=50)

        col1, col2 = st.columns(2)
        with col1:
            tipo1 = st.selectbox("Tipo Principal (Tipo 1) *", tipos_pokemon[:-1])
        with col2:
            tipo2_selecionado = st.selectbox(
                "Tipo Secundário (Tipo 2)",
                tipos_pokemon,
                index=len(tipos_pokemon)-1
            )
        tipo2 = None if tipo2_selecionado == "Nenhum" else tipo2_selecionado
        
        treinador_selecionado = st.selectbox(
            "Treinador Responsável *", 
            lista_treinadores
        )

        uploaded_file = st.file_uploader(
            "Upload da Imagem do Pokémon *", 
            type=["png", "jpg", "jpeg"]
        )

        submit_button = st.form_submit_button("Cadastrar")

        if submit_button:
            treinador_valido = (treinador_selecionado not in ["Selecione treinador", "Nenhum treinador cadastrado"])
            
            if not nome or not tipo1:
                st.warning("Preencha o nome do Pokémon e o Tipo Principal (Tipo 1).")
            elif not treinador_valido:
                st.error("A **Associação Obrigatória** exige que você selecione um Treinador válido.")
            elif uploaded_file is None:
                st.error("O **Upload de Imagem** é obrigatório para o cadastro.")
            else:
                nome_treinador = treinador_selecionado
                caminho_foto = imagem(uploaded_file)
                
                if insert_pokemon(nome.strip().capitalize(), tipo1, tipo2, nome_treinador, caminho_foto):
                    st.success(f"Pokémon **{nome.strip().capitalize()}** cadastrado e associado a {nome_treinador}!")

def visualizar_pokemons():
    df_pokemons = select_pokemons()

    if df_pokemons is None:
        return

    if not df_pokemons.empty:
        df_pokemons.columns = [
            "Nome", "Tipo 1", "Tipo 2", 
            "Treinador", "Cidade do Treinador", "URL da Foto"
        ]
        
        df_pokemons["Tipo 2"] = df_pokemons["Tipo 2"].fillna("—")
        df_pokemons["Treinador"] = df_pokemons["Treinador"].fillna("Sem Treinador")
        df_pokemons["Cidade do Treinador"] = df_pokemons["Cidade do Treinador"].fillna("—")
        
        st.caption(f"Total de Pokémon cadastrados: **{len(df_pokemons)}**")
        
        cols = st.columns(3)
        col_index = 0

        for index, row in df_pokemons.iterrows():
            with cols[col_index]:
                st.subheader(f" {row['Nome']}")
                st.write(f"**Tipo 1:** {row['Tipo 1']}")
                st.write(f"**Tipo 2:** {row['Tipo 2']}")
                st.markdown(f"**Responsável:** **{row['Treinador']}** ({row['Cidade do Treinador']})")
                
                if row["URL da Foto"] and row["URL da Foto"] != 'None':
                    try:
                        st.image(row["URL da Foto"], caption=row["Nome"], use_container_width=True)
                    except:
                        st.warning("URL da imagem inválida.")
                else:
                    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/200px-Pok%C3%A9_Ball_icon.svg.png", 
                             caption="Imagem indisponível", use_container_width=True)


                st.markdown("---")

            col_index = (col_index + 1) % 3

    else:
        st.info("Nenhum Pokémon cadastrado ainda. Vá para a aba 'Cadastro de Pokémon' para começar!")

def main():
    st.set_page_config(layout="wide")
    st.title("Pokedex")

    tab_cadastro, tab_visualizar, tab_gerenciar = st.tabs(["Gerenciamento de treinadores","Cadastro de Pokémon", "Visualizar Pokémon", ])
    create_table()
    create_table1()
    with tab_cadastro:
        st.header("Cadastrar Novo Pokémon")
        formulario_cadastro()

    with tab_visualizar:
        st.header("Lista de Pokémon Cadastrados")
        visualizar_pokemons()
    
    with tab_gerenciar:
        st.header("Cadastro de novos treinadores")
        formulario1_cadastro()


if __name__ == "__main__":
    main()