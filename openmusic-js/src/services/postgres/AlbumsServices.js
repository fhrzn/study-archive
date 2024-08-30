const nanoid = require('nano-id');
const { Pool } = require('pg');
const InvariantError = require('../../exceptions/InvariantError');
const NotFoundError = require('../../exceptions/NotFoundError');

class AlbumsService {
    constructor(cacheService) {
        this._albums = [];
        this._pool = new Pool();
        this._cacheService = cacheService;
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
        
        
        const { cover, ...item } = resultAlbum.rows[0];
        return {...item, coverUrl: cover, songs};
    }

    async editAlbumById(id, { name, year, cover }) {
        const query = {
            text: 'UPDATE albums SET name = $1, year = $2, cover = $3 WHERE id = $4 RETURNING id',
            values: [name, year, cover, id],
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

    async likeAlbumById(albumId, userId) {
        const checkLikeExistQuery = {
            text: 'SELECT user_id FROM user_album_likes WHERE album_id = $1 AND user_id = $2',
            values: [albumId, userId],
        }
        
        const resultLike = await this._pool.query(checkLikeExistQuery);

        if (resultLike.rows.length > 0) {
            throw new InvariantError('Anda sudah menyukai album ini');
        }

        const id = `user-album-like-${nanoid(16)}`;
        const query = {
            text: 'INSERT INTO user_album_likes VALUES ($1, $2, $3) RETURNING id',
            values: [id, userId, albumId],
        };

        const results = await this._pool.query(query);
        

        if (!results.rows[0].id) {
            throw new InvariantError('Gagal menyukai album');
        }

        this._cacheService.delete(`user-album-likes:${albumId}`);

        return results.rows[0].id;
    }

    async dislikeAlbumById(albumId, userId) {
        const query = {
            text: 'DELETE FROM user_album_likes WHERE album_id = $1 AND user_id = $2 RETURNING id',
            values: [albumId, userId],
        };

        const results = await this._pool.query(query);

        if (!results.rows.length) {
            throw new InvariantError('Gagal batal menyukai album');
        }

        this._cacheService.delete(`user-album-likes:${albumId}`);

        return results.rows[0].id;
    }

async getAlbumLikesById(id) {
        try {
            const result = await this._cacheService.get(`user-album-likes:${id}`);
            // return JSON.parse(result);
            return {
                isCache: true,
                likes: JSON.parse(result)
            }
        } catch {
            const query = {
                text: "SELECT COUNT(1) AS likes FROM user_album_likes WHERE album_id = $1",
                values: [id],
            };

            const result = await this._pool.query(query);

            await this._cacheService.set(`user-album-likes:${id}`, JSON.stringify(result.rows[0]));

            return {
                isCache: false,
                likes: result.rows[0]
            }
        }
    }
}

module.exports = AlbumsService