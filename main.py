import sqlite3
from tkinter import messagebox

DB_NAME = 'estudante.db'  # Define o nome do banco de dados como constante

class SistemaDeRegistro:
    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria a tabela se não existir."""
        self.conn = sqlite3.connect(DB_NAME)  # Usa a constante DB_NAME
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela 'estudantes' no banco de dados se ela ainda não existir."""
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS estudantes (
                                id INTEGER  PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                email TEXT NOT NULL,
                                tel TEXT NOT NULL,
                                sexo TEXT NOT NULL,
                                data_nascimento NOT NULL,
                                endereco TEXT NULL,
                                curso TEXT NOT NULL,
                                imagem TEXT NOT NULL)
                            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela: {e}")
            messagebox.showerror('ERRO', f"Erro ao criar a tabela: {e}")
            # Aqui você pode adicionar um tratamento de erro mais robusto, como logar o erro.

    def register_student(self, estudantes):
        """Registra um novo estudante no banco de dados."""
        try:
            self.c.execute("INSERT INTO estudantes(nome, email, tel, sexo, data_nascimento,endereco, curso, imagem) VALUES (?,?,?,?,?,?,?,?)", estudantes)
            self.conn.commit()
            messagebox.showinfo('SUCESSO','Aluno Resgistrado com Sucesso!')
        except sqlite3.Error as e:
            messagebox.showerror('ERRO', f"Erro ao registrar aluno: {e}")
            self.conn.rollback() # Importante para desfazer a transação em caso de erro

    def view_all_students(self):
        """Retorna todos os estudantes cadastrados no banco de dados."""
        try:
            self.c.execute("SELECT * FROM estudantes")
            dados = self.c.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror('ERRO', f"Erro ao visualizar todos os alunos: {e}")
            return []

    def search_students(self, id):
        """Busca um estudante no banco de dados pelo ID."""
        try:
            self.c.execute("SELECT * FROM estudantes WHERE id=?", (id,))
            dados = self.c.fetchone()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror('ERRO', f"Erro ao procurar aluno com ID {id}: {e}")
            return None
        
     # *** INSERIR ESTA FUNÇÃO ***
    def search_students_by_name(self, nome):
        try:
            # Usamos LIKE para busca parcial e % como curinga
            self.c.execute("SELECT * FROM estudantes WHERE nome LIKE ?", ('%' + nome + '%',))
            dados = self.c.fetchall()
            return dados
        except sqlite3.Error as e:
            messagebox.showerror('ERRO', f"Erro ao procurar aluno com nome '{nome}': {e}")
            return []   




        

    def update_student(self, novo_valor):
        """Atualiza as informações de um estudante no banco de dados."""
        try:
            query = "UPDATE estudantes SET nome=?, email=?, tel=?, sexo=?, data_nascimento=?, endereco=?, curso=?, imagem=? WHERE id=?"
            self.c.execute(query, novo_valor)
            self.conn.commit()
            messagebox.showinfo('SUCESSO', f'Estudante com ID: {novo_valor[8]} foi atualizado com Sucesso!')
        except sqlite3.Error as e:
            messagebox.showerror('ERRO', f"Erro ao atualizar aluno com ID {novo_valor[8]}: {e}")
            self.conn.rollback()

    def delete_student(self, id):
        """Exclui um estudante do banco de dados pelo ID."""
        try:
            self.c.execute("DELETE FROM estudantes WHERE id=?", (id,))
            self.conn.commit()
            messagebox.showinfo('SUCESSO', f'Estudante com ID: {id} foi Deletado com Sucesso!')
        except sqlite3.Error as e:
            messagebox.showerror('ERRO', f"Erro ao deletar aluno com ID {id}: {e}")
            self.conn.rollback()

    def close_connection(self):
        """Fecha a conexão com o banco de dados."""
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao fechar a conexão: {e}")

# Criando uma instância do Sistema de Registro
sistema_de_registro = SistemaDeRegistro()

if __name__ == '__main__':
    # Bloco de teste (opcional)
    pass