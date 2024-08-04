const nanoid = require('nano-id');
const InvariantError = require('../../exceptions/InvariantError');
const NotFoundError = require('../../exceptions/NotFoundError');

class SongsService {
    constructor() {
        this._songs = [];
    }

    addSong({ title, year, genre, performer, duration, albumId }) {
        const id = nanoid(16);

        const newSong = {
            title, year, genre, performer, duration, albumId, id
        };

        this._songs.push(newSong);

        const isSuccess = this._songs.filter((song) => song.id === id).length > 0;

        if (!isSuccess) {
            throw new InvariantError('Lagu gagal ditambahkan');
        }

        return id;
    }

    getSongs() {
        return this._songs;
    }

    getSongById(id) {
        const song = this._songs.filter((n) => n.id === id)[0];
        if (!song) {
            throw new NotFoundError('Lagu tidak ditemukan');
        }

        return song;
    }

    editSongById(id, { title, year, genre, performer, duration, albumId }) {
        const index = this._songs.findIndex((song) => song.id === id);

        if (index === -1) {
            throw new NotFoundError('Gagal memperbarui lagu. Id tidak ditemukan');
        }

        this._songs[index] = {
           ...this._songs[index],
            title,
            year,
            genre,
            performer,
            duration,
            albumId
        };
    }

    deleteSongById(id) {
        const index = this._songs.findIndex((song) => song.id === id);

        if (index === -1) {
            throw new NotFoundError('Lagu gagal dihapus. Id tidak ditemukan');
        }

        this._songs.splice(index, 1);
    }
}

module.exports = SongsService;