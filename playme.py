#@carlosHS92
import sys

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)
import pygame

REPRODUCE = 0

class Principal:
    def __init__(self):
        pygame.init()
        self.gladefile = "play.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        self.filechooser = self.wTree.get_widget("filechooserbutton1")
        self.btnReproducir = self.wTree.get_widget("btnReproducir")
        self.lblCancion = self.wTree.get_widget("lblCancion")
        self.lblAutor = self.wTree.get_widget("lblAutor")
        self.progressbar1 = self.wTree.get_widget("progressbar1")
        self.btnParar = self.wTree.get_widget("btnParar")
        self.btnPausa = self.wTree.get_widget("btnPausa")
        self.barraProgresiva = self.wTree.get_widget("progressbar1")
        self.btnVolumen = self.wTree.get_widget("volumebutton1")
        dic = {"on_filechooserbutton1_selection_changed": self.CargarMusica,
               "on_btnReproduce_clicked": self.ReproducirMusica,
               "on_btnDetener_clicked": self.DetenerMusica,
               "on_btnPausa_clicked": self.PausarMusica,
               "on_volumebutton1_value_changed": self.CambiarVolumen,
               "on_window1_destroy": gtk.main_quit,
               "close_window": self.DetenerMusica}
        self.wTree.signal_autoconnect(dic)
        self.btnVolumen.set_value(1)
        self.progressbar1.set_fraction(1)

    def setReproduce(self):
        global REPRODUCE
        REPRODUCE = 0

    def CambiarVolumen(self, widget, volumen):
        pygame.mixer.music.set_volume(volumen)
        self.progressbar1.set_fraction(volumen)

    def PausarMusica(self, widget):
        pygame.mixer.music.pause()


    def CargarMusica(self, widget):
        self.setReproduce()
        ruta = self.filechooser.get_filename()
        try:
            mp3=open(ruta,'r+b')
            try:
                mp3.seek(-128,2)
                print mp3.read(3)
                nombre = mp3.read(30)
                artista = mp3.read(30)
                self.lblCancion.set_text(str(nombre))
                self.lblAutor.set_text(str(artista))
                print "Nombre..........: " + nombre
                print "Artista.........: " + artista
            finally:
                mp3.close()
        except IOError:
            self.lblCancion.set_text("cancion")
            self.lblCancion.set_text("autor")
            print ("IO Error");

        print "cargar musica"

    def DetenerMusica(self, widget):
        self.setReproduce()
        print "Stop!"
        pygame.mixer.music.stop()

    def ReproducirMusica(self, widget):
        if REPRODUCE == 0:
            ruta = self.filechooser.get_filename()
            #time = pygame.time.Clock()
            try:
                pygame.mixer.music.load(ruta)
                print "Music file %s loaded!" % ruta
            except:
                print "File %s not found! (%s)" % (ruta, pygame.get_error())
                return
            pygame.mixer.music.play()
            global REPRODUCE
            REPRODUCE = 1
        else:
            pygame.mixer.music.unpause()
        #while pygame.mixer.music.get_busy():


if __name__ == "__main__":
    hwg = Principal()
    gtk.main()

if __name__ == "__del__":
    pygame.mixer.music.stop()
