import face_recognition
import numpy as np
import cv2
import pickle
from typing import Optional, List, Tuple

class FaceRecognizer:
    def __init__(self, tolerance: float = 0.6):
        """
        Inicializa o reconhecedor facial

        Args:
            tolerance: Tolerância para comparação de faces (quanto menor, mais rigoroso)
        """
        self.tolerance = tolerance

    def encode_face(self, image_path: str) -> Optional[np.ndarray]:
        """
        Gera o encoding de uma face a partir de uma imagem

        Args:
            image_path: Caminho da imagem

        Returns:
            Array numpy com o encoding da face ou None se nenhuma face for detectada
        """
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            return face_encodings[0]
        return None

    def encode_face_from_frame(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Gera o encoding de uma face a partir de um frame de vídeo

        Args:
            frame: Frame capturado da câmera

        Returns:
            Array numpy com o encoding da face ou None se nenhuma face for detectada
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_frame)

        if len(face_encodings) > 0:
            return face_encodings[0]
        return None

    def compare_faces(self, known_encoding: np.ndarray,
                     unknown_encoding: np.ndarray) -> bool:
        """
        Compara dois encodings de faces

        Args:
            known_encoding: Encoding conhecido (do banco de dados)
            unknown_encoding: Encoding a ser comparado

        Returns:
            True se as faces correspondem, False caso contrário
        """
        results = face_recognition.compare_faces(
            [known_encoding],
            unknown_encoding,
            tolerance=self.tolerance
        )
        return results[0]

    def find_match(self, unknown_encoding: np.ndarray,
                   known_encodings: List[Tuple[int, np.ndarray]]) -> Optional[int]:
        """
        Busca uma correspondência entre um encoding desconhecido e uma lista de encodings conhecidos

        Args:
            unknown_encoding: Encoding a ser identificado
            known_encodings: Lista de tuplas (user_id, encoding)

        Returns:
            ID do usuário correspondente ou None se não houver correspondência
        """
        for user_id, known_encoding in known_encodings:
            if self.compare_faces(known_encoding, unknown_encoding):
                return user_id
        return None

    def detect_faces_in_frame(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detecta faces em um frame

        Args:
            frame: Frame capturado da câmera

        Returns:
            Lista de tuplas com as coordenadas (top, right, bottom, left) de cada face
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        return face_locations

    @staticmethod
    def encoding_to_bytes(encoding: np.ndarray) -> bytes:
        """Converte um encoding para bytes para armazenamento"""
        return pickle.dumps(encoding)

    @staticmethod
    def bytes_to_encoding(data: bytes) -> np.ndarray:
        """Converte bytes de volta para encoding"""
        return pickle.loads(data)
