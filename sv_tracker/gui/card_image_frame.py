from tkinter import *
from sv_tracker.database.image_database_interface import ImageDatabaseInterface
from PIL import ImageTk, Image


class CardImageFrame:
    START_SCALE = 0.65

    def __init__(self, parent, card, count):
        image_db = ImageDatabaseInterface()
        self.card_img = Image.open(image_db.get_card_image(card.card_id))
        self.resized_img = self.card_img.resize((int(self.card_img.width*self.START_SCALE),
                                                 int(self.card_img.height*self.START_SCALE)))
        self.img_copy = self.resized_img
        self.tk_img = ImageTk.PhotoImage(self.img_copy)

        self.card_name = card.card_name
        self.cost = card.cost
        self.original_count = count
        self.current_count = count
        self.card_clan = card.clan

        self.frame = self._generate_frame(parent)
        self.canvas = self._generate_canvas(self.frame)
        self.cost_frame = self._generate_cost_frame(self.frame)
        self.count_label = None
        self.count_frame = self._generate_count_frame(self.frame)

        self._adjust_labels()

    def _generate_frame(self, parent):
        frame = Frame(parent, bd=0)
        return frame

    def _generate_canvas(self, parent):
        canvas = Canvas(parent, width=self.tk_img.width(), height=self.tk_img.height(), bd=0)
        canvas.create_image(0, 2, image=self.tk_img, anchor=NW)
        canvas.create_text(10, self.tk_img.height()/2, text=self.card_name, anchor=W,
                           fill="white")
        return canvas

    def _generate_cost_frame(self, parent):
        height = self.tk_img.height()
        width = height

        class_color = {
            0: 'gray',
            1: '#339900',
            2: '#D7CD4C',
            3: '#333399',
            4: '#CC6633',
            5: '#9D87DE',
            6: '#990033',
            7: '#B0A979',
            8: '#41ACE1',
        }

        frame = Frame(parent, width=width, height=height, bg=class_color[self.card_clan], bd=0)
        label = Label(frame, bg=frame['bg'], text=self.cost, bd=0, fg="white", font="times 12 bold")
        label.place(relx=0.5, rely=0.5, x=0, y=0, anchor="center")
        return frame

    def _generate_count_frame(self, parent):
        height = self.tk_img.height()
        width = height
        frame = Frame(parent, width=width, height=height, bg="black", bd=0)
        label = Label(frame, bg=frame['bg'], text='x' + str(self.current_count), bd=0, fg="white",
                      font="fira 10 bold")
        label.place(relx=0.5, rely=0.5, x=0, y=0, anchor="center")
        self.count_label = label
        return frame

    def _adjust_labels(self):
        self.cost_frame.grid(row=0, column=0)
        self.canvas.grid(row=0, column=1)
        self.count_frame.grid(row=0, column=2)

    def update_count(self, count):
        self.current_count = count
        self.count_label.configure(text='x' + str(self.current_count))
        self.gray_out_image()
        self.update_canvas()
        self.gray_out_count()

    def gray_out_image(self):
        if self.current_count == 0:
            self.img_copy = self.resized_img.copy().convert('LA')
            gray = Image.new('LA', (self.img_copy.width, self.img_copy.height), '#666666')
            self.img_copy = Image.blend(self.img_copy, gray, 0.5)
        else:
            self.img_copy = self.resized_img

    def gray_out_count(self):
        fg_color = 'white'
        color = 'black'
        if self.current_count == 0:
            color = 'gray'
        elif self.current_count != self.original_count:
            fg_color = 'black'
            color = '#90EE90'
        self.count_frame.configure(bg=color)
        self.count_label.configure(bg=self.count_frame['bg'], fg=fg_color)

    def update_canvas(self):
        self.tk_img = ImageTk.PhotoImage(self.img_copy)
        self.canvas.delete(1)
        self.canvas.delete(2)
        self.canvas.create_image(0, 2, image=self.tk_img, anchor=NW)
        font_size = max(int((self.canvas.winfo_height() / 35) * 10), 8)
        self.canvas.create_text(10, self.canvas.winfo_height() / 2, text=self.card_name, anchor=W,
                                fill="white", font='fira ' + str(font_size) + ' bold')

    def resize(self, scale):
        self.resize_label(scale)
        self.resize_cost_frame()
        self.resize_count_frame()

    def resize_label(self, scale):
        new_width = int(self.card_img.width * scale)
        new_height = int(self.card_img.height * scale)
        self.resized_img = self.card_img.resize((new_width, new_height))
        self.gray_out_image()
        self.update_canvas()
        self.canvas.configure(width=new_width, height=new_height)

    def resize_cost_frame(self):
        height = self.tk_img.height()
        width = height
        self.cost_frame.configure(width=width, height=height)

    def resize_count_frame(self):
        height = self.tk_img.height()
        width = height
        self.count_frame.configure(width=width, height=height)