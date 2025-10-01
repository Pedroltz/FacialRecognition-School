import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf, GLib
import cv2
import os

class RegisterTeacherWindow(Gtk.Window):
    def __init__(self, parent, controller):
        super().__init__(transient_for=parent, title="Cadastrar Professor")
        self.controller = controller
        self.set_default_size(700, 750)
        self.captured_photo = None

        # Box principal vertical
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        self.set_child(main_box)

        # Título
        title_label = Gtk.Label(label="Cadastro de Professor")
        title_label.add_css_class("title-2")
        title_label.set_halign(Gtk.Align.CENTER)
        main_box.append(title_label)

        # Separador
        separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator1)

        # Grid para campos de formulário
        grid = Gtk.Grid()
        grid.set_row_spacing(8)
        grid.set_column_spacing(10)
        grid.set_halign(Gtk.Align.CENTER)
        main_box.append(grid)

        # Campo Nome
        name_label = Gtk.Label(label="Nome:")
        name_label.set_halign(Gtk.Align.END)
        name_label.set_size_request(80, -1)
        self.name_entry = Gtk.Entry()
        self.name_entry.set_size_request(400, -1)
        self.name_entry.set_placeholder_text("Nome completo")
        grid.attach(name_label, 0, 0, 1, 1)
        grid.attach(self.name_entry, 1, 0, 1, 1)

        # Campo Idade
        age_label = Gtk.Label(label="Idade:")
        age_label.set_halign(Gtk.Align.END)
        age_label.set_size_request(80, -1)
        self.age_entry = Gtk.Entry()
        self.age_entry.set_size_request(400, -1)
        self.age_entry.set_placeholder_text("Idade")
        grid.attach(age_label, 0, 1, 1, 1)
        grid.attach(self.age_entry, 1, 1, 1, 1)

        # Campo Telefone
        phone_label = Gtk.Label(label="Telefone:")
        phone_label.set_halign(Gtk.Align.END)
        phone_label.set_size_request(80, -1)
        self.phone_entry = Gtk.Entry()
        self.phone_entry.set_size_request(400, -1)
        self.phone_entry.set_placeholder_text("(00) 00000-0000")
        grid.attach(phone_label, 0, 2, 1, 1)
        grid.attach(self.phone_entry, 1, 2, 1, 1)

        # Campo Email
        email_label = Gtk.Label(label="Email:")
        email_label.set_halign(Gtk.Align.END)
        email_label.set_size_request(80, -1)
        self.email_entry = Gtk.Entry()
        self.email_entry.set_size_request(400, -1)
        self.email_entry.set_placeholder_text("email@exemplo.com")
        grid.attach(email_label, 0, 3, 1, 1)
        grid.attach(self.email_entry, 1, 3, 1, 1)

        # Separador
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator2)

        # Label foto
        photo_label = Gtk.Label(label="Foto")
        photo_label.set_halign(Gtk.Align.CENTER)
        main_box.append(photo_label)

        # Frame para foto
        photo_frame = Gtk.Frame()
        photo_frame.set_halign(Gtk.Align.CENTER)

        # Área de foto
        self.photo_preview = Gtk.Image()
        self.photo_preview.set_size_request(400, 300)
        self.photo_preview.set_pixel_size(400)
        photo_frame.set_child(self.photo_preview)
        main_box.append(photo_frame)

        # Separador
        separator3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator3)

        # Botões
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        main_box.append(button_box)

        capture_btn = Gtk.Button(label="Capturar Foto")
        capture_btn.connect("clicked", self.on_capture_clicked)
        button_box.append(capture_btn)

        save_btn = Gtk.Button(label="Salvar Cadastro")
        save_btn.add_css_class("suggested-action")
        save_btn.connect("clicked", self.on_save_clicked)
        button_box.append(save_btn)

        # Label de status
        self.status_label = Gtk.Label(label="")
        self.status_label.set_wrap(True)
        self.status_label.set_halign(Gtk.Align.CENTER)
        main_box.append(self.status_label)

    def on_capture_clicked(self, button):
        """Abre a câmera para capturar foto"""
        capture_window = CaptureWindow(self, self.controller)
        capture_window.present()

    def set_captured_photo(self, photo_path: str):
        """Define a foto capturada"""
        self.captured_photo = photo_path

        try:
            # Carregar foto original
            pixbuf_original = GdkPixbuf.Pixbuf.new_from_file(photo_path)

            # Redimensionar para 400x300
            pixbuf_scaled = pixbuf_original.scale_simple(400, 300, GdkPixbuf.InterpType.BILINEAR)

            # Exibir
            self.photo_preview.set_from_pixbuf(pixbuf_scaled)
            self.status_label.set_text("Foto capturada com sucesso!")
        except Exception as e:
            self.status_label.set_text(f"Erro ao carregar foto: {e}")

    def on_save_clicked(self, button):
        """Salva o cadastro do professor"""
        name = self.name_entry.get_text().strip()
        age_text = self.age_entry.get_text().strip()
        phone = self.phone_entry.get_text().strip()
        email = self.email_entry.get_text().strip()

        if not all([name, age_text, phone, email, self.captured_photo]):
            self.status_label.set_text("Preencha todos os campos e capture uma foto!")
            return

        try:
            age = int(age_text)
        except ValueError:
            self.status_label.set_text("Idade deve ser um número válido!")
            return

        success, message = self.controller.register_teacher(
            name, age, phone, email, self.captured_photo
        )

        self.status_label.set_text(message)

        if success:
            GLib.timeout_add_seconds(2, self.close)


class CaptureWindow(Gtk.Window):
    def __init__(self, parent, controller):
        super().__init__(transient_for=parent, title="Capturar Foto")
        self.controller = controller
        self.parent_window = parent
        self.set_default_size(680, 600)
        self.camera = None
        self.camera_timeout_id = None
        self.current_frame = None

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.set_child(main_box)

        # Label de status no topo
        self.status_label = Gtk.Label(label="Aguarde, inicializando câmera...")
        self.status_label.set_wrap(True)
        main_box.append(self.status_label)

        # Área de vídeo com Image (sem frame para manter tamanho)
        self.video_image = Gtk.Image()
        self.video_image.set_size_request(640, 480)
        self.video_image.set_pixel_size(640)
        main_box.append(self.video_image)

        # Botão capturar
        capture_btn = Gtk.Button(label="Capturar Foto")
        capture_btn.connect("clicked", self.on_capture_clicked)
        main_box.append(capture_btn)

        # Conectar sinal de fechamento
        self.connect("close-request", self.on_close_request)

        # Iniciar câmera com delay
        GLib.timeout_add(500, self.init_camera)

    def init_camera(self):
        """Inicializa a câmera"""
        try:
            self.camera = cv2.VideoCapture(0)

            # Configurar resolução
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            if not self.camera.isOpened():
                self.status_label.set_text("✗ Erro: Não foi possível abrir a câmera!")
                return False

            # Descartar primeiros frames (warm-up)
            for _ in range(3):
                self.camera.read()

            self.status_label.set_text("✓ Câmera pronta! Posicione seu rosto e clique em 'Capturar Foto'")
            self.camera_timeout_id = GLib.timeout_add(66, self.update_frame)  # 15 FPS
            return False
        except Exception as e:
            self.status_label.set_text(f"✗ Erro ao inicializar câmera: {str(e)}")
            return False

    def update_frame(self):
        """Atualiza o frame da câmera"""
        if not self.camera or not self.camera.isOpened():
            return False

        ret, frame = self.camera.read()
        if not ret or frame is None:
            return True

        try:
            self.current_frame = frame.copy()

            # Converter para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Redimensionar para tamanho fixo 640x480
            frame_resized = cv2.resize(frame_rgb, (640, 480))

            # Manter buffer em memória
            self._frame_bytes = frame_resized.tobytes()

            # Criar pixbuf com tamanho fixo
            pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                GLib.Bytes.new(self._frame_bytes),
                GdkPixbuf.Colorspace.RGB,
                False,
                8,
                640,
                480,
                640 * 3
            )

            # Atualizar Image
            self.video_image.set_from_pixbuf(pixbuf)

            return True
        except Exception as e:
            print(f"Erro ao atualizar frame: {e}")
            return True

    def on_capture_clicked(self, button):
        """Captura a foto atual"""
        if self.current_frame is None:
            self.status_label.set_text("✗ Aguarde a câmera inicializar!")
            return

        try:
            # Salvar foto
            photo_path = f"data/faces/teacher_{GLib.get_real_time()}.jpg"
            os.makedirs(os.path.dirname(photo_path), exist_ok=True)
            cv2.imwrite(photo_path, self.current_frame, [cv2.IMWRITE_JPEG_QUALITY, 95])

            # Notificar janela pai
            self.parent_window.set_captured_photo(photo_path)

            # Fechar janela
            self.cleanup_camera()
            self.close()
        except Exception as e:
            self.status_label.set_text(f"✗ Erro ao capturar foto: {e}")

    def on_close_request(self, window):
        """Manipula o fechamento da janela"""
        self.cleanup_camera()
        return False

    def cleanup_camera(self):
        """Libera recursos da câmera"""
        # Parar atualização de frames
        if self.camera_timeout_id:
            GLib.source_remove(self.camera_timeout_id)
            self.camera_timeout_id = None

        # Liberar câmera
        if self.camera and self.camera.isOpened():
            self.camera.release()
            self.camera = None

        self.current_frame = None
