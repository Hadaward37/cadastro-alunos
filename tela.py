# Importando dependencias do Tkinter----------------------
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd

# importando pillow---------------------------------------
from PIL import ImageTk, Image

# Tk calendar---------------------------------------------
from tkcalendar import Calendar, DateEntry
from datetime import date

# Importando main
from main import *

# Variável para controlar se um aluno foi carregado para edição
aluno_carregado = False

# Cores---------------------------------------------------
co0 = "#2e2d2b"  # Preta
co1 = "#feffff"  # Branca
co2 = "#e5e5e5"  # grey
co3 = "#00a095"  # Verde
co4 = "#403d3d"  # letra
co6 = "#003452"  # azul
co7 = "#ef5350"  # vermelha

co6 = "#146C94"  # azul (redefinido)
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # + verde


# criando janela-----------------------------------------
janela = Tk()
janela.title("")
janela.geometry('810x535')
janela.configure(background=co1)
janela.resizable(width=FALSE, height=FALSE)

style = Style(janela)
style.theme_use('clam')

# Criando os frames---------------------------------------
frame_logo = Frame(janela, width=850, height=52, bg=co6)
frame_logo.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW, columnspan=5)

frame_botoes = Frame(janela, width=100, height=200, bg=co1, relief=RAISED)
frame_botoes.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frame_detalhes = Frame(janela, width=800, height=100, bg=co1, relief=SOLID)
frame_detalhes.grid(row=1, column=1, pady=1, padx=10, sticky=NSEW)

frame_tabela = Frame(janela, width=800, height=100, bg=co1, relief=SOLID)
frame_tabela.grid(row=3, column=0, pady=0, padx=10, sticky=NSEW, columnspan=5)

# Frame Logo-------------------------------------------------
global image, imagem_string, l_imagem

# Abre a imagem do logo
app_lg = Image.open('chapeu.png')
app_lg = app_lg.resize((50, 50))
app_lg = ImageTk.PhotoImage(app_lg)
# Cria o Label para o logo com texto
app_logo = Label(frame_logo, image=app_lg, text=" Registro de Alunos", width=850, compound=LEFT, anchor=NW, font=('Verdana 15'), bg=co6, fg=co1)
app_logo.place(x=5, y=0)

# Abrindo a imagem padrão para detalhes
imagem = Image.open('chapeu.png')
imagem = imagem.resize((130, 130))
imagem = ImageTk.PhotoImage(imagem)
l_imagem = Label(frame_detalhes, image=imagem, bg=co1, fg=co4)
l_imagem.place(x=390, y=10)


# Criando Funçoes para CRUD-------------------------------------------------------
# Funcao adiconar
def adicionar():
    global imagem_string, l_imagem

    # obtendo valores dos campos de entrada
    nome = e_nome.get()
    email = e_email.get()
    tel = e_tel.get()
    sexo = c_sexo.get()
    data = data_nascimento.get()
    endereco = e_endereco.get()
    curso = c_curso.get()
    img = imagem_string

    # Criando uma lista com os valores
    lista = [nome, email, tel, sexo, data, endereco, curso, img]

    # verificando se algum campo está vazio
    for i in lista:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Registrando os valores no sistema
    sistema_de_registro.register_student(lista)

    # Limpando os campos de entrada após o registro
    e_nome.delete(0, END)
    e_email.delete(0, END)
    e_tel.delete(0, END)
    c_sexo.delete(0, END)
    data_nascimento.delete(0, END)
    e_endereco.delete(0, END)
    c_curso.delete(0, END)

    # *** RESETANDO A FOTO PARA A PADRÃO APÓS A ADIÇÃO ***
    imagem_padrao = Image.open('chapeu.png')
    imagem_padrao = imagem_padrao.resize((130, 130))
    imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
    l_imagem.config(image=imagem_padrao)
    l_imagem.image = imagem_padrao  # Manter a referência

    # Mostrando os valores atualizados na tabela
    mostrar_alunos()

def procurar():
    global imagem, imagem_string, l_imagem, aluno_carregado, tree_aluno

    termo_busca = e_procurar.get().strip()

    if termo_busca:
        if termo_busca.isdigit():
            # Tenta buscar por ID
            try:
                id_aluno = int(termo_busca)
                dados = sistema_de_registro.search_students(id_aluno)
                if dados:
                    # Limpa e preenche os campos com os dados do aluno encontrado
                    e_nome.delete(0, END)
                    e_email.delete(0, END)
                    e_tel.delete(0, END)
                    c_sexo.set('')
                    data_nascimento.delete(0, END)
                    e_endereco.delete(0, END)
                    c_curso.set('')

                    e_nome.insert(END, dados[1])
                    e_email.insert(END, dados[2])
                    e_tel.insert(END, dados[3])
                    c_sexo.set(dados[4])
                    data_nascimento.insert(END, dados[5])
                    e_endereco.insert(END, dados[6])
                    c_curso.set(dados[7])

                    imagem_path = dados[8]
                    imagem_string = imagem_path
                    try:
                        imagem = Image.open(imagem_path)
                        imagem = imagem.resize((130, 130))
                        imagem = ImageTk.PhotoImage(imagem)
                        l_imagem.config(image=imagem)
                        l_imagem.image = imagem
                    except FileNotFoundError:
                        try:
                            imagem_padrao = Image.open('chapeu.png')
                            imagem_padrao = imagem_padrao.resize((130, 130))
                            imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
                            l_imagem.config(image=imagem_padrao)
                            l_imagem.image = imagem_padrao
                        except FileNotFoundError:
                            l_imagem.config(text="Sem imagem", image='')
                    aluno_carregado = True
                    app_adicionar.config(state=DISABLED)
                else:
                    messagebox.showinfo('Info', f'Aluno com ID "{termo_busca}" não encontrado.')
                    aluno_carregado = False
                    app_adicionar.config(state=NORMAL)
            except ValueError:
                messagebox.showerror('Erro', 'Por favor, insira um ID válido para procurar.')
            except Exception as e:
                messagebox.showerror('Erro', f'Ocorreu um erro ao procurar por ID: {e}')
        else:
            # Tenta buscar por nome
            resultados = sistema_de_registro.search_students_by_name(termo_busca)
            if resultados:
                # Limpa e preenche os campos com os dados do primeiro aluno encontrado
                primeiro_aluno = resultados[0]
                e_nome.delete(0, END)
                e_email.delete(0, END)
                e_tel.delete(0, END)
                c_sexo.set(primeiro_aluno[4])  # Sexo
                data_nascimento.delete(0, END)
                data_nascimento.insert(END, primeiro_aluno[5]) # Data de Nascimento
                e_endereco.delete(0, END)
                e_endereco.insert(END, primeiro_aluno[6])
                c_curso.set(primeiro_aluno[7]) # Curso

                # *** INSERINDO OS VALORES FALTANTES ***
                e_nome.insert(END, primeiro_aluno[1])  # Nome
                e_email.insert(END, primeiro_aluno[2]) # Email
                e_tel.insert(END, primeiro_aluno[3])   # Telefone

                imagem_path = primeiro_aluno[8]
                imagem_string = imagem_path
                try:
                    imagem = Image.open(imagem_path)
                    imagem = imagem.resize((130, 130))
                    imagem = ImageTk.PhotoImage(imagem)
                    l_imagem.config(image=imagem)
                    l_imagem.image = imagem
                except FileNotFoundError:
                    try:
                        imagem_padrao = Image.open('chapeu.png')
                        imagem_padrao = imagem_padrao.resize((130, 130))
                        imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
                        l_imagem.config(image=imagem_padrao)
                        l_imagem.image = imagem_padrao
                    except FileNotFoundError:
                        l_imagem.config(text="Sem imagem", image='')
                aluno_carregado = True
                app_adicionar.config(state=DISABLED)

                messagebox.showinfo('Info', f'Aluno(s) encontrado(s) com o nome contendo "{termo_busca}". Os dados do primeiro aluno (ID: {primeiro_aluno[0]}) foram carregados.')
            else:
                messagebox.showinfo('Info', f'Nenhum aluno encontrado com o nome contendo "{termo_busca}".')
                aluno_carregado = False
                app_adicionar.config(state=NORMAL)
    else:
        messagebox.showerror('Erro', 'Por favor, digite um ID ou nome para procurar.')
# funçao atualizar alunos
def atualizar():
    global imagem_string, l_imagem, aluno_carregado

    # Verifica se um aluno foi carregado para atualização
    if not aluno_carregado:
        messagebox.showerror('Erro', 'Por favor, procure um aluno para atualizar.')
        return

    try:
        # obtendo o id do aluno a ser atualizado
        id_aluno = int(e_procurar.get())

        # obtendo os novos valores dos campos de entrada
        nome = e_nome.get()
        email = e_email.get()
        tel = e_tel.get()
        sexo = c_sexo.get()
        data = data_nascimento.get()
        endereco = e_endereco.get()
        curso = c_curso.get()
        img = imagem_string

        # Criando a lista com os valores a serem atualizados, incluindo o ID
        lista = [nome, email, tel, sexo, data, endereco, curso, img, id_aluno]

        # verificando se algum campo está vazio
        for i in lista[:-1]:  # Exclui o ID da verificação de campos vazios
            if i == '':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
        # *** CHAMANDO A FUNÇÃO PARA ATUALIZAR NO BANCO DE DADOS ***
        sistema_de_registro.update_student(lista)

        # Limpar os campos de entrada após a atualização
        e_nome.delete(0, END)
        e_email.delete(0, END)
        e_tel.delete(0, END)
        c_sexo.set('')
        data_nascimento.delete(0, END)
        e_endereco.delete(0, END)
        c_curso.set('')
        e_procurar.delete(0, END)  # Limpar o campo de procura também

        # Resetar a foto para a padrão
        imagem_padrao = Image.open('chapeu.png')
        imagem_padrao = imagem_padrao.resize((130, 130))
        imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
        l_imagem.config(image=imagem_padrao)
        l_imagem.image = imagem_padrao

        # *** CHAMANDO A FUNÇÃO PARA ATUALIZAR A TABELA NA INTERFACE ***
        mostrar_alunos()

        # *** REABILITAR O BOTÃO "ADICIONAR" APÓS A ATUALIZAÇÃO E LIMPEZA ***
        aluno_carregado = False
        app_adicionar.config(state=NORMAL)

    except ValueError:
        messagebox.showerror('Erro', 'Por favor, procure um aluno válido para atualizar.')
    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro ao atualizar: {e}')


# funçao Deletar alunos
def deletar():
    global imagem, imagem_string, l_imagem, aluno_carregado

    # Verifica se um aluno foi carregado para deleção
    if not aluno_carregado:
        messagebox.showerror('Erro', 'Por favor, procure um aluno para deletar.')
        return

    try:
        # obtendo o id do aluno a ser deletado
        id_aluno = int(e_procurar.get())

        # deletando aluno do sistema
        sistema_de_registro.delete_student(id_aluno)
        messagebox.showinfo('Sucesso', f'Aluno com ID: {id_aluno} foi Deletado com Sucesso!')

        # *** CARREGANDO A IMAGEM PADRÃO APÓS A DELEÇÃO ***
        imagem_padrao = Image.open('chapeu.png')
        imagem_padrao = imagem_padrao.resize((130, 130))
        imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
        l_imagem.config(image=imagem_padrao)
        l_imagem.image = imagem_padrao  # Manter a referência

        # *** CHAME A FUNÇÃO PARA ATUALIZAR A TABELA AQUI ***
        mostrar_alunos()

        # Limpando campos de entrada após a deleção
        e_nome.delete(0, END)
        e_email.delete(0, END)
        e_tel.delete(0, END)
        c_sexo.set('')
        data_nascimento.delete(0, END)
        e_endereco.delete(0, END)
        c_curso.set('')
        e_procurar.delete(0, END)

        # Resetando a variável de aluno carregado e habilitando o botão adicionar
        aluno_carregado = False
        app_adicionar.config(state=NORMAL)

    except ValueError:
        messagebox.showerror('Erro', 'Por favor, insira o ID do aluno para deletar.')
    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro ao deletar: {e}')


def limpar_campos():
    global imagem, imagem_string, l_imagem, aluno_carregado

    # Limpa todos os campos de entrada
    e_procurar.delete(0, END)
    e_nome.delete(0, END)
    e_email.delete(0, END)
    e_tel.delete(0, END)
    c_sexo.set('')  # Limpar o Combobox usando .set('')
    data_nascimento.delete(0, END)
    e_endereco.delete(0, END)
    c_curso.set('')  # Limpar o Combobox usando .set('')

    # Resetar a foto para a padrão
    imagem_padrao = Image.open('chapeu.png')
    imagem_padrao = imagem_padrao.resize((130, 130))
    imagem_padrao = ImageTk.PhotoImage(imagem_padrao)
    l_imagem.config(image=imagem_padrao)
    l_imagem.image = imagem_padrao

    # Habilitar o botão "Adicionar" novamente
    aluno_carregado = False
    app_adicionar.config(state=NORMAL)

    # Mostrando os valores na tabela (que estará vazia se nenhum aluno foi adicionado novamente)
    mostrar_alunos()


# Criando os campos de entrada----------------------------------
l_nome = Label(frame_detalhes, text='Nome *', anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_nome.place(x=4, y=10)
e_nome = Entry(frame_detalhes, width=30, justify='left', relief='solid')
e_nome.place(x=7, y=40)

l_email = Label(frame_detalhes, text='Email *', anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_email.place(x=4, y=70)
e_email = Entry(frame_detalhes, width=30, justify='left', relief='solid')
e_email.place(x=7, y=100)

l_tel = Label(frame_detalhes, text='Telefone *', anchor=NW, font=('Ivy 10'), bg=co1, )
l_tel.place(x=4, y=130)
e_tel = Entry(frame_detalhes, width=15, justify='left', relief='solid')
e_tel.place(x=7, y=160)

l_sexo = Label(frame_detalhes, text='Sexo *', anchor=NW, font=('Ivy 10'), bg=co1, )
l_sexo.place(x=127, y=130)
c_sexo = ttk.Combobox(frame_detalhes, width=7, font=('Ivy 8 bold'), justify='center')
c_sexo['values'] = ('M', 'F', 'Outros')
c_sexo.place(x=130, y=160)

l_data_nascimento = Label(frame_detalhes, text='Data de Nascimento *', anchor=NW, font=('Ivy 10'), bg=co1, )
l_data_nascimento.place(x=220, y=10)
data_nascimento = DateEntry(frame_detalhes, width=18, justify='center', background='darkblue', foreground='white', borderwidth=2, year=2023, )
data_nascimento.place(x=224, y=40)

l_endereco = Label(frame_detalhes, text='Endereço *', anchor=NW, font=('Ivy 10'), bg=co1, )
l_endereco.place(x=220, y=69)
e_endereco = Entry(frame_detalhes, width=25, justify='left', relief='solid')
e_endereco.place(x=224, y=100)


cursos = ['Engenharia', 'Medicina', 'Analise de Sistemas', 'Educação Fisica', 'Licenciatura', 'Advocacia']


l_curso = Label(frame_detalhes, text='Cursos *', anchor=NW, font=('Ivy 10'), bg=co1, )
l_curso.place(x=220, y=130)
c_curso = ttk.Combobox(frame_detalhes, width=20, font=('Ivy 8 bold'), justify='center')
c_curso['values'] = (cursos)
c_curso.place(x=224, y=160)


# Escolher imagem----------------------------------------------
def escolher_imagem():
    global imagem, imagem_string, l_imagem

    imagem = fd.askopenfilename()
    imagem_string = imagem

    imagem = Image.open(imagem)
    imagem = imagem.resize((130, 130))
    imagem = ImageTk.PhotoImage(imagem)
    l_imagem = Label(frame_detalhes, image=imagem, bg=co1, fg=co4)
    l_imagem.place(x=390, y=10)

    botao_carregar['text'] = 'TROCAR DE FOTO'


botao_carregar = Button(frame_detalhes, command=escolher_imagem, text='Carregar Foto'.upper(), width=20, compound=CENTER, anchor=CENTER, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co1, fg=co0)
botao_carregar.place(x=390, y=160)


# Tabela Alunos------------------------------------
def mostrar_alunos():
    global tree_aluno
    # creating a treeview with dual scrollbars--------------
    list_header = ['id', 'Nome', 'email', 'Telefone', 'sexo', 'Data', 'Endereço', 'Curso']

    # view all students--------------------------------
    df_list = sistema_de_registro.view_all_students()

    tree_aluno = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")

    # Vertical scroollbar----------------------------
    vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_aluno.yview)

    # Horizontal scroollbar----------------------------
    hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_aluno.xview)

    tree_aluno.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree_aluno.grid(column=0, row=1, sticky='nsew')
    vsb.grid(column=1, row=1, sticky='ns')
    hsb.grid(column=0, row=2, sticky='ew')
    frame_tabela.grid_rowconfigure(0, weight=12)

    hd = ["nw", "nw", "nw", "center", "center", "center", "center", "center", "center"]
    h = [40, 150, 150, 70, 70, 70, 120, 100, 100]
    n = 0

    for col in list_header:
        tree_aluno.heading(col, text=col.title(), anchor=NW)
        # Adjust the column's width to the header string
        tree_aluno.column(col, width=h[n], anchor=hd[n])
        n += 1
    for item in df_list:
        tree_aluno.insert('', 'end', values=item)


# Procurar aluno------------------------------------

frame_procurar = Frame(frame_botoes, width=180, height=55, bg=co1, relief=RAISED)
frame_procurar.grid(row=0, column=0, pady=10, padx=10, sticky=NSEW)

l_procurar = Label(frame_procurar, text="Procurar Aluno [ID ou Nome]", anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_procurar.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky=NW)

e_procurar = Entry(frame_procurar, width=15, justify='left', relief='solid', font=('Ivy 10'))
e_procurar.grid(row=1, column=0, pady=5, padx=5, sticky=W)

botao_procurar = Button(frame_procurar, command=procurar, text='Buscar', width=8, anchor=CENTER, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co1, fg=co0)
botao_procurar.grid(row=1, column=1, pady=5, padx=5, sticky=E)


# BTG Adicionar Aluno--------------------------------------------------------
app_img_adicionar = Image.open('adicionar.png')
app_img_adicionar = app_img_adicionar.resize((25, 25))
app_img_adicionar = ImageTk.PhotoImage(app_img_adicionar)

app_adicionar = Button(frame_botoes, command=adicionar, image=app_img_adicionar, relief=GROOVE, text=' Adicionar', width=100, compound=LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_adicionar.grid(row=1, column=0, pady=5, padx=10, sticky=NSEW)

app_adicionar.config(state=NORMAL)
aluno_carregado = False  # Garante que a variável esteja False no início/comando adicionado recente


# BTG Atualizar Aluno---------------------------------------------
app_img_atualizar = Image.open('atualizar.jpeg')
app_img_atualizar = app_img_atualizar.resize((25, 25))
app_img_atualizar = ImageTk.PhotoImage(app_img_atualizar)

app_atualizar = Button(frame_botoes, command=atualizar, image=app_img_atualizar, relief=GROOVE, text=' Atualizar', width=100, compound=LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_atualizar.grid(row=2, column=0, pady=5, padx=10, sticky=NSEW)

# BTG Deletar Aluno----------------------------------------
app_img_deletar = Image.open('delete.png')
app_img_deletar = app_img_deletar.resize((25, 25))
app_img_deletar = ImageTk.PhotoImage(app_img_deletar)

app_deletar = Button(frame_botoes, command=deletar, image=app_img_deletar, relief=GROOVE, text=' Deletar', width=100, compound=LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_deletar.grid(row=3, column=0, pady=5, padx=10, sticky=NSEW)

# BTG Limpar Aluno--------------------------------------------------------
app_img_limpar = Image.open('limpar.png')  # Certifique-se que o caminho está correto
app_img_limpar = app_img_limpar.resize((25, 25))
app_img_limpar = ImageTk.PhotoImage(app_img_limpar)

app_limpar = Button(frame_botoes, command=limpar_campos, image=app_img_limpar, relief=GROOVE, text=' Limpar', width=100, compound=LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_limpar.grid(row=4, column=0, pady=5, padx=10, sticky=NSEW)


# Linha separadora----------------------------------------------
l_linha = Label(frame_botoes, relief=GROOVE, text='h', width=1, height=123, font=('Ivy 1'), bg=co1, fg=co0)
l_linha.place(x=266, y=15)


def fechar_janela():
    sistema_de_registro.close_connection()
    janela.destroy()


janela.protocol("WM_DELETE_WINDOW", fechar_janela)

# Chamar a tabela para exibir os alunos ao iniciar
mostrar_alunos()

janela.mainloop()
