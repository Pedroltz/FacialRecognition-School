import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class RegisterClassWindow(Gtk.Window):
    def __init__(self, parent, controller):
        super().__init__(transient_for=parent, title="Cadastrar Aula")
        self.controller = controller
        self.set_default_size(600, 450)

        # Box principal vertical
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        self.set_child(main_box)

        # Título
        title_label = Gtk.Label(label="Cadastro de Aula")
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
        grid.set_vexpand(True)
        grid.set_valign(Gtk.Align.CENTER)
        main_box.append(grid)

        # Dropdown de Salas
        room_label = Gtk.Label(label="Sala:")
        room_label.set_halign(Gtk.Align.END)
        room_label.set_size_request(120, -1)
        self.room_dropdown = Gtk.DropDown()
        self.room_dropdown.set_size_request(300, -1)
        self.room_model = Gtk.StringList()
        self.room_dropdown.set_model(self.room_model)
        grid.attach(room_label, 0, 0, 1, 1)
        grid.attach(self.room_dropdown, 1, 0, 1, 1)

        # Dropdown de Professores
        teacher_label = Gtk.Label(label="Professor:")
        teacher_label.set_halign(Gtk.Align.END)
        teacher_label.set_size_request(120, -1)
        self.teacher_dropdown = Gtk.DropDown()
        self.teacher_dropdown.set_size_request(300, -1)
        self.teacher_model = Gtk.StringList()
        self.teacher_dropdown.set_model(self.teacher_model)
        grid.attach(teacher_label, 0, 1, 1, 1)
        grid.attach(self.teacher_dropdown, 1, 1, 1, 1)

        # Campo Data
        date_label = Gtk.Label(label="Data:")
        date_label.set_halign(Gtk.Align.END)
        date_label.set_size_request(120, -1)
        self.date_entry = Gtk.Entry()
        self.date_entry.set_size_request(300, -1)
        self.date_entry.set_placeholder_text("DD/MM/YYYY")
        grid.attach(date_label, 0, 2, 1, 1)
        grid.attach(self.date_entry, 1, 2, 1, 1)

        # Campo Horário Início
        start_label = Gtk.Label(label="Hora Início:")
        start_label.set_halign(Gtk.Align.END)
        start_label.set_size_request(120, -1)
        self.start_entry = Gtk.Entry()
        self.start_entry.set_size_request(300, -1)
        self.start_entry.set_placeholder_text("HH:MM")
        grid.attach(start_label, 0, 3, 1, 1)
        grid.attach(self.start_entry, 1, 3, 1, 1)

        # Campo Horário Fim
        end_label = Gtk.Label(label="Hora Fim:")
        end_label.set_halign(Gtk.Align.END)
        end_label.set_size_request(120, -1)
        self.end_entry = Gtk.Entry()
        self.end_entry.set_size_request(300, -1)
        self.end_entry.set_placeholder_text("HH:MM")
        grid.attach(end_label, 0, 4, 1, 1)
        grid.attach(self.end_entry, 1, 4, 1, 1)

        # Campo Disciplina
        subject_label = Gtk.Label(label="Disciplina:")
        subject_label.set_halign(Gtk.Align.END)
        subject_label.set_size_request(120, -1)
        self.subject_entry = Gtk.Entry()
        self.subject_entry.set_size_request(300, -1)
        self.subject_entry.set_placeholder_text("Nome da disciplina (opcional)")
        grid.attach(subject_label, 0, 5, 1, 1)
        grid.attach(self.subject_entry, 1, 5, 1, 1)

        # Separador
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator2)

        # Botão salvar
        save_btn = Gtk.Button(label="Salvar Aula")
        save_btn.add_css_class("suggested-action")
        save_btn.set_halign(Gtk.Align.CENTER)
        save_btn.connect("clicked", self.on_save_clicked)
        main_box.append(save_btn)

        # Label de status
        self.status_label = Gtk.Label(label="")
        self.status_label.set_wrap(True)
        self.status_label.set_halign(Gtk.Align.CENTER)
        main_box.append(self.status_label)

        # Popular dropdowns
        self.populate_dropdowns()

    def populate_dropdowns(self):
        """Popula os dropdowns de salas e professores"""
        # Salas
        rooms = self.controller.get_all_rooms()
        self.rooms_data = {}
        for idx, room in enumerate(rooms):
            self.room_model.append(room['name'])
            self.rooms_data[idx] = room

        # Professores
        teachers = self.controller.get_all_teachers()
        self.teachers_data = {}
        for idx, teacher in enumerate(teachers):
            self.teacher_model.append(teacher['name'])
            self.teachers_data[idx] = teacher

    def on_save_clicked(self, button):
        """Salva a aula"""
        room_idx = self.room_dropdown.get_selected()
        teacher_idx = self.teacher_dropdown.get_selected()
        date = self.date_entry.get_text().strip()
        start_time = self.start_entry.get_text().strip()
        end_time = self.end_entry.get_text().strip()
        subject = self.subject_entry.get_text().strip()

        if not all([date, start_time, end_time]):
            self.status_label.set_text("Preencha os campos obrigatórios (sala, professor, data, horários)!")
            return

        room = self.rooms_data.get(room_idx)
        teacher = self.teachers_data.get(teacher_idx)

        if not room or not teacher:
            self.status_label.set_text("Selecione uma sala e um professor!")
            return

        success, message = self.controller.create_class(
            room['id'], teacher['id'], date, start_time, end_time, subject
        )

        self.status_label.set_text(message)

        if success:
            GLib.timeout_add_seconds(2, self.close)
