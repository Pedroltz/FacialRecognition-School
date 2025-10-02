import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


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
        self.teachers_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
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
        self._clear_listbox(self.teachers_listbox)

        teachers = self.controller.get_all_teachers()
        if not teachers:
            self.teachers_listbox.append(Gtk.Label(label="Nenhum professor cadastrado"))
            return

        for teacher in teachers:
            row = self._create_teacher_row(teacher)
            self.teachers_listbox.append(row)

    def _create_teacher_row(self, teacher):
        """Cria uma linha para o professor com checkbox"""
        main_box = self._create_main_box()
        checkbox = self._create_checkbox()
        main_box.append(checkbox)

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_box.set_hexpand(True)

        name_label = Gtk.Label(label=teacher['name'])
        name_label.add_css_class("title-4")
        name_label.set_halign(Gtk.Align.START)
        info_box.append(name_label)

        info_text = f"ID: {teacher['id']} | Idade: {teacher['age']} | Tel: {teacher['phone']} | Email: {teacher['email']}"
        info_label = Gtk.Label(label=info_text)
        info_label.set_halign(Gtk.Align.START)
        info_box.append(info_label)

        main_box.append(info_box)

        row = Gtk.ListBoxRow()
        row.set_child(main_box)
        row.teacher_data = teacher
        row.checkbox = checkbox
        row.connect("activate", lambda r: r.checkbox.set_active(not r.checkbox.get_active()))

        return row

    def on_delete_selected_teachers(self, button):
        """Exclui professores selecionados"""
        selected_rows = self._get_selected_rows(self.teachers_listbox)

        if not selected_rows:
            self.teachers_status_label.set_text("Selecione pelo menos um professor para excluir!")
            return

        teacher_ids = [row.teacher_data['id'] for row in selected_rows]
        self._show_delete_confirmation(
            count=len(teacher_ids),
            item_type="professor(es)",
            callback=self.process_delete_teachers,
            data=teacher_ids
        )

    def process_delete_teachers(self, dialog, result, teacher_ids):
        """Processa exclusão de professores"""
        try:
            button_index = dialog.choose_finish(result)
            if button_index == 1:
                deleted_count = sum(
                    1 for teacher_id in teacher_ids
                    if self.controller.delete_teacher(teacher_id)
                )
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
        self.rooms_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
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
        self._clear_listbox(self.rooms_listbox)

        rooms = self.controller.get_all_rooms()
        if not rooms:
            self.rooms_listbox.append(Gtk.Label(label="Nenhuma sala cadastrada"))
            return

        for room in rooms:
            row = self._create_room_row(room)
            self.rooms_listbox.append(row)

    def _create_room_row(self, room):
        """Cria uma linha para a sala com checkbox"""
        main_box = self._create_main_box()
        checkbox = self._create_checkbox()
        main_box.append(checkbox)

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_box.set_hexpand(True)

        name_label = Gtk.Label(label=room['name'])
        name_label.add_css_class("title-4")
        name_label.set_halign(Gtk.Align.START)
        info_box.append(name_label)

        info_text = f"ID: {room['id']}"
        if room.get('description'):
            info_text += f" | Descrição: {room['description']}"
        info_label = Gtk.Label(label=info_text)
        info_label.set_halign(Gtk.Align.START)
        info_box.append(info_label)

        main_box.append(info_box)

        row = Gtk.ListBoxRow()
        row.set_child(main_box)
        row.room_data = room
        row.checkbox = checkbox
        row.connect("activate", lambda r: r.checkbox.set_active(not r.checkbox.get_active()))

        return row

    def on_delete_selected_rooms(self, button):
        """Exclui salas selecionadas"""
        selected_rows = self._get_selected_rows(self.rooms_listbox)

        if not selected_rows:
            self.rooms_status_label.set_text("Selecione pelo menos uma sala para excluir!")
            return

        room_ids = [row.room_data['id'] for row in selected_rows]
        self._show_delete_confirmation(
            count=len(room_ids),
            item_type="sala(s)",
            callback=self.process_delete_rooms,
            data=room_ids
        )

    def process_delete_rooms(self, dialog, result, room_ids):
        """Processa exclusão de salas"""
        try:
            button_index = dialog.choose_finish(result)
            if button_index == 1:
                deleted_count = sum(
                    1 for room_id in room_ids
                    if self.controller.delete_room(room_id)
                )
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
        self.classes_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
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
        self._clear_listbox(self.classes_listbox)

        classes = self.controller.get_all_classes()
        if not classes:
            self.classes_listbox.append(Gtk.Label(label="Nenhuma aula cadastrada"))
            return

        for cls in classes:
            row = self._create_class_row(cls)
            self.classes_listbox.append(row)

    def _create_class_row(self, cls):
        """Cria uma linha para a aula com checkbox"""
        main_box = self._create_main_box()
        checkbox = self._create_checkbox()
        main_box.append(checkbox)

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_box.set_hexpand(True)

        subject = cls.get('subject', 'Sem disciplina')
        subject_label = Gtk.Label(label=subject)
        subject_label.add_css_class("title-4")
        subject_label.set_halign(Gtk.Align.START)
        info_box.append(subject_label)

        info1_label = Gtk.Label(label=f"Sala: {cls['room_name']} | Professor: {cls['teacher_name']}")
        info1_label.set_halign(Gtk.Align.START)
        info_box.append(info1_label)

        info2_label = Gtk.Label(
            label=f"{cls['day_of_week']} | Horário: {cls['start_time']} - {cls['end_time']} | ID: {cls['id']}"
        )
        info2_label.set_halign(Gtk.Align.START)
        info_box.append(info2_label)

        main_box.append(info_box)

        row = Gtk.ListBoxRow()
        row.set_child(main_box)
        row.class_data = cls
        row.checkbox = checkbox
        row.connect("activate", lambda r: r.checkbox.set_active(not r.checkbox.get_active()))

        return row

    def on_delete_selected_classes(self, button):
        """Exclui aulas selecionadas"""
        selected_rows = self._get_selected_rows(self.classes_listbox)

        if not selected_rows:
            self.classes_status_label.set_text("Selecione pelo menos uma aula para excluir!")
            return

        class_ids = [row.class_data['id'] for row in selected_rows]
        self._show_delete_confirmation(
            count=len(class_ids),
            item_type="aula(s)",
            callback=self.process_delete_classes,
            data=class_ids
        )

    def process_delete_classes(self, dialog, result, class_ids):
        """Processa exclusão de aulas"""
        try:
            button_index = dialog.choose_finish(result)
            if button_index == 1:
                deleted_count = sum(
                    1 for class_id in class_ids
                    if self.controller.delete_class(class_id)
                )
                self.classes_status_label.set_text(f"{deleted_count} aula(s) excluída(s) com sucesso!")
                self.update_classes_list()
        except Exception as e:
            self.classes_status_label.set_text(f"Erro: {str(e)}")

    # Métodos auxiliares reutilizáveis
    def _clear_listbox(self, listbox):
        """Limpa todos os itens de uma listbox"""
        while True:
            row = listbox.get_row_at_index(0)
            if row is None:
                break
            listbox.remove(row)

    def _create_main_box(self):
        """Cria um box horizontal principal com margens"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        return box

    def _create_checkbox(self):
        """Cria um checkbox centralizado verticalmente"""
        checkbox = Gtk.CheckButton()
        checkbox.set_valign(Gtk.Align.CENTER)
        return checkbox

    def _get_selected_rows(self, listbox):
        """Retorna lista de rows com checkbox marcado"""
        selected_rows = []
        index = 0
        while True:
            row = listbox.get_row_at_index(index)
            if row is None:
                break
            if hasattr(row, 'checkbox') and row.checkbox.get_active():
                selected_rows.append(row)
            index += 1
        return selected_rows

    def _show_delete_confirmation(self, count, item_type, callback, data):
        """Mostra diálogo de confirmação para exclusão"""
        dialog = Gtk.AlertDialog()
        dialog.set_message(f"Excluir {count} {item_type}?")
        dialog.set_detail(f"Tem certeza que deseja excluir {count} {item_type} selecionado(s)?")
        dialog.set_buttons(["Cancelar", "Excluir"])
        dialog.set_cancel_button(0)
        dialog.set_default_button(1)
        dialog.choose(self, None, callback, data)
