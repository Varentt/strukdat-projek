class MaxHeap:
    def __init__(self):
        self.heap = []

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # --- CORE HEAP OPERATIONS ---
    def heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index]['nilai'] > self.heap[parent]['nilai']:
            self.swap(index, parent)
            self.heapify_up(parent)

    def heapify_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index

        if left < len(self.heap) and self.heap[left]['nilai'] > self.heap[largest]['nilai']:
            largest = left

        if right < len(self.heap) and self.heap[right]['nilai'] > self.heap[largest]['nilai']:
            largest = right

        if largest != index:
            self.swap(index, largest)
            self.heapify_down(largest)

    # --- INSERT ---
    def insert(self, nama, nilai, kelas=None):
        nama = nama.lower()

        for siswa in self.heap:
            if siswa['nama'].lower() == nama and siswa['kelas'] == kelas:
                return False

        self.heap.append({"nama": nama, "nilai": nilai, "kelas": kelas})
        self.heapify_up(len(self.heap) - 1)
        return True

    # --- EXTRACT MAX ---
    def extract_max(self):
        if not self.heap:
            return None
        
        root = self.heap[0]
        last_item = self.heap.pop()

        if self.heap:
            self.heap[0] = last_item
            self.heapify_down(0)

        return root

    # --- UPDATE NILAI ---
    def update_nilai(self, nama, nilai_baru, kelas=None):
        nama = nama.lower()
        index = -1

        for i, siswa in enumerate(self.heap):
            if siswa['nama'].lower() == nama and (kelas is None or siswa['kelas'] == kelas):
                index = i
                break

        if index == -1:
            return False

        nilai_lama = self.heap[index]['nilai']
        self.heap[index]['nilai'] = nilai_baru

        if nilai_baru > nilai_lama:
            self.heapify_up(index)
        else:
            self.heapify_down(index)

        return True

    # --- DELETE ---
    def delete_siswa(self, nama, kelas=None):
        nama = nama.lower()
        index = -1

        for i, siswa in enumerate(self.heap):
            if siswa['nama'].lower() == nama and (kelas is None or siswa['kelas'] == kelas):
                index = i
                break

        if index == -1:
            return False

        last_index = len(self.heap) - 1
        self.swap(index, last_index)

        deleted_item = self.heap.pop()

        if index < len(self.heap):
            parent = (index - 1) // 2
            if index > 0 and self.heap[index]['nilai'] > self.heap[parent]['nilai']:
                self.heapify_up(index)
            else:
                self.heapify_down(index)

        return deleted_item

    # --- GET SORTED DATA ---
    def get_sorted_data(self):
        temp_heap = MaxHeap()
        temp_heap.heap = self.heap.copy()

        sorted_result = []
        while temp_heap.heap:
            sorted_result.append(temp_heap.extract_max())

        return sorted_result

    # --- REMEDIAL ---
    def get_remedial_students(self, kkm):
        remedial = [s for s in self.heap if s['nilai'] < kkm]
        remedial.sort(key=lambda x: x['nilai'])
        return remedial
