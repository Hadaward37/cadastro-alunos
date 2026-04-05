from config.database import get_connection

def main():
    conn = get_connection()
    if conn:
        print("Conectado com sucesso!")
        conn.close()
    else:
        print("Falha na conexão")

if __name__ == "__main__":
    main()
