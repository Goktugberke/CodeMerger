import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os


class CodeMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI İçin Kod Birleştirici")
        self.root.geometry("600x500")

        self.selected_files = []

        # --- Üst Bölüm: Dosya Seçme Butonu ---
        self.btn_frame = tk.Frame(root, pady=10)
        self.btn_frame.pack()

        self.btn_select = tk.Button(self.btn_frame, text="Dosyaları Seç (Gözat)", command=self.select_files,
                                    bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_select.pack(side=tk.LEFT, padx=10)

        self.btn_clear = tk.Button(self.btn_frame, text="Listeyi Temizle", command=self.clear_list, bg="#f44336",
                                   fg="white", font=("Arial", 10, "bold"))
        self.btn_clear.pack(side=tk.LEFT, padx=10)

        # --- Orta Bölüm: Dosya Listesi ve Path Alanı ---
        self.lbl_info = tk.Label(root, text="Seçilen Dosyalar veya Manuel Path Yapıştırma Alanı:", font=("Arial", 10))
        self.lbl_info.pack()

        self.text_area = scrolledtext.ScrolledText(root, width=70, height=15)
        self.text_area.pack(padx=10, pady=5)
        self.text_area.insert(tk.END,
                              "Dosyaları 'Gözat' butonuyla seçebilir veya path'leri (tırnaklı/tırnaksız) buraya yapıştırabilirsin.\n")

        # --- Alt Bölüm: Çevir Butonu ---
        self.btn_convert = tk.Button(root, text="ÇEVİR VE KAYDET", command=self.convert_files, bg="#2196F3", fg="white",
                                     font=("Arial", 12, "bold"), height=2)
        self.btn_convert.pack(pady=20, fill=tk.X, padx=50)

    def select_files(self):
        # Dosya seçim penceresini aç
        filenames = filedialog.askopenfilenames(title="Dosyaları Seç",
                                                filetypes=(("Kod Dosyaları", "*.c *.h *.cpp *.py *.js *.txt *.java"),
                                                           ("Tüm Dosyalar", "*.*")))
        if filenames:
            # Mevcut metni temizle (eğer varsayılan mesaj varsa)
            current_content = self.text_area.get("1.0", tk.END).strip()
            if "Dosyaları 'Gözat'" in current_content:
                self.text_area.delete("1.0", tk.END)

            for name in filenames:
                # Pathleri tırnak içine alarak ekle (senin formatına uygun olsun diye)
                formatted_path = f'"{os.path.normpath(name)}"\n'
                self.text_area.insert(tk.END, formatted_path)

    def clear_list(self):
        self.text_area.delete("1.0", tk.END)

    def convert_files(self):
        # Text alanındaki içeriği al
        content = self.text_area.get("1.0", tk.END).strip()

        if not content:
            messagebox.showwarning("Uyarı", "Lütfen önce dosya seçin veya path yapıştırın.")
            return

        # Satır satır pathleri ayıkla
        lines = content.split('\n')
        valid_files = []

        for line in lines:
            # Tırnak işaretlerini ve boşlukları temizle
            path = line.strip().replace('"', '').replace("'", "")
            if path and os.path.exists(path):
                valid_files.append(path)
            elif path:  # Path var ama dosya yoksa uyar
                print(f"Uyarı: Dosya bulunamadı -> {path}")

        if not valid_files:
            messagebox.showerror("Hata", "Geçerli bir dosya yolu bulunamadı.")
            return

        # Kaydetme yeri sor
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Dosyası", "*.txt")],
                                                 title="Sonucu Nereye Kaydedelim?")

        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as outfile:
                for file_path in valid_files:
                    try:
                        # Dosya içeriğini oku
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                            file_content = infile.read()

                        # İSTENİLEN FORMAT
                        outfile.write(f'"{file_path}" :\n')
                        outfile.write(file_content)
                        outfile.write('\n\n################################################################\n')

                    except Exception as e:
                        outfile.write(f'"{file_path}" : DOSYA OKUMA HATASI ({str(e)})\n')
                        outfile.write('\n################################################################\n')

            messagebox.showinfo("Başarılı", f"İşlem tamamlandı!\nDosya şuraya kaydedildi:\n{save_path}")

        except Exception as e:
            messagebox.showerror("Hata", f"Yazma hatası oluştu: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeMergerApp(root)
    root.mainloop()