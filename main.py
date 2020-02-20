from operator import attrgetter


class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = int(score)
        
    def __repr__(self):
        return f'Book(id={self.id},score={self.score})'


class Library:
    def __init__(self, id, books, shippable, sign_time):
        self.id = id
        self.books = books
        self.n_books = len(books)
        self.sign_time = sign_time
        self.shippable = shippable
        self.sorted_books = sorted(books, key=attrgetter('score'), reverse=True)
        self.max_score = self._calc_score(self.sorted_books)
    
    def _calc_score(self, books):
        return sum([b.score for b in books])
    
    def get_max_score_timed(self, signup_day, limit):
        availabel_time = limit - (self.sign_time + signup_day)
        
        if availabel_time < 0:
            availabel_time = 0
        
        n_books_scanable = min(availabel_time // self.shippable, self.n_books)
        
        books_scanable = self.sorted_books[:n_books_scanable]
        return self._calc_score(books_scanable)
    
    def __repr__(self):
        return f'Lib(id={self.id},n_books={self.n_books},max_score={self.max_score})'

    
def find_book(books, book_id):
    for book in books:
        if book.id == book_id:
            return book
    print(f'book {book_id} not found')
    return None


def get_book_list(books, book_ids):
    book_list = []
    for b_id in book_ids:
        book = find_book(books, int(b_id))
        if book:
            book_list.append(book)
    return book_list


def init(file_name):
    with open(file_name, 'r') as f:
        a = f.readline().split()
        limit = a[2]
        n_libs = int(a[1])
        b = f.readline().split()
        books = [Book(i, s) for i, s in enumerate(b)]
        
        libs = []
        for l_id in range(n_libs):
            l = f.readline()
            l_b = f.readline().split()
            lib = Library(int(l_id), get_book_list(books, l_b), l[2], l[1])
            libs.append(lib)
        
        sorted_libs = sorted(libs, key=attrgetter('max_score'), reverse=True)
        
        with open('out.txt', 'w') as o:
            o.write(f'{str(n_libs)}\n')
            for lib in sorted_libs:
                sent_books = ' '.join([str(bk.id) for bk in lib.sorted_books])
                o.write(f'{lib.id} {len(sent_books)}\n')
                o.write(f'{sent_books}\n')
                
init('b_read_on.txt')