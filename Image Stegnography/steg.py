import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("🔓 Hacker Steganography Tool 🔓")
        master.geometry("800x600")
        master.configure(bg="black")  

        # Title Label
        self.title_label = tk.Label(master, text="HACKER STEGANOGRAPHY", 
                                    font=("Courier New", 20, "bold"), 
                                    fg="lime", bg="black")
        self.title_label.pack(pady=10)

        # Dark mode styles
        self.style = ttk.Style()
        self.style.configure("TNotebook", background="black", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="black", foreground="lime", padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "black")], foreground=[("selected", "lime")])

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.encode_frame = tk.Frame(self.notebook, bg="black")
        self.notebook.add(self.encode_frame, text="Encode")

        self.decode_frame = tk.Frame(self.notebook, bg="black")
        self.notebook.add(self.decode_frame, text="Decode")

        self.create_encoding_frame()
        self.create_decoding_frame()

    def create_encoding_frame(self):
        tk.Label(self.encode_frame, text="Encode Image:", fg="lime", bg="black", font=("Courier New", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.encode_image_path = tk.StringVar()
        encode_entry = tk.Entry(self.encode_frame, textvariable=self.encode_image_path, width=40, bg="black", fg="lime", insertbackground="lime")
        encode_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        tk.Button(self.encode_frame, text="Browse", command=self.browse_encode_image, bg="black", fg="lime", relief="ridge").grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.encode_frame, text="Secret Message:", fg="lime", bg="black", font=("Courier New", 12, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.secret_message = tk.Text(self.encode_frame, height=8, width=50, font=("Courier New", 10), bg="black", fg="lime", insertbackground="lime")
        self.secret_message.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        tk.Button(self.encode_frame, text="🔐 Encode", command=self.encode, bg="black", fg="lime", relief="ridge").grid(row=2, column=1, pady=10)
        self.encode_frame.columnconfigure(1, weight=1)

    def create_decoding_frame(self):
        tk.Label(self.decode_frame, text="Decode Image:", fg="lime", bg="black", font=("Courier New", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.decode_image_path = tk.StringVar()
        decode_entry = tk.Entry(self.decode_frame, textvariable=self.decode_image_path, width=40, bg="black", fg="lime", insertbackground="lime")
        decode_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        tk.Button(self.decode_frame, text="Browse", command=self.browse_decode_image, bg="black", fg="lime", relief="ridge").grid(row=0, column=2, padx=5, pady=5)

        tk.Button(self.decode_frame, text="🕵️ Decode", command=self.decode, bg="black", fg="lime", relief="ridge").grid(row=1, column=1, pady=10)

        tk.Label(self.decode_frame, text="Decoded Message:", fg="lime", bg="black", font=("Courier New", 12, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.decoded_message = tk.Text(self.decode_frame, height=8, width=50, font=("Courier New", 10), bg="black", fg="lime", insertbackground="lime", state='disabled')
        self.decoded_message.grid(row=2, column=1, padx=5, pady=5, sticky="we")

        self.decode_frame.columnconfigure(1, weight=1)

    def browse_encode_image(self):
        self.encode_image_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]))

    def browse_decode_image(self):
        self.decode_image_path.set(filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]))

    def encode(self):
        image_path = self.encode_image_path.get()
        message = self.secret_message.get("1.0", tk.END).strip()

        if not image_path or not message:
            messagebox.showerror("Error", "Please select an image and enter a message.")
            return

        try:
            img = Image.open(image_path)
            encoded_img = self.encode_message(img, message)

            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                encoded_img.save(save_path)
                messagebox.showinfo("Success", "✅ Image encoded and saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def encode_message(self, img, message):
        message += "###"  
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        pixels = list(img.getdata())

        if len(binary_message) > len(pixels) * 3:
            messagebox.showerror("Error", "Message too large to encode in image.")
            return img

        encoded_pixels = []
        message_index = 0

        for pixel in pixels:
            if message_index < len(binary_message):
                r, g, b = pixel
                r = (r & ~1) | int(binary_message[message_index])
                message_index += 1
                encoded_pixels.append((r, g, b))
            else:
                encoded_pixels.append(pixel)

        encoded_img = Image.new(img.mode, img.size)
        encoded_img.putdata(encoded_pixels)
        return encoded_img

    def decode(self):
        image_path = self.decode_image_path.get()

        if not image_path:
            messagebox.showerror("Error", "Please select an image to decode.")
            return

        try:
            img = Image.open(image_path)
            decoded_message = self.decode_message(img)

            self.decoded_message.config(state='normal')
            self.decoded_message.delete("1.0", tk.END)
            self.decoded_message.insert("1.0", decoded_message)
            self.decoded_message.config(state='disabled')
            messagebox.showinfo("Decoded", "📜 Secret message retrieved successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_message(self, img):
        pixels = list(img.getdata())
        binary_message = ""

        for pixel in pixels:
            r, g, b = pixel
            binary_message += str(r & 1)  

        chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        decoded_text = ''.join(chr(int(char, 2)) for char in chars if int(char, 2) != 0)

        if "###" in decoded_text:
            return decoded_text.split("###")[0]
        else:
            return "❌ No hidden message found!"

root = tk.Tk()
app = SteganographyApp(root)
root.mainloop()
