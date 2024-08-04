const nanoid = require('nano-id');
const { Pool } = require('pg');
const InvariantError = require('../../exceptions/InvariantError');
const NotFoundError = require('../../exceptions/NotFoundError');

class SongsService {
    constructor() {
        this._songs = [];
        this._pool = new Pool();
    }

    async addSong({ title, year, genre, performer, duration, albumId }) {
        const id = nanoid(16);

        const query = {
            text: 'INSERT INTO songs VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id',
            values: [id, title, year, genre, performer, duration, albumId],
        }

        const result = await this._pool.query(query);

        if (!result.rows[0].id) {
            throw new InvariantError('Lagu gagal ditambahkan');
        }

        return result.rows[0].id;
    }

    async getSongs(title, performer) {
        let queryStr = 'SELECT * FROM songs';
        let values = [];
        if (title && performer) {
            queryStr += ` WHERE title ILIKE $1 AND performer ILIKE $2`;
            values.push(`%${title}%`, `%${performer}%`)
        }
        else if (title) {
            queryStr += ` WHERE title ILIKE $1`;
            values.push(`%${title}%`)
        }
        else if (performer) {
            queryStr += ` WHERE performer ILIKE $1`;
            values.push(`%${performer}%`)
        }

        const query = {
            text: queryStr,
            values: values,
        }
        const result = await this._pool.query(query);
        return result.rows.map(({ id, title, performer }) => ({ id, title, performer}));
    }

    async getSongById(id) {
        const query = {
            text: 'SELECT * FROM songs WHERE id = $1',
            values: [id],
        };
        const result = await this._pool.query(query);

        if (!result.rows.length) {
            throw new NotFoundError('Lagu tidak ditemukan');
        }

        return result.rows[0];
    }

    async editSongById(id, { title, year, genre, performer, duration, albumId }) {
        const query = {
            text: 'UPDATE songs SET title = $1, year = $2, genre = $3, performer = $4, duration = $5, album_id = $6 WHERE id = $7 RETURNING id',
            values: [title, year, genre, performer, duration, albumId || null, id],
        }
        const result = await this._pool.query(query);
        
        if (!result.rows.length) {
            throw new NotFoundError('Gagal memperbarui lagu. Id tidak ditemukan');
        }
    }

    async deleteSongById(id) {
        const query = {
            text: 'DELETE FROM songs WHERE id = $1 RETURNING id',
            values: [id],
        }
        const result = await this._pool.query(query);

        if (!result.rows.length) {
            throw new NotFoundError('Lagu gagal dihapus. Id tidak ditemukan');
        }
    }
}

module.exports = SongsService;