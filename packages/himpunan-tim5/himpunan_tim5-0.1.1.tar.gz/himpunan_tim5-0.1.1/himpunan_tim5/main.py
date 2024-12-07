class Himpunan:
    def __init__(self, *elements):
        # Inisialisasi himpunan dengan elemen unik
        self.data = list(set(elements))
    
    def __repr__(self):
        # Representasi string untuk mencetak objek
        return f"({', '.join(map(str, self.data))})"
    
    def __len__(self):
        # Mengembalikan jumlah elemen dalam himpunan
        return len(self.data)
    
    def __contains__(self, item):
        # Mengecek apakah item ada dalam himpunan
        return item in self.data
    
    def __eq__(self, other):
        # Mengecek apakah dua himpunan sama
        return set(self.data) == set(other.data)
    
    def __le__(self, other):
        # Mengecek apakah self subset dari other
        return all(item in other.data for item in self.data)
    
    def __lt__(self, other):
        # Mengecek apakah self proper subset dari other
        return self <= other and len(self) < len(other)
    
    def __ge__(self, other):
        # Mengecek apakah self superset dari other
        return all(item in self.data for item in other.data)
    
    def __floordiv__(self, other):
        # Mengecek ekuivalensi dua himpunan
        return set(self.data) == set(other.data)
    
    def __add__(self, other):
        # Gabungan (union)
        return Himpunan(*(self.data + other.data))
    
    def __iadd__(self, item):
        # Menambah elemen ke himpunan menggunakan +=
        if item not in self.data:
            self.data.append(item)
        return self
    
    def __sub__(self, other):
        # Selisih (difference)
        return Himpunan(*(item for item in self.data if item not in other.data))
    
    def __truediv__(self, other):
        # Irisan (intersection)
        return Himpunan(*(item for item in self.data if item in other.data))
    
    def __mul__(self, other):
        # Selisih simetris (symmetric difference)
        return (self - other) + (other - self)
    
    def __pow__(self, other):
        # Hasil kali Cartesian
        return [(a, b) for a in self.data for b in other.data]
    
    def __abs__(self):
        # Menghitung himpunan kuasa
        from itertools import chain, combinations
        power_set = list(chain.from_iterable(combinations(self.data, r) for r in range(len(self.data) + 1)))
        return len(power_set)
    
    def ListKuasa(self):
        # Mengembalikan daftar elemen himpunan kuasa
        from itertools import chain, combinations
        return list(chain.from_iterable(combinations(self.data, r) for r in range(len(self.data) + 1)))
    
    def tambah(self, item):
        # Menambah elemen ke himpunan
        if item not in self.data:
            self.data.append(item)
    
    def hapus(self, item):
        # Menghapus elemen dari himpunan
        if item in self.data:
            self.data.remove(item)
    
    def complement(self, universal):
        # Menghitung komplemen terhadap himpunan universal
        return Himpunan(*(item for item in universal.data if item not in self.data))


