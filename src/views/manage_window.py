import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class ManageWindow(Gtk.Window):
    def __init__(self, parent, controller):
        super().__init__(transient_for=parent, title="Gerenciar")
        self.controller = controller
        self.set_default_size(800, 600)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.set_child(main_box)

        # Notebook (abas)
        notebook = Gtk.Notebook()
        main_box.append(notebook)

        # Aba Professores
        teachers_box = self.create_teachers_tab()
        notebook.append_page(teachers_box, Gtk.Label(label="Professores"))

        # Aba Salas
        rooms_box = self.create_rooms_tab()
        notebook.append_page(rooms_box, Gtk.Label(label="Salas"))

        # Aba Aulas
        classes_box = self.create_classes_tab()
        notebook.append_page(classes_box, Gtk.Label(label="Aulas"))

    def create_teachers_tab(self):
        """Cria aba de gerenciamento de professores"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)

        # Título
        title = Gtk.Label(label="Gerenciar Professores")
        title.add_css_class("title-3")
        box.append(title)

        # ScrolledWindow com lista
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.append(scrolled)

        # ListBox para professores
        self.teachers_listbox = Gtk.ListBox()
        self.teachers_listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.teachers_listbox.add_css_class("boxed-list")
        scrolled.set_child(self.teachers_listbox)

        # Botões de ação
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(10)
        box.append(button_box)

        refresh_btn = Gtk.Button(label="Atualizar")
        refresh_btn.connect("clicked", lambda b: self.update_teachers_list())
        button_box.append(refresh_btn)

        delete_btn = Gtk.Button(label="Excluir Selecionados")
        delete_btn.add_css_class("destructive-action")
        delete_btn.connect("clicked", self.on_delete_selected_teachers)
        button_box.append(delete_btn)

        # Label de status
        self.teachers_status_label = Gtk.Label(label="")
        box.append(self.teachers_status_label)

        # Atualizar lista
        self.update_teachers_list()

        return box

    def update_teachers_list(self):
        """Atualiza lista de professores"""
        # Limpar lista
        while True:
            row = self.teachers_listbox.get_row_at_index(0)
            if row is None:
                break
            self.teachers_listbox.remove(row)

        teachers = self.controller.get_all_teachers()

        if not teachers:
            label = Gtk.Label(label="Nenhum professor cadastrado")
            self.teachers_listbox.append(label)
            return

        for teacher in teachers:
            # Box para cada item
            row_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            row_box.set_margin_top(10)
            row_box.set_margin_bottom(10)
            row_box.set_margin_start(10)
            row_box.set_margin_end(10)

            # Nome em destaque
            name_label = Gtk.Label(label=teacher['name'])
            name_label.add_css_class("title-4")
            name_label.set_halign(Gtk.Align.START)
            row_box.append(name_label)

            # Informações
            info_label = Gtk.Label(
                label=f"ID: {teacher['id']} | Idade: {teacher['age']} | Tel: {teacher['phone']} | Email: {teacher['email']}"
            )
            info_label.set_halign(Gtk.Align.START)
            row_box.append(info_label)

            # Adicionar row com dados do professor
            row = Gtk.ListBoxRow()
            row.set_child(row_box)
            row.teacher_data = teacher
            self.teachers_listbox.append(row)

    def on_delete_selected_teachers(self, button):
        """Exclui professores selecionados"""
        selected_rows = []

        # Coletar todas as rows selecionadas
        def collect_selected(row):
            if hasattr(row, 'teacher_data'):
                selected_rows.append(row)

        self.teachers_listbox.selected_foreach(collect_selected)

        if not selected_rows:
            self.teachers_status_label.set_text("Selecione pelo menos um professor para excluir!")
            return

        # Preparar lista de IDs
        teacher_ids = [row.teacher_data['id'] for row in selected_rows]
        count = len(teacher_ids)

        # Diálogo de confirmação
        dialog = Gtk.AlertDialog()
        dialog.set_message(f"Excluir {count} professor(es)?")
        dialog.set_detail(f"Tem certeza que deseja excluir {count} professor(es) selecionado(s)?")
        dialog.set_buttons(["Cancelar", "Excluir"])
        dialog.set_cancel_button(0)
        dialog.set_default_button(1)

        dialog.choose(self, None, self.process_delete_teachers, teacher_ids)

    def process_delete_teachers(self, dialog, result, teacher_ids):
        """Processa exclusão de professores"""
        try:
            button_index = dialog.choose_finish(result)
            if button_index == 1:  # Excluir
                deleted_count = 0
                for teacher_id in teacher_ids:
                    if self.controller.delete_teacher(teacher_id):
                        deleted_count += 1

                self.teachers_status_label.set_text(f"{deleted_count} professor(es) excluído(s) com sucesso!")
                self.update_teachers_list()
        except Exception as e:
            self.teachers_status_label.set_text(f"Erro: {str(e)}")

    def create_rooms_tab(self):
        """Cria aba de gerenciamento de salas"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)

        # Título
        title = Gtk.Label(label="Gerenciar Salas")
        title.add_css_class("title-3")
        box.append(title)

        # ScrolledWindow com lista
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.append(scrolled)

        # ListBox para salas
        self.rooms_listbox = Gtk.ListBox()
        self.rooms_listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.rooms_listbox.add_css_class("boxed-list")
        scrolled.set_child(self.rooms_listbox)

        # Botões de ação
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(10)
        box.append(button_box)

        refresh_btn = Gtk.Button(label="Atualizar")
        refresh_btn.connect("clicked", lambda b: self.update_rooms_list())
        button_box.append(refresh_btn)

        delete_btn = Gtk.Button(label="Excluir Selecionados")
        delete_btn.add_css_class("destructive-action")
        delete_btn.connect("clicked", self.on_delete_selected_rooms)
        button_box.append(delete_btn)

        # Label de status
        self.rooms_status_label = Gtk.Label(label="")
        box.append(self.rooms_status_label)

        # Atualizar lista
        self.update_rooms_list()

        return box

    def update_rooms_list(self):
        """Atualiza lista de salas"""
        # Limpar lista
        while True:
            row = self.rooms_listbox.get_row_at_index(0)
            if row is None:
                break
            self.rooms_listbox.remove(row)

        rooms = self.controller.get_all_rooms()

        if not rooms:
            label = Gtk.Label(label="Nenhuma sala cadastrada")
            self.rooms_listbox.append(label)
            return

        for room in rooms:
            # Box para cada item
            row_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            row_box.set_margin_top(10)
            row_box.set_margin_bottom(10)
            row_box.set_margin_start(10)
            row_box.set_margin_end(10)

            # Nome em destaque
            name_label = Gtk.Label(label=room['name'])
            name_label.add_css_class("title-4")
            name_label.set_halign(Gtk.Align.START)
            row_box.append(name_label)

            # Informações
            info_text = f"ID: {room['id']}"
            if room.get('description'):
                info_text += f" | Descrição: {room['description']}"
            info_label = Gtk.Label(label=info_text)
            info_label.set_halign(Gtk.Align.START)
            row_box.append(info_label)

            # Adicionar row com dados da sala
            row = Gtk.ListBoxRow()
            row.set_child(row_box)
            row.room_data = room
            self.rooms_listbox.append(row)

    def on_delete_selected_rooms(self, button):
        """Exclui salas selecionadas"""
        selected_rows = []

        # Coletar todas as rows selecionadas
        def collect_selected(row):
            if hasattr(row, 'room_data'):
                selected_rows.append(row)

        self.rooms_listbox.selected_foreach(collect_selected)

        if not selected_rows:
            self.rooms_status_label.set_text("Selecione pelo menos uma sala para excluir!")
            return

        # Preparar lista de IDs
        room_ids = [row.room_data['id'] for row in selected_rows]
        count = len(room_ids)

        # Diálogo de confirmação
        dialog = Gtk.AlertDialog()
        dialog.set_message(f"Excluir {count} sala(s)?")
        dialog.set_detail(f"Tem certeza que deseja excluir {count} sala(s) selecionada(s)?")
        dialog.set_buttons(["Cancelar", "Excluir"])
        dialog.set_cancel_button(0)
        dialog.set_default_button(1)

        dialog.choose(self, None, self.process_delete_rooms, room_ids)

    def process_delete_rooms(self, dialog, result, room_ids):
        """Processa exclusão de salas"""
        try:
            button_index = dialog.choose_finish(result)
            if button_index == 1:  # Excluir
                deleted_count = 0
                for room_id in room_ids:
                    if self.controller.delete_room(room_id):
                        deleted_count += 1

                self.rooms_status_label.set_text(f"{deleted_count} sala(s) excluída(s) com sucesso!")
                self.update_rooms_list()
        except Exception as e:
            self.rooms_status_label.set_text(f"Erro: {str(e)}")

    def create_classes_tab(self):
        """Cria aba de gerenciamento de aulas"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_margin_top(10)

        # Título
        title = Gtk.Label(label="Gerenciar Aulas")
        title.add_css_class("title-3")
        box.append(title)

        # ScrolledWindow com lista
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.append(scrolled)

        # ListBox para aulas
        self.classes_listbox = Gtk.ListBox()
        self.classes_listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.classes_listbox.add_css_class("boxed-list")
        scrolled.set_child(self.classes_listbox)

        # Botões de ação
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        button_box.set_margin_top(10)
        box.append(button_box)

        refresh_btn = Gtk.Button(label="Atualizar")
        refresh_btn.connect("clicked", lambda b: self.update_classes_list())
        button_box.append(refresh_btn)

        delete_btn = Gtk.Button(label="Excluir Selecionados")
        delete_btn.add_css_class("destructive-action")
        delete_btn.connect("clicked", self.on_delete_selected_classes)
        button_box.append(delete_btn)

        # Label de status
        self.classes_status_label = Gtk.Label(label="")
        box.append(self.classes_status_label)

        # Atualizar lista
        self.update_classes_list()

        return box

    def update_classes_list(self):
        """Atualiza lista de aulas"""
        # Limpar lista
        while True:
            row = self.classes_listbox.get_row_at_index(0)
            if row is None:
                break
            self.classes_listbox.remove(row)

        classes = self.controller.get_all_classes()

        if not classes:
            label = Gtk.Label(label="Nenhuma aula cadastrada")
            self.classes_listbox.append(label)
            return

        for cls in classes:
            from datetime import datetime
            try:
                date_obj = datetime.strptime(cls['date'], '%Y-%m-%d')
                date_br = date_obj.strftime('%d/%m/%Y')
            except:
                date_br = cls['date']

            # Box para cada item
            row_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            row_box.set_margin_top(10)
            row_box.set_margin_bottom(10)
            row_box.set_margin_start(10)
            row_box.set_margin_end(10)

            # Disciplina em destaque
            subject = cls.get('subject', 'Sem disciplina')
            subject_label = Gtk.Label(label=subject)
            subject_label.add_css_class("title-4")
            subject_label.set_halign(Gtk.Align.START)
            row_box.append(subject_label)

            # Informações linha 1
            info1_label = Gtk.Label(
                label=f"Sala: {cls['room_name']} | Professor: {cls['teacher_name']}"
            )
            info1_label.set_halign(Gtk.Align.START)
            row_box.append(info1_label)

            # Informações linha 2
            info2_label = Gtk.Label(
                label=f"Data: {date_br} | Horário: {cls['start_time']} - {cls['end_time']} | ID: {cls['id']}"
            )
            info2_label.set_halign(Gtk.Align.START)
            row_box.append(info2_label)

            # Adicionar row com dados da aula
            row = Gtk.ListBoxRow()
            row.set_child(row_box)
            row.class_data = cls
            self.classes_listbox.append(row)

    def on_delete_selected_classes(self, button):
        """Exclui aulas selecionadas"""
        selected_rows = []

        # Coletar todas as rows selecionadas
        def collect_selected(row):
            if hasattr(row, 'class_data'):
                selected_rows.append(row)

        self.classes_listbox.selected_foreach(collect_selected)

        if not selected_rows:
            self.classes_status_label.set_text("Selecione pelo menos uma aula para excluir!")
            return

        # Preparar lista de IDs
        class_ids = [row.class_data['id'] for row in selected_rows]
        count = len(class_ids)

        # Diálogo de confirmação
        dialog = Gtk.AlertDialog()
        dialog.set_message(f"Excluir {count} aula(s)?")
        dialog.set_detail(f"Tem certeza que deseja excluir {count} aula(s) selecionada(s)?")
        dialog.set_buttons(["Cancelar", "Excluir"])
        dialog.set_cancel_button(0)
        dialog.set_default_button(1)

        dialog.choose(self, None, self.process_delete_classes, class_ids)

    def process_delete_classes(self, dialog, result, class_ids):
        """Processa exclusão de aulas"""
        try:
            button_index = dialog.choose_finish(result)
            if button_index == 1:  # Excluir
                deleted_count = 0
                for class_id in class_ids:
                    if self.controller.delete_class(class_id):
                        deleted_count += 1

                self.classes_status_label.set_text(f"{deleted_count} aula(s) excluída(s) com sucesso!")
                self.update_classes_list()
        except Exception as e:
            self.classes_status_label.set_text(f"Erro: {str(e)}")
