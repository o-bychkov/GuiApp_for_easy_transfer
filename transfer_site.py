import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Buglump:
    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file("%s/Site_transfer.glade" % os.getcwd())

        self.window = self.builder.get_object("main_window")

        self.entry_login = self.builder.get_object("entry_login")
        self.entry_ip = self.builder.get_object("entry_ip")
        self.entry_site_dir = self.builder.get_object("entry_site_dir")
        self.entry_bd_name = self.builder.get_object("entry_bd_name")
        self.entry_bd_pass = self.builder.get_object("entry_bd_pass")
        self.apply = self.builder.get_object("apply")

        self.file_transfer = self.builder.get_object("file_transfer")

        self.create_bd_dump = self.builder.get_object('create_bd_dump')

        self.entry_new_bd_name = self.builder.get_object("entry_new_bd_name")
        self.import_bd = self.builder.get_object("import_bd")

        self.entry_way_from = self.builder.get_object("entry_way_from")
        self.entry_way_to = self.builder.get_object("entry_way_to")
        self.change_ways = self.builder.get_object("change_ways")
        self.button_ok_change_ways = self.builder.get_object("button_ok_change_ways")

        self.window.connect("destroy", Gtk.main_quit)
        self.window.show()

        self.apply.connect('clicked', self.button_apply)
        self.button_ok_change_ways.connect('clicked', self.replacement_site_ways)

    def button_apply(self, widget):

        # Блок для переноса файлов
        if (self.entry_login.get_text() and self.entry_ip.get_text() and self.entry_site_dir.get_text()) == '':
            self.file_transfer.set_text('Заполните все поля')
        elif self.entry_site_dir.get_text() == 'public_html':
            self.file_transfer.set_text('rsync -rpPvt --log-file=progress_rsync %s@%s:~/%s/ ./' % (self.entry_login.get_text(), self.entry_ip.get_text(), self.entry_site_dir.get_text()))
        else:
            self.file_transfer.set_text('rsync -rpPvt --log-file=progress_rsync %s@%s:~/%s/public_html/ ./' % (self.entry_login.get_text(), self.entry_ip.get_text(), self.entry_site_dir.get_text()))

        # Блок для дампа базы данных
        if (self.entry_bd_name.get_text() and self.entry_bd_pass.get_text()) == '':
            self.create_bd_dump.set_text('')
        else:
            self.create_bd_dump.set_text("mysqldump -u'%s' %s -p'%s' > bd_dump.sql" % (self.entry_bd_name.get_text(), self.entry_bd_name.get_text(), self.entry_bd_pass.get_text()))

        # Блок для импорта базы данных
        if (self.entry_new_bd_name.get_text() and self.entry_bd_pass.get_text()) == '':
            self.import_bd.set_text('')
        else:
            self.import_bd.set_text("mysql -u'%s' %s -p'%s' < bd_dump.sql" % (self.entry_new_bd_name.get_text(), self.entry_new_bd_name.get_text(), self.entry_bd_pass.get_text()))


    def replacement_site_ways(self, widget):

        # Блок для замены путей
        if (self.entry_way_from.get_text() and self.entry_way_to.get_text()) == '':
            self.change_ways.set_text('Заполните все поля')
        else:
            bash_change_ways = "grep -rl '%s' | xargs sed -i 's/\\" % self.entry_way_from.get_text()
            for elem in self.entry_way_from.get_text().strip('/').split('/'):
                bash_change_ways += "/%s\\" % elem
            bash_change_ways += "//\\"
            for elem in self.entry_way_to.get_text().strip('/').split('/'):
                bash_change_ways += "/%s\\" % elem
            bash_change_ways += "//'"
            self.change_ways.set_text(bash_change_ways)



if __name__ == "__main__":
    main = Buglump()
    Gtk.main()


