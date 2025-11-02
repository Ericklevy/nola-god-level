from sqlalchemy.orm import Session

class BaseRepository:
    """
    Um repositório base que todos os outros repositórios herdarão.
    Ele simplesmente armazena a sessão do banco de dados.
    """
    def __init__(self, db: Session):
        self.db = db
