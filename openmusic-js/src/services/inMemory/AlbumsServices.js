const nanoid = require('nano-id');
const InvariantError = require('../../exceptions/InvariantError');
const NotFoundError = require('../../exceptions/NotFoundError');

class AlbumsService {
    constructor() {
        this._albums = [];
    }

    addAlbum({ name, year }) {
        const id = nanoid(16);

        const newAlbum = {
            name, year, id
        };

        this._albums.push(newAlbum);

        const isSuccess = this._albums.filter((album) => album.id === id).length > 0;

        if (!isSuccess) {
            throw new InvariantError('Album gagal ditambahkan');
        }

        return id;
    }

    getAlbums() {
        return this._albums;
    }

    getAlbumById(id) {
        const album = this._albums.filter((n) => n.id === id)[0];
        if (!album) {
            throw new NotFoundError('Album tidak ditemukan');
        }

        return album;
    }

    editAlbumById(id, { name, year }) {
        const index = this._albums.findIndex((album) => album.id === id);

        if (index === -1) {
            throw new NotFoundError('Gagal memperbarui album. Id tidak ditemukan');
        }

        this._albums[index] = {
           ...this._albums[index],
            name,
            year
        };
    }

    deleteAlbumById(id) {
        const index = this._albums.findIndex((album) => album.id === id);

        if (index === -1) {
            throw new NotFoundError('Album gagal dihapus. Id tidak ditemukan');
        }

        this._albums.splice(index, 1);
    }
}

module.exports = AlbumsService