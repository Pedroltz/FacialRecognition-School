import os
from typing import Tuple, Optional, Dict, List
import numpy as np
from datetime import datetime, timedelta
from src.models.database import Database
from src.utils.face_recognition import FaceRecognizer

class RoomController:
    def __init__(self):
        self.db = Database()
        self.face_recognizer = FaceRecognizer()

    # ===== GERENCIAMENTO DE PROFESSORES =====

    def register_teacher(self, name: str, age: int, phone: str, email: str,
                        photo_path: str) -> Tuple[bool, str]:
        """
        Registra um novo professor no sistema

        Args:
            name: Nome completo do professor
            age: Idade do professor
            phone: Telefone do professor
            email: Email do professor
            photo_path: Caminho da foto do professor

        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Gerar encoding da face
            face_encoding = self.face_recognizer.encode_face(photo_path)

            if face_encoding is None:
                return False, "Nenhuma face detectada na foto!"

            # Converter encoding para bytes
            encoding_bytes = FaceRecognizer.encoding_to_bytes(face_encoding)

            # Salvar foto permanente
            teacher_photo_path = f"data/faces/teacher_{name.replace(' ', '_')}_{os.getpid()}.jpg"
            os.rename(photo_path, teacher_photo_path)

            # Adicionar ao banco de dados
            teacher_id = self.db.add_teacher(
                name=name,
                age=age,
                phone=phone,
                email=email,
                face_encoding=encoding_bytes,
                photo_path=teacher_photo_path
            )

            return True, f"Professor {name} cadastrado com sucesso! (ID: {teacher_id})"

        except Exception as e:
            return False, f"Erro ao cadastrar professor: {str(e)}"

    def get_all_teachers(self) -> List[Dict]:
        """Retorna todos os professores cadastrados"""
        return self.db.get_all_teachers()

    def delete_teacher(self, teacher_id: int) -> bool:
        """Remove um professor do sistema"""
        teacher = self.db.get_teacher(teacher_id)
        if teacher:
            # Remover foto
            if os.path.exists(teacher['photo_path']):
                os.remove(teacher['photo_path'])

            # Remover do banco
            return self.db.delete_teacher(teacher_id)

        return False

    # ===== GERENCIAMENTO DE SALAS =====

    def create_room(self, name: str, description: str = "") -> Tuple[bool, str]:
        """
        Cria uma nova sala (estrutura física)

        Args:
            name: Nome da sala (ex: "Sala A", "Laboratório 1")
            description: Descrição opcional da sala

        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            room_id = self.db.add_room(name=name, description=description)
            return True, f"Sala '{name}' criada com sucesso! (ID: {room_id})"
        except Exception as e:
            return False, f"Erro ao criar sala: {str(e)}"

    def get_all_rooms(self) -> List[Dict]:
        """Retorna todas as salas cadastradas"""
        return self.db.get_all_rooms()

    def delete_room(self, room_id: int) -> bool:
        """Remove uma sala do sistema"""
        return self.db.delete_room(room_id)

    # ===== GERENCIAMENTO DE AULAS =====

    def create_class(self, room_id: int, teacher_id: int, day_of_week: str,
                    start_time: str, end_time: str, subject: str = "") -> Tuple[bool, str]:
        """
        Cria uma nova aula em uma sala

        Args:
            room_id: ID da sala
            teacher_id: ID do professor
            day_of_week: Dia da semana (Segunda, Terça, Quarta, Quinta, Sexta, Sábado)
            start_time: Horário de início (HH:MM)
            end_time: Horário de término (HH:MM)
            subject: Matéria/assunto opcional

        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Validar se a sala existe
            room = self.db.get_room(room_id)
            if not room:
                return False, "Sala não encontrada!"

            # Validar se o professor existe
            teacher = self.db.get_teacher(teacher_id)
            if not teacher:
                return False, "Professor não encontrado!"

            # Validar dia da semana
            valid_days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
            if day_of_week not in valid_days:
                return False, "Dia da semana inválido!"

            # Validar formato de horários
            try:
                datetime.strptime(start_time, '%H:%M')
                datetime.strptime(end_time, '%H:%M')
            except ValueError:
                return False, "Formato de hora inválido! Use HH:MM."

            # Adicionar aula ao banco de dados
            class_id = self.db.add_class(
                room_id=room_id,
                teacher_id=teacher_id,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time,
                subject=subject
            )

            return True, f"Aula criada com sucesso na {room['name']}! (ID: {class_id})"

        except Exception as e:
            return False, f"Erro ao criar aula: {str(e)}"

    def get_classes_by_room(self, room_id: int) -> List[Dict]:
        """Retorna todas as aulas de uma sala"""
        return self.db.get_classes_by_room(room_id)

    def get_all_classes(self) -> List[Dict]:
        """Retorna todas as aulas"""
        return self.db.get_all_classes()

    def delete_class(self, class_id: int) -> bool:
        """Remove uma aula do sistema"""
        return self.db.delete_class(class_id)

    # ===== AUTENTICAÇÃO E VALIDAÇÃO =====

    def authenticate_teacher_in_room(self, frame: np.ndarray, room_id: int) -> Tuple[bool, Optional[Dict], str, Optional[Dict]]:
        """
        Autentica um professor através de reconhecimento facial para uma sala específica
        Permite acesso se houver uma aula agendada (10min antes) ou aceita qualquer professor na sala

        Args:
            frame: Frame capturado da câmera
            room_id: ID da sala

        Returns:
            Tupla (sucesso, dados_do_professor, mensagem_status, dados_da_aula_ou_None)
        """
        try:
            # Buscar informações da sala
            room = self.db.get_room(room_id)
            if not room:
                return False, None, "Sala não encontrada!", None

            # Gerar encoding do frame
            unknown_encoding = self.face_recognizer.encode_face_from_frame(frame)

            if unknown_encoding is None:
                return False, None, "Nenhuma face detectada!", None

            # Buscar todos os professores cadastrados
            teachers = self.db.get_all_teachers()

            if not teachers:
                return False, None, "Nenhum professor cadastrado!", None

            # Preparar encodings conhecidos
            known_encodings = []
            for teacher in teachers:
                encoding = FaceRecognizer.bytes_to_encoding(teacher['face_encoding'])
                known_encodings.append((teacher['id'], encoding))

            # Buscar correspondência
            teacher_id = self.face_recognizer.find_match(unknown_encoding, known_encodings)

            if teacher_id is None:
                return False, None, "Professor não reconhecido!", None

            # Buscar dados completos do professor
            teacher_data = self.db.get_teacher(teacher_id)

            # Buscar aula correspondente ao horário atual nesta sala (qualquer professor)
            current_class = self._find_current_class(room_id)

            if current_class:
                # Há uma aula agendada - verificar se é o professor correto
                if current_class['teacher_id'] == teacher_id:
                    # Professor correto
                    subject = current_class.get('subject', 'Sem assunto')
                    self.db.add_access_log(room_id, teacher_id, f"AUTORIZADO - {subject}", current_class['id'])
                    message = f"Acesso autorizado!\nDisciplina: {subject}"
                    return True, teacher_data, message, current_class
                else:
                    # Professor errado tentando acessar sala reservada
                    scheduled_teacher = self.db.get_teacher(current_class['teacher_id'])
                    teacher_name = scheduled_teacher['name'] if scheduled_teacher else "outro professor"
                    subject = current_class.get('subject', 'Sem assunto')
                    self.db.add_access_log(room_id, teacher_id, f"NEGADO - Sala reservada para {teacher_name}", current_class['id'])
                    message = f"Acesso negado!\nEsta sala está reservada para {teacher_name}\nDisciplina: {subject}"
                    return False, teacher_data, message, current_class
            else:
                # Não há aula agendada no momento - negar acesso
                # Se não há aula cadastrada, não permite acesso
                self.db.add_access_log(room_id, teacher_id, "NEGADO - Sem aula agendada", None)
                message = "Acesso negado!\nNão há aula cadastrada nesta sala no momento."
                return False, teacher_data, message, None

        except Exception as e:
            return False, None, f"Erro na autenticação: {str(e)}", None

    def _find_current_class(self, room_id: int) -> Optional[Dict]:
        """
        Busca aula correspondente ao momento atual (10min antes até o fim)

        Args:
            room_id: ID da sala

        Returns:
            Dicionário com dados da aula ou None
        """
        # Obter aulas desta sala
        classes = self.db.get_classes_by_room(room_id)

        now = datetime.now()

        # Mapear dia da semana atual
        weekday_map = {
            0: "Segunda",
            1: "Terça",
            2: "Quarta",
            3: "Quinta",
            4: "Sexta",
            5: "Sábado",
            6: "Domingo"
        }
        current_day = weekday_map[now.weekday()]

        for cls in classes:
            # Verificar se é o dia da semana correto
            if cls['day_of_week'] == current_day:
                # Verificar se está no horário permitido (10min antes até fim)
                try:
                    start_time = datetime.strptime(cls['start_time'], '%H:%M').time()
                    end_time = datetime.strptime(cls['end_time'], '%H:%M').time()

                    class_start = datetime.combine(now.date(), start_time)
                    class_end = datetime.combine(now.date(), end_time)

                    allowed_start = class_start - timedelta(minutes=10)

                    if allowed_start <= now <= class_end:
                        return cls
                except:
                    continue

        return None

    def get_room_logs(self, room_id: int) -> List[Dict]:
        """Retorna o histórico de acessos de uma sala"""
        return self.db.get_room_logs(room_id)
