import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib

class RegisterRoomWindow(Gtk.Window):
    def __init__(self, parent, controller):
        super().__init__(transient_for=parent, title="Cadastrar Sala")
        self.controller = controller
        self.set_default_size(550, 300)

        # Box principal vertical
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(15)
        main_box.set_margin_bottom(15)
        main_box.set_margin_start(15)
        main_box.set_margin_end(15)
        self.set_child(main_box)

        # Título
        title_label = Gtk.Label(label="Cadastro de Sala")
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

        # Campo Nome
        name_label = Gtk.Label(label="Nome:")
        name_label.set_halign(Gtk.Align.END)
        name_label.set_size_request(80, -1)
        self.name_entry = Gtk.Entry()
        self.name_entry.set_size_request(350, -1)
        self.name_entry.set_placeholder_text("Nome da sala")
        grid.attach(name_label, 0, 0, 1, 1)
        grid.attach(self.name_entry, 1, 0, 1, 1)

        # Campo Descrição
        desc_label = Gtk.Label(label="Descrição:")
        desc_label.set_halign(Gtk.Align.END)
        desc_label.set_size_request(80, -1)
        self.desc_entry = Gtk.Entry()
        self.desc_entry.set_size_request(350, -1)
        self.desc_entry.set_placeholder_text("Descrição (opcional)")
        grid.attach(desc_label, 0, 1, 1, 1)
        grid.attach(self.desc_entry, 1, 1, 1, 1)

        # Separador
        separator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.append(separator2)

        # Botão salvar
        save_btn = Gtk.Button(label="Salvar Sala")
        save_btn.add_css_class("suggested-action")
        save_btn.set_halign(Gtk.Align.CENTER)
        save_btn.connect("clicked", self.on_save_clicked)
        main_box.append(save_btn)

        # Label de status
        self.status_label = Gtk.Label(label="")
        self.status_label.set_wrap(True)
        self.status_label.set_halign(Gtk.Align.CENTER)
        main_box.append(self.status_label)

    def on_save_clicked(self, button):
        """Salva a sala"""
        name = self.name_entry.get_text().strip()
        description = self.desc_entry.get_text().strip()

        if not name:
            self.status_label.set_text("Por favor, informe o nome da sala!")
            return

        success, message = self.controller.create_room(name, description)
        self.status_label.set_text(message)

        if success:
            GLib.timeout_add_seconds(2, self.close)
