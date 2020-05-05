from tkinter import *
from image_database_interface import ImageDatabaseInterface
from PIL import ImageTk, Image


class CardImageFrame:
    START_SCALE = 1

    def __init__(self, parent, card, count):
        image_db = ImageDatabaseInterface()
        self.card_img = Image.open(image_db.get_card_image(card.card_id))
        img_copy = self.card_img.resize((int(self.card_img.width*self.START_SCALE),
                                         int(self.card_img.height*self.START_SCALE)))
        self.tk_img = ImageTk.PhotoImage(img_copy)

        self.card_name = card.card_name
        self.cost = card.cost
        self.count = count
        self.card_clan = card.clan

        self.frame = self._generate_frame(parent)
        self.canvas = self._generate_canvas(self.frame)
        self.cost_frame = self._generate_cost_frame(self.frame)
        self.count_frame = self._generate_count_frame(self.frame)

        self._adjust_labels()

    def _generate_frame(self, parent):
        frame = Frame(parent, bd=0)
        return frame

    def _generate_canvas(self, parent):
        canvas = Canvas(parent, width=self.tk_img.width(), height=self.tk_img.height(), bd=0)
        canvas.create_image(0, 2, image=self.tk_img, anchor=NW)
        canvas.create_text(10, self.tk_img.height()/2, text=self.card_name, anchor=W, fill="white")
        return canvas

    def _generate_cost_frame(self, parent):
        height = self.tk_img.height()
        width = height
        frame = Frame(parent, width=width, height=height, bg="gray", bd=0)
        label = Label(frame, bg=frame['bg'], text=self.cost, bd=0)
        label.place(relx=0.5, rely=0.5, x=0, y=0, anchor="center")
        return frame

    def _generate_count_frame(self, parent):
        height = self.tk_img.height()
        width = height
        frame = Frame(parent, width=width, height=height, bg="black", bd=0)
        label = Label(frame, bg=frame['bg'], text='x' + str(self.count), bd=0, fg="white")
        label.place(relx=0.5, rely=0.5, x=0, y=0, anchor="center")
        return frame

    def _adjust_labels(self):
        self.cost_frame.grid(row=0, column=0)
        self.canvas.grid(row=0, column=1)
        self.count_frame.grid(row=0, column=2)

    def resize(self, scale):
        self.resize_label(scale)
        self.resize_cost_frame()
        self.resize_count_frame()

    def resize_label(self, scale):
        new_width = int(self.card_img.width * scale)
        new_height = int(self.card_img.height * scale)
        img_copy = self.card_img.resize((new_width, new_height))
        self.tk_img = ImageTk.PhotoImage(img_copy)
        self.canvas.configure(width=new_width, height=new_height)
        self.canvas.delete(1)
        self.canvas.delete(2)
        self.canvas.create_image(0, 2, image=self.tk_img, anchor=NW)
        self.canvas.create_text(10, new_height/2, text=self.card_name, anchor=W, fill="white")

    def resize_cost_frame(self):
        height = self.tk_img.height()
        width = height
        self.cost_frame.configure(width=width, height=height)

    def resize_count_frame(self):
        height = self.tk_img.height()
        width = height
        self.count_frame.configure(width=width, height=height)