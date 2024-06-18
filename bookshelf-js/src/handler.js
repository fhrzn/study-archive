const nanoId = require('nano-id');
const books = require('./books');

const addBookHandler = (request, h) => {
    const { 
        name,
        year,
        author,
        summary,
        publisher,
        pageCount,
        readPage,
        reading
    } = request.payload;

    // validate
    if (!name || name === null || name === undefined === name === '') {
        const response = h.response({
            status: 'fail',
            message: 'Gagal menambahkan buku. Mohon isi nama buku'
        });
        response.code(400);
        return response;
    }
        
    if (readPage > pageCount) {
        const response = h.response({
            status: 'fail',
            message: 'Gagal menambahkan buku. readPage tidak boleh lebih besar dari pageCount'
        });
        response.code(400);
        return response;    
    }

    const id = nanoId(16);
    const finished = readPage === pageCount ? true : false;
    const insertedAt = new Date().toISOString();
    const updatedAt = insertedAt;

    const newBook = {
        id, name, year, author, summary, publisher, pageCount, readPage, finished, reading, insertedAt, updatedAt
    };

    books.push(newBook);

    const isSuccess = books.filter((book) => book.id === id).length > 0;

    if (isSuccess) {
        const response = h.response({
            status: 'success',
            message: 'Buku berhasil ditambahkan',
            data: {
                "bookId": id
            }
        });
        response.code(201);
        return response;
    }

    const response = h.response({
        status: 'fail',
        message: 'Buku gagal ditambahkan',
    });
    response.code(500);
    return response;

};


const getAllBooksHandler = (request, h) => {
    const { name, reading, finished } = request.query;

    let allBooks = books;
    if (name !== undefined) {
        allBooks = books.filter((book) => book.name.toLowerCase().includes(name.toLowerCase()));
    }

    if (reading !== undefined) {
        allBooks = books.filter((book) => book.reading == (reading == 1 ? true : false));
    }
    
    if (finished !== undefined) {
        allBooks = books.filter((book) => book.finished == (finished == 1 ? true : false));
    }

    const response = h.response({
        status: 'success',
        data: {
            books: allBooks.map(({ id, name, publisher}) => ({ id, name, publisher }))
        },
    });
    return response;
};


const getBookByIdHandler = (request, h) => {
    const { id } = request.params;

    const book = books.filter((book) => book.id === id)[0];

    if (book !== undefined) {
        return {
            status: 'success',
            data: {
                book,
            }
        };
    }

    const response = h.response({
        status: 'fail',
        message: 'Buku tidak ditemukan'
    });
    response.code(404);
    return response;
};


const editBookByIdHandler = (request, h) => {
    const { id } = request.params;
    const { 
        name,
        year,
        author,
        summary,
        publisher,
        pageCount,
        readPage,
        reading
    } = request.payload;

    // validate
    const index = books.findIndex((book) => book.id === id);
    if (index === -1) {
        const response = h.response({
            status: 'fail',
            message: 'Gagal memperbarui buku. Id tidak ditemukan',
        });
        response.code(404);
        return response;
    }

    if (!name || name === null || name === undefined === name === '') {
        const response = h.response({
            status: 'fail',
            message: 'Gagal memperbarui buku. Mohon isi nama buku'
        });
        response.code(400);
        return response;
    }
        
    if (readPage > pageCount) {
        const response = h.response({
            status: 'fail',
            message: 'Gagal memperbarui buku. readPage tidak boleh lebih besar dari pageCount'
        });
        response.code(400);
        return response;    
    }

    const updatedAt = new Date().toISOString();
    const finished = readPage === pageCount ? true : false;
    books[index] = {
        ...books[index],
        name,
        year,
        author,
        summary,
        publisher,
        pageCount,
        readPage,
        finished,
        reading,
        updatedAt
    };
    
    const response = h.response({
        status: 'success',
        message: 'Buku berhasil diperbarui'
    });
    response.code(200);
    return response;
}


const deleteBookByIdHandler = (request, h) => {
    const { id } = request.params;

    const index = books.findIndex((book) => book.id === id);

    if (index !== -1) {
        books.splice(index, 1);
        const response = h.response({
            status: 'success',
            message: 'Buku berhasil dihapus'
        });
        response.code(200);
        return response;
    }

    const response = h.response({
        status: "fail",
        message: "Buku gagal dihapus. Id tidak ditemukan",
    });
    response.code(404);
    return response;
}


module.exports = { addBookHandler, getAllBooksHandler, getBookByIdHandler, editBookByIdHandler, deleteBookByIdHandler }