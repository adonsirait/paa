from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

class map:
    #Deklarasi variabel awal yang nantinya akan digunakan
    def __init__(self) -> None:
        self.scale = 10
        self.len = 0
        self.width = 150*self.scale
        self.height = 150*self.scale
        self.padding = self.scale
        self.road_len = 20*self.scale
        self.road_width = 20
        self.simpang = []
        self.jarak = 10
        self.bangunan = [
            Image.open("bangunan/kecil5.png").resize((50,30)),
            Image.open("bangunan/kecil7.png").resize((50,30)), 
            Image.open("bangunan/kecil2.png").resize((50,50)), 
            Image.open("bangunan/besar1.jpg").resize((100,50)),
            Image.open("bangunan/house.jpg").resize((5,5)),
            ]
        self.tumbuhan = [
            Image.open("tumbuhan/treeA.jpg").resize((20,20)),
            Image.open("tumbuhan/bushA.png").resize((20,20)), 
            Image.open("tumbuhan/bushB.jpg").resize((20,20)), 
            Image.open("tumbuhan/batuA.jpg").resize((20,20))
            ]
        self.map = Image.new("RGBA",(self.width, self.height ), "gray" )
        self.mapDraw = ImageDraw.Draw(self.map)
        
    #Fungsi limit ini untuk membatasi posisi x dan y agar tidak keluar dari map
    def limitX(self, x) : return 0 if x <= 0 else (x if x < self.width else self.width )
    def limitY(self, y) : return 0 if y <= 0 else (y if y < self.height else self.height )
    #Fungsi untuk membuat jalan , dimulai dari titik 0,0 Menggunakan metode rekursif    
    def makeRoads(self, pos, direction):
        self.len += 1
        if self.len > 150 and (pos[0]<=0 or pos[0]>=self.width or pos[1] <= 0 or pos[1] >=self.height ): return
        self.simpang.append(pos)
        step = random.choice([1,1])
        #Next vertice berarti titik selanjutnya atau x2, y2
        #Titik selanjutnya itu menggunakan library random untuk mencari x dan y terdekat
        nextvertice = ( pos[0] + self.road_width if direction == "y" else pos[0] + self.road_len  * step, pos[1] + self.road_width if direction == "x" else pos[1] + self.road_len *step)
        if nextvertice not in self.simpang : self.simpang.append(nextvertice)
        valid = [pos[0] <= 0 and direction == "y", pos[1] <=0 and direction == "x", nextvertice[1] >= self.height and direction == "x", pos[0] >= self.height and direction == "x"]
        nextvertice = (self.limitX(nextvertice[0]), self.limitY(nextvertice[1]))
        xsort, ysort = sort([pos[0], nextvertice[0]]), sort([pos[1], nextvertice[1]])
        if(xsort[1] >= self.width or xsort[1] <= 0) : 
            self.simpang.append((self.limitX(xsort[1]), pos[1]))
        if(ysort[1] >= self.height or ysort[1] <= 0) : 
            self.simpang.append((pos[0]+10, self.limitY(ysort[1])))
        if not sum(valid) : 
            #Fungsi untk menggambar jalan
            self.mapDraw.rectangle(((xsort[0], ysort[0]), (xsort[1] , ysort[1] )), "black")
            if direction == "y" : self.mapDraw.line(((xsort[0] + 10, ysort[0] + 10), ( xsort[0] +10 , ysort[1] - 10)),"white", 1)
            else : self.mapDraw.line(((xsort[0] + 20 , ysort[0] + 10), ( xsort[1] -10 , ysort[0]+10 )),"white", 1)
        
        nextX = self.width if nextvertice[0] <= 0 else (nextvertice[0] - (20 if direction == "y" else 0) if nextvertice[0] < self.width else 0)
        nextY = self.height if nextvertice[1] <= 0 else (nextvertice[1] - (20 if direction == 'x' else 0) if nextvertice[1] < self.height else 0)
        # if nextX == self.lastVertex[0] and self.lastVertex2[1] < nextY: self.map.paste( self.corner[1], (self.lastVertex))
        # if nextX == self.lastVertex[0] and self.lastVertex2[1] > nextY: self.map.paste( self.corner[0], (self.lastVertex))
        print((nextX, nextY) , " : last - ", self.lastVertex, self.lastVertex2)
        self.lastVertex = (nextX, nextY)
        self.lastVertex2 = pos
        self.makeRoads((nextX,nextY ),random.choice(["x", 'y']) )
    
    #Fungsi untuk membuat map baru, yang mana akan dieksekusi ketika tombol generate map ditekan
    def createMap(self):
        self.simpang = [(0,0), (0,self.height), (self.width , 0) ,(self.width, self.height)]
        self.len = 0
        self.lastVertex = (random.randrange(0, self.width, self.road_len), random.choice([0, self.height]))
        self.lastVertex2 = (random.randrange(0, self.width, self.road_len), random.choice([0, self.height]))
        self.map = Image.new("RGBA", (self.width, self.height), (150, 150, 150))
        self.mapDraw = ImageDraw.Draw(self.map)
        self.makeRoads(self.lastVertex, "y")
        #Save map
        self.map.save("map1.png")
        self.mapping()
        #Save map2
        self.map.save("map2.png")
        return self.map
    
    #Panggil fungsi generate building ketika jalan sudah berada di batas bawah map
    def generateBuilding(self, pos):
        x = pos[0][0]
        #titik paling atas area
        #Fungsi ini untuk mengembalikan asset / gambar bangunan yang muat dengan area yang sekarang ingin digenerate BangunanX berarti menyamping gambarnya
        def getBangunanX(x):
            return [bangunan for bangunan in self.bangunan if bangunan.size[0] + x < pos[1][0]-self.padding]
        #Fungsi ini untuk mengembalikan asset / gambar bangunan yang muat dengan area yang sekarang ingin digenerate
        #BangunanY berarti vertical atau keatas
        def getBangunanY(x,y):
            return [bangunan for bangunan in self.tumbuhan if bangunan.size[0] + x < pos[1][0]-self.padding and bangunan.size[1] + y < pos[1][1]-50]
        
        while x < pos[1][0]:
            #Kandidat bangunan yang muat utk diletakkan
            kandidat = getBangunanX(x)
            #Jika ternyata ada atau memungkinkan untuk memasukkan bangunan
            if len(kandidat):
                #Ambil salah satu bangunan yang muat utuk diamsukkan ke area, menggunakan library random / diacak
                build = random.choice(kandidat)
                #Untuk rectangel ini kita isi arenya dengan warna abu-abu supaya berkesan ada jalan setapak
                self.mapDraw.rectangle(((x, pos[0][1]), (x+build.size[0]+20, pos[0][1]+build.size[1])),"green")
                #Kita paste atau tempelkan gambar bangunan kedalam area yang sekrang
                self.map.paste(build, (x, pos[0][1]))
                #Tambahkan nilai x karena disini penempatan bangunan nya dari kiri ke kanan area
                x += build.size[0] + self.jarak
            else: break
        x = pos[0][0]
        y = pos[0][1] + 50 + self.padding
        
        #Ini kusus untuk ditengah atau dekorasi / pepohonan 
        while  y < pos[1][1] - 50:
            tertinggi = 50
            while x < pos[1][0] :
                kandidat = getBangunanY(x, y)
                if len(kandidat):
                    build = random.choice(kandidat)
                    self.mapDraw.rectangle(((x,y), (x+build.size[0]+20, y+build.size[1])),"green")
                    self.map.paste(build, (x, random.randint(y, y+(tertinggi - build.size[1]))))
                    tertinggi = max(build.size[1], tertinggi)
                    x += build.size[0] + self.padding
                else : break
            y += tertinggi + self.padding
        x = pos[0][0]
        
        #Sama saja , tapi untuk titik paling bawah area
        if abs(pos[1][1] - pos[0][1]) < 120 : return
        while x < pos[1][0]:
            kandidat = getBangunanX(x)
            if len(kandidat):
                build = random.choice(kandidat)
                self.mapDraw.rectangle(((x, pos[1][1]-build.size[1]), (x+build.size[0]+20, pos[1][1]-build.size[1]+build.size[1])),"green")
                self.map.paste(build, (x, pos[1][1]-build.size[1]))
                x += build.size[0] + self.jarak
            else: break
        
    #Fungsi mapping dipanggil untuk memetakan area yang sekirannya bisa dimasukkan bangunan 
    #Biasanya berupa area kotak 
    #Utk algoritmanya dia cari sebuah titik kemudian cari titik tetangga terdekatnya 
    def mapping(self):
        text = ["" for i in range(len(self.simpang))]
        
        #MEncari titik yang akan dijadikan titik orign area
        for idx, titik in enumerate(self.simpang):
            if titik[1] > self.height : continue
            nearX,nearY = 0,0
            #Perulangan untuk mencari titik tetangga terdekat
            for titikTetangga in self.simpang:
                if titik != titikTetangga and titik[0] > 0 and titik[1] > 0:
                    nearX = titikTetangga[0] if  (titikTetangga[0] > nearX and titikTetangga[0] < titik[0] and titik[1] == titikTetangga[1]) else nearX
                    nearY = titikTetangga[1] if  (titikTetangga[1] > nearY and titikTetangga[1] < titik[1]) else nearY
            if idx < len(text) and text[idx] != "":
                text[idx] = ""
            if titik[1] == 1500 : 
                print(titik, ": ", nearX , nearY)
            if titik[0] - nearX >= 30 and titik[1]-nearY >= 30:
                if (titik[0], nearY) not in self.simpang: 
                    text.append("aha")
                    self.simpang.append((titik[0], nearY-20))
                if titik[1] < self.width - 20 : self.mapDraw.rectangle(((nearX+1,nearY+1), (titik[0]-1, titik[1]-1)), "gray")
                self.mapDraw.rectangle(((nearX+10,nearY+10), (titik[0]-10, titik[1]-10)), "green")
                self.generateBuilding(((nearX+10,nearY+10), (titik[0]-10, titik[1]-10)))


myMap = map()
#Attribut yang akan digunakan oleh UI atau mengatur windows  
zoom_factor = 1.0
INITIAL_WIDTH = 500
INITIAL_HEIGHT = 400
viewport_width = 400
viewport_height = 400
viewport_x = INITIAL_WIDTH//2 - (viewport_width//2)
viewport_y = INITIAL_HEIGHT//2 -(viewport_height//2)
new_map = None

#Fungsi yang dipanggil untuk mengupdate map dari tombol generate building
def update_map():
    global new_map, map_label
    new_map  = myMap.createMap()
    print(myMap.simpang)
    cropped_map = new_map.crop((viewport_x, viewport_y, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    update()
    
#Fungsi untuk mengupdate tampilan ketika terjadi zoom in / zoom out / pergeseran map/ viewpoint
def update():
    print("zoom")
    global new_map
    cropped_map = new_map.crop((viewport_x * zoom_factor, viewport_y * zoom_factor, viewport_x* zoom_factor + viewport_width* zoom_factor, viewport_y* zoom_factor + viewport_height* zoom_factor))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    
#Fungsi untuk memperkecil tampilan / viewport
def zoom_in():
    global zoom_factor
    if zoom_factor < 5.0:
        zoom_factor += 0.1
        update()

# Fungsi untuk memperbesar tampilan/ viewport map
def zoom_out():
    global zoom_factor
    if zoom_factor > 0.5:
        zoom_factor -= 0.1
        update()
#Fungsi scroll untk mendapatkan event ketika terjadi scroll pada mouse
#Maka zoom factor atau skala zoom akan diubah berdasarkan arah scrolling
def scroll(event):
    global viewport_x, viewport_y, zoom_factor
    if event.delta > 0:# Scroll ke atas
        if zoom_factor > 0.5: zoom_factor -= 0.1
    else:
        if zoom_factor < 4.0:# Scroll ke bawah
            zoom_factor += 0.1
    update()
            

#Ini fungsi untuk mendeteksi ketika keyword a,s,d,w ditekan
#Dan berfungsi untuk menggeser viewpoint / posisi
def on_key_press(event):
    global viewport_y, viewport_x
    if event.keysym == 'a' and viewport_x > 0:
        viewport_x -= 20
    elif event.keysym == 's' and viewport_y < (INITIAL_HEIGHT  + viewport_height)// zoom_factor:
        viewport_y += 20
    elif event.keysym == 'd' and viewport_x < (INITIAL_WIDTH + viewport_width)// zoom_factor:
        viewport_x += 20
    elif event.keysym == 'w' and  viewport_y > 0:
        viewport_y -= 20
    update()

#Inisialiasi GUI / Interface dari Window Form yang akan ditampilkan kepada user
root = tk.Tk()
root.title("Map Generator")
root.bind("<MouseWheel>", scroll)
root.bind("<KeyPress-a>", on_key_press)
root.bind("<KeyPress-s>", on_key_press)
root.bind("<KeyPress-d>", on_key_press)
root.bind("<KeyPress-w>", on_key_press)
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

map_label = ttk.Label(frame)
map_label.grid(row=0, column=0, padx=10, pady=10)

generate_button = ttk.Button(root, text="Generate Map", command=update_map)
generate_button.grid(row=1, column=0, pady=10)


update_map()
root.mainloop()
        
