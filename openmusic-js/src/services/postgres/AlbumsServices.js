const nanoid = require('nano-id');
const { Pool } = require('pg');
const InvariantError = require('../../exceptions/InvariantError');
const NotFoundError = require('../../exceptions/NotFoundError');

class AlbumsService {
    constructor() {
        this._albums = [];
        this._pool = new Pool();
    }

    async addAlbum({ name, year }) {
        const id = `album-${nanoid(16)}`;

        const query = {
            text: 'INSERT INTO albums VALUES ($1, $2, $3) RETURNING id',
            values: [id, name, year],
        };

        const result = await this._pool.query(query);

        if (!result.rows[0].id) {
            throw new InvariantError('Album gagal ditambahkan')
        }

        return result.rows[0].id;
    }

    async getAlbums() {
        const result = await this._pool.query('SELECT * FROM albums');
        return result.rows;
    }

    async getAlbumById(id) {
        const queryAlbum = {
            text: 'SELECT * FROM albums WHERE id = $1',
            values: [id],
        };
        const resultAlbum = await this._pool.query(queryAlbum);

        if (!resultAlbum.rows.length) {
            throw new NotFoundError('Album tidak ditemukan');
        }

        const songQuery = {
            text: 'SELECT * FROM songs WHERE album_id = $1',
            values: [resultAlbum.rows[0].id],
        };
        const resultSong = await this._pool.query(songQuery);
        const songs = resultSong.rows.map(({ id, title, performer }) => ({ id, title, performer}))
        
        // return result.rows[0];
        return {...resultAlbum.rows[0], songs };
    }

    async editAlbumById(id, { name, year }) {
        const query = {
            text: 'UPDATE albums SET name = $1, year = $2 WHERE id = $3 RETURNING id',
            values: [name, year, id],
        };
        const result = await this._pool.query(query);

        if (!result.rows.length) {
            throw new NotFoundError('Gagal memperbarui album. Id tidak ditemukan');
        }
    }

    async deleteAlbumById(id) {
        const query = {
            text: 'DELETE FROM albums WHERE id = $1 RETURNING id',
            values: [id],
        };

        const result = await this._pool.query(query);

        if (!result.rows.length) {
            throw new NotFoundError('Album gagal dihapus. Id tidak ditemukan');
        }
    }
}

module.exports = AlbumsService