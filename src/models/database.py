import sqlite3
import os
from typing import Optional, List, Dict
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "data/classroom.db"):
        self.db_path = db_path
        self._create_database()

    def _create_database(self):
        """Cria o banco de dados e tabelas se não existirem"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de Professores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                face_encoding BLOB NOT NULL,
                photo_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Salas (estrutura física)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Aulas (agendamentos em salas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                teacher_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                subject TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES rooms (id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')

        # Tabela de Registro de Acessos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                class_id INTEGER,
                teacher_id INTEGER NOT NULL,
                access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms (id),
                FOREIGN KEY (class_id) REFERENCES classes (id),
                FOREIGN KEY (teacher_id) REFERENCES teachers (id)
            )
        ''')

        conn.commit()
        conn.close()

    # ===== MÉTODOS PARA PROFESSORES =====

    def add_teacher(self, name: str, age: int, phone: str, email: str,
                    face_encoding: bytes, photo_path: str) -> int:
        """Adiciona um novo professor ao banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO teachers (name, age, phone, email, face_encoding, photo_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, phone, email, face_encoding, photo_path))

        teacher_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return teacher_id

    def get_teacher(self, teacher_id: int) -> Optional[Dict]:
        """Busca um professor por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM teachers WHERE id = ?', (teacher_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'phone': row[3],
                'email': row[4],
                'face_encoding': row[5],
                'photo_path': row[6],
                'created_at': row[7]
            }
        return None

    def get_all_teachers(self) -> List[Dict]:
        """Retorna todos os professores"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM teachers')
        rows = cursor.fetchall()
        conn.close()

        teachers = []
        for row in rows:
            teachers.append({
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'phone': row[3],
                'email': row[4],
                'face_encoding': row[5],
                'photo_path': row[6],
                'created_at': row[7]
            })

        return teachers

    def delete_teacher(self, teacher_id: int) -> bool:
        """Remove um professor do banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    # ===== MÉTODOS PARA SALAS (ROOMS) =====

    def add_room(self, name: str, description: str = "") -> int:
        """Adiciona uma nova sala (estrutura física)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO rooms (name, description)
            VALUES (?, ?)
        ''', (name, description))

        room_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return room_id

    def get_room(self, room_id: int) -> Optional[Dict]:
        """Busca uma sala por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3]
            }
        return None

    def get_all_rooms(self) -> List[Dict]:
        """Retorna todas as salas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms ORDER BY name')
        rows = cursor.fetchall()
        conn.close()

        rooms = []
        for row in rows:
            rooms.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'created_at': row[3]
            })

        return rooms

    def delete_room(self, room_id: int) -> bool:
        """Remove uma sala"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    # ===== MÉTODOS PARA AULAS (CLASSES) =====

    def add_class(self, room_id: int, teacher_id: int, date: str,
                  start_time: str, end_time: str, subject: str = "") -> int:
        """Adiciona uma nova aula"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO classes (room_id, teacher_id, date, start_time, end_time, subject)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (room_id, teacher_id, date, start_time, end_time, subject))

        class_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return class_id

    def get_class(self, class_id: int) -> Optional[Dict]:
        """Busca uma aula por ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.*, r.name as room_name, t.name as teacher_name, t.email as teacher_email
            FROM classes c
            JOIN rooms r ON c.room_id = r.id
            JOIN teachers t ON c.teacher_id = t.id
            WHERE c.id = ?
        ''', (class_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'room_id': row[1],
                'teacher_id': row[2],
                'date': row[3],
                'start_time': row[4],
                'end_time': row[5],
                'subject': row[6],
                'created_at': row[7],
                'room_name': row[8],
                'teacher_name': row[9],
                'teacher_email': row[10]
            }
        return None

    def get_classes_by_room(self, room_id: int) -> List[Dict]:
        """Retorna todas as aulas de uma sala"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.*, r.name as room_name, t.name as teacher_name, t.email as teacher_email
            FROM classes c
            JOIN rooms r ON c.room_id = r.id
            JOIN teachers t ON c.teacher_id = t.id
            WHERE c.room_id = ?
            ORDER BY c.date, c.start_time
        ''', (room_id,))
        rows = cursor.fetchall()
        conn.close()

        classes = []
        for row in rows:
            classes.append({
                'id': row[0],
                'room_id': row[1],
                'teacher_id': row[2],
                'date': row[3],
                'start_time': row[4],
                'end_time': row[5],
                'subject': row[6],
                'created_at': row[7],
                'room_name': row[8],
                'teacher_name': row[9],
                'teacher_email': row[10]
            })

        return classes

    def get_all_classes(self) -> List[Dict]:
        """Retorna todas as aulas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.*, r.name as room_name, t.name as teacher_name, t.email as teacher_email
            FROM classes c
            JOIN rooms r ON c.room_id = r.id
            JOIN teachers t ON c.teacher_id = t.id
            ORDER BY c.date, c.start_time
        ''')
        rows = cursor.fetchall()
        conn.close()

        classes = []
        for row in rows:
            classes.append({
                'id': row[0],
                'room_id': row[1],
                'teacher_id': row[2],
                'date': row[3],
                'start_time': row[4],
                'end_time': row[5],
                'subject': row[6],
                'created_at': row[7],
                'room_name': row[8],
                'teacher_name': row[9],
                'teacher_email': row[10]
            })

        return classes

    def delete_class(self, class_id: int) -> bool:
        """Remove uma aula"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM classes WHERE id = ?', (class_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return deleted

    # ===== MÉTODOS PARA REGISTRO DE ACESSOS =====

    def add_access_log(self, room_id: int, teacher_id: int, status: str, class_id: Optional[int] = None) -> int:
        """Registra um acesso de professor à sala"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO access_logs (room_id, class_id, teacher_id, status)
            VALUES (?, ?, ?, ?)
        ''', (room_id, class_id, teacher_id, status))

        log_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return log_id

    def get_room_logs(self, room_id: int) -> List[Dict]:
        """Retorna todos os logs de acesso de uma sala"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT al.*, t.name as teacher_name
            FROM access_logs al
            JOIN teachers t ON al.teacher_id = t.id
            WHERE al.room_id = ?
            ORDER BY al.access_time DESC
        ''', (room_id,))
        rows = cursor.fetchall()
        conn.close()

        logs = []
        for row in rows:
            logs.append({
                'id': row[0],
                'room_id': row[1],
                'class_id': row[2],
                'teacher_id': row[3],
                'access_time': row[4],
                'status': row[5],
                'teacher_name': row[6]
            })

        return logs
