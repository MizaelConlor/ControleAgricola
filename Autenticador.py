import streamlit as st
import sqlite3
from streamlit_authenticator import Authenticate

# Configuração do banco de dados SQLite
conn = sqlite3.connect('user_data.db')
c = conn.cursor()

# Cria a tabela de usuários se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')

# Cria a tabela de dados do usuário se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        user_id INTEGER,
        data TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
''')
conn.commit()

# Configuração do autenticador
authenticator = Authenticate(
    {'usernames': {'alice': {'password': 'alice123'}, 'bob': {'password': 'bob123'}}},
    'cookie_name', 'signature_key', cookie_expiry_days=30
)

# Interface de login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Bem-vindo *{name}*')

    # Carrega os dados do usuário
    c.execute('SELECT user_id FROM users WHERE username = ?', (username,))
    user_id = c.fetchone()[0]

    # Interface para salvar dados
    user_data = st.text_area("Digite seus dados pessoais:")
    if st.button("Salvar Dados"):
        c.execute('INSERT INTO user_data (user_id, data) VALUES (?, ?)', (user_id, user_data))
        conn.commit()
        st.success("Dados salvos com sucesso!")

    # Exibe os dados salvos
    c.execute('SELECT data FROM user_data WHERE user_id = ?', (user_id,))
    saved_data = c.fetchall()
    if saved_data:
        st.write("Seus dados salvos:")
        for data in saved_data:
            st.write(data[0])

elif authentication_status == False:
    st.error('Username/password está incorreto')
elif authentication_status == None:
    st.warning('Por favor, insira seu username e password')

# Fecha a conexão com o banco de dados
conn.close()