import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk
import cv2  # Para captura de vídeo

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app, controller):
        super().__init__(application=app, title="Sistema de Gerenciamento de Salas")
        self.controller = controller
        self.set_default_size(900, 700)

        # Controle de câmera
        self.camera = None
        self.camera_timeout_id = None
        self.camera_init_timeout_id = None
        self.current_room_id = None

        # Controle de janelas
        self.register_teacher_window = None
        self.register_room_window = None
        self.register_class_window = None
        self.manage_window = None

        # Container principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.set_child(main_box)

        # Título
        title = Gtk.Label(label="Sistema de Gerenciamento de Salas com Reconhecimento Facial")
        title.add_css_class("title-1")
        main_box.append(title)

        # Container de botões superiores
        top_button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        top_button_box.set_halign(Gtk.Align.CENTER)
        main_box.append(top_button_box)

        # Botão cadastrar professor
        register_teacher_btn = Gtk.Button(label="Cadastrar Professor")
        register_teacher_btn.connect("clicked", self.on_register_teacher_clicked)
        top_button_box.append(register_teacher_btn)

        # Botão cadastrar sala
        register_room_btn = Gtk.Button(label="Cadastrar Sala")
        register_room_btn.connect("clicked", self.on_register_room_clicked)
        top_button_box.append(register_room_btn)

        # Botão cadastrar aula
        register_class_btn = Gtk.Button(label="Cadastrar Aula")
        register_class_btn.connect("clicked", self.on_register_class_clicked)
        top_button_box.append(register_class_btn)

        # Botão gerenciar
        manage_btn = Gtk.Button(label="Gerenciar")
        manage_btn.connect("clicked", self.on_manage_clicked)
        top_button_box.append(manage_btn)

        # Separador
        separator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator1)

        # Label de seleção
        select_label = Gtk.Label(label="Selecione uma sala para monitorar:")
        main_box.append(select_label)

        # Dropdown de salas
        self.room_dropdown = Gtk.DropDown()
        self.room_model = Gtk.StringList()
        self.room_dropdown.set_model(self.room_model)
        main_box.append(self.room_dropdown)

        # Conectar sinal do dropdown ANTES de popular
        self.room_dropdown.connect("notify::selected", self.on_room_selected)

        # Popular dropdown
        self.update_room_list()

        # Container de monitoramento (inicialmente oculto)
        self.monitor_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.monitor_box.set_visible(False)
        main_box.append(self.monitor_box)

        # Container horizontal: Vídeo + Informações
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        content_box.set_halign(Gtk.Align.CENTER)
        self.monitor_box.append(content_box)

        # Área de vídeo
        self.video_frame = Gtk.Picture()
        self.video_frame.set_size_request(640, 480)
        content_box.append(self.video_frame)

        # Container de informações ao lado do vídeo
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        info_box.set_size_request(300, -1)
        content_box.append(info_box)

        # Título das informações
        info_title = Gtk.Label(label="Horários da Sala")
        info_title.add_css_class("title-3")
        info_title.set_halign(Gtk.Align.START)
        info_box.append(info_title)

        # Label de informações da aula (com scroll)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(300, 350)
        info_box.append(scrolled)

        self.class_info_label = Gtk.Label(label="")
        self.class_info_label.set_wrap(True)
        self.class_info_label.set_halign(Gtk.Align.START)
        self.class_info_label.set_valign(Gtk.Align.START)
        scrolled.set_child(self.class_info_label)

        # Botão de autenticar centralizado abaixo
        auth_btn = Gtk.Button(label="Autenticar")
        auth_btn.add_css_class("suggested-action")
        auth_btn.set_size_request(200, 40)
        auth_btn.set_halign(Gtk.Align.CENTER)
        auth_btn.connect("clicked", self.on_authenticate_clicked)
        self.monitor_box.append(auth_btn)

        # Conectar fechamento da janela
        self.connect("close-request", self.on_close_request)

    def update_room_list(self):
        """Atualiza a lista de salas no dropdown"""
        # Bloquear sinal temporariamente
        self.room_dropdown.handler_block_by_func(self.on_room_selected)

        # Limpar modelo
        self.room_model.splice(0, self.room_model.get_n_items())

        # Adicionar opção padrão
        self.room_model.append("Nenhum")

        # Obter e adicionar salas
        rooms = self.controller.get_all_rooms()
        self.rooms_data = {0: None}  # Índice 0 = Nenhum

        for idx, room in enumerate(rooms, start=1):
            self.room_model.append(f"{room['name']}")
            self.rooms_data[idx] = room

        # Selecionar "Nenhum"
        self.room_dropdown.set_selected(0)

        # Desbloquear sinal
        self.room_dropdown.handler_unblock_by_func(self.on_room_selected)

    def on_room_selected(self, dropdown, param):
        """Callback quando uma sala é selecionada"""
        selected_idx = dropdown.get_selected()
        room_data = self.rooms_data.get(selected_idx)

        # Se for "Nenhum", ocultar monitoramento
        if room_data is None:
            self.monitor_box.set_visible(False)
            self.cleanup_camera()
            self.current_room_id = None
            return

        # Se for a mesma sala já selecionada, não reiniciar câmera
        if self.current_room_id == room_data['id']:
            return

        self.current_room_id = room_data['id']

        # Limpar câmera anterior se existir
        self.cleanup_camera()

        # Mostrar área de monitoramento
        self.monitor_box.set_visible(True)

        # Buscar aulas agendadas para esta sala
        self.update_class_info(room_data['id'])

        # Inicializar câmera com delay
        self.camera_init_timeout_id = GLib.timeout_add(500, self.init_camera)

    def update_class_info(self, room_id):
        """Atualiza informações das aulas agendadas"""
        classes = self.controller.get_classes_by_room(room_id)

        if not classes:
            self.class_info_label.set_text("Nenhuma aula agendada.")
            return

        info_text = ""
        for cls in classes:
            from datetime import datetime
            try:
                date_obj = datetime.strptime(cls['date'], '%Y-%m-%d')
                date_br = date_obj.strftime('%d/%m/%Y')
            except:
                date_br = cls['date']

            info_text += f"{date_br}\n"
            info_text += f"{cls['start_time']} - {cls['end_time']}\n"
            info_text += f"Professor: {cls['teacher_name']}\n"
            if cls.get('subject'):
                info_text += f"Disciplina: {cls['subject']}\n"
            info_text += "\n"

        self.class_info_label.set_text(info_text.strip())

    def init_camera(self):
        """Inicializa a câmera"""
        try:
            self.camera = cv2.VideoCapture(0)

            if not self.camera.isOpened():
                self.show_error_dialog("Não foi possível abrir a câmera!")
                self.camera_init_timeout_id = None
                return False

            self.camera_timeout_id = GLib.timeout_add(66, self.update_frame)
            self.camera_init_timeout_id = None
            return False
        except Exception as e:
            self.show_error_dialog(f"Erro ao inicializar câmera: {str(e)}")
            self.camera_init_timeout_id = None
            return False

    def update_frame(self):
        """Atualiza o frame da câmera"""
        if not self.camera or not self.camera.isOpened():
            return False

        ret, frame = self.camera.read()
        if ret:
            self.current_frame = frame

            # Converter para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Redimensionar mantendo proporção
            target_width = 640
            target_height = 480
            h, w = frame_rgb.shape[:2]
            aspect = w / h

            if aspect > (target_width / target_height):
                new_width = target_width
                new_height = int(target_width / aspect)
            else:
                new_height = target_height
                new_width = int(target_height * aspect)

            frame_resized = cv2.resize(frame_rgb, (new_width, new_height))

            # Manter referência ao buffer para evitar garbage collection
            self._frame_data = frame_resized.tobytes()

            # Converter diretamente para GdkPixbuf (sem disco)
            pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(
                GLib.Bytes.new(self._frame_data),
                GdkPixbuf.Colorspace.RGB,
                False,
                8,
                new_width,
                new_height,
                new_width * 3
            )

            texture = Gdk.Texture.new_for_pixbuf(pixbuf)
            self.video_frame.set_paintable(texture)
            return True

        return False

    def on_authenticate_clicked(self, button):
        """Realiza autenticação facial"""
        if not hasattr(self, 'current_frame') or self.current_room_id is None:
            self.show_error_dialog("Câmera não está pronta ou sala não selecionada!")
            return

        success, teacher_data, message, class_data = self.controller.authenticate_teacher_in_room(
            self.current_frame, self.current_room_id
        )

        if success:
            # Construir mensagem de sucesso
            result_text = f"Professor: {teacher_data['name']}\n"
            result_text += f"Email: {teacher_data['email']}\n"
            result_text += f"Telefone: {teacher_data['phone']}\n"

            if class_data:
                from datetime import datetime
                try:
                    date_obj = datetime.strptime(class_data['date'], '%Y-%m-%d')
                    date_br = date_obj.strftime('%d/%m/%Y')
                except:
                    date_br = class_data['date']

                result_text += f"\nAula Agendada:\n"
                result_text += f"Data: {date_br}\n"
                result_text += f"Horário: {class_data['start_time']} - {class_data['end_time']}\n"
                if class_data.get('subject'):
                    result_text += f"Disciplina: {class_data['subject']}"

            self.show_success_dialog("Acesso Autorizado!", result_text)
        else:
            self.show_error_dialog(message)

    def show_success_dialog(self, title, details):
        """Mostra um diálogo de sucesso"""
        dialog = Gtk.AlertDialog()
        dialog.set_message(title)
        dialog.set_detail(details)
        dialog.set_buttons(["OK"])
        dialog.set_default_button(0)
        dialog.choose(self, None, lambda d, r: None)

    def show_error_dialog(self, message):
        """Mostra um diálogo de erro"""
        dialog = Gtk.AlertDialog()
        dialog.set_message("Acesso Negado!")
        dialog.set_detail(message)
        dialog.set_buttons(["OK"])
        dialog.set_default_button(0)
        dialog.choose(self, None, lambda d, r: None)

    def cleanup_camera(self):
        """Libera recursos da câmera"""
        if self.camera_init_timeout_id:
            GLib.source_remove(self.camera_init_timeout_id)
            self.camera_init_timeout_id = None

        if self.camera_timeout_id:
            GLib.source_remove(self.camera_timeout_id)
            self.camera_timeout_id = None

        if self.camera and self.camera.isOpened():
            self.camera.release()
            self.camera = None

    def on_close_request(self, window):
        """Manipula o fechamento da janela principal"""
        self.cleanup_camera()
        return False

    # Callbacks dos botões
    def on_register_teacher_clicked(self, button):
        """Abre janela de cadastro de professor"""
        if self.register_teacher_window is not None:
            self.register_teacher_window.present()
            return

        from src.views.register_teacher_window import RegisterTeacherWindow
        self.register_teacher_window = RegisterTeacherWindow(self, self.controller)
        self.register_teacher_window.connect("close-request", self.on_register_teacher_window_closed)
        self.register_teacher_window.present()

    def on_register_teacher_window_closed(self, window):
        """Callback quando janela de cadastro de professor é fechada"""
        self.register_teacher_window = None
        return False

    def on_register_room_clicked(self, button):
        """Abre janela de cadastro de sala"""
        if self.register_room_window is not None:
            self.register_room_window.present()
            return

        from src.views.register_room_window import RegisterRoomWindow
        self.register_room_window = RegisterRoomWindow(self, self.controller)
        self.register_room_window.connect("close-request", self.on_register_room_window_closed)
        self.register_room_window.present()

    def on_register_room_window_closed(self, window):
        """Callback quando janela de cadastro de sala é fechada"""
        self.register_room_window = None
        self.update_room_list()
        return False

    def on_register_class_clicked(self, button):
        """Abre janela de cadastro de aula"""
        if self.register_class_window is not None:
            self.register_class_window.present()
            return

        from src.views.register_class_window import RegisterClassWindow
        self.register_class_window = RegisterClassWindow(self, self.controller)
        self.register_class_window.connect("close-request", self.on_register_class_window_closed)
        self.register_class_window.present()

    def on_register_class_window_closed(self, window):
        """Callback quando janela de cadastro de aula é fechada"""
        self.register_class_window = None
        self.update_room_list()
        return False

    def on_manage_clicked(self, button):
        """Abre janela de gerenciamento"""
        if self.manage_window is not None:
            self.manage_window.present()
            return

        from src.views.manage_window import ManageWindow
        self.manage_window = ManageWindow(self, self.controller)
        self.manage_window.connect("close-request", self.on_manage_window_closed)
        self.manage_window.present()

    def on_manage_window_closed(self, window):
        """Callback quando janela de gerenciamento é fechada"""
        self.manage_window = None
        self.update_room_list()
        return False
