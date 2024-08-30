const nanoid = require('nano-id');
const { Pool } = require('pg');
const InvariantError = require('../../exceptions/InvariantError');
const AuthorizationError = require('../../exceptions/AuthorizationError');
const NotFoundError = require('../../exceptions/NotFoundError');

class PlaylistService {
    constructor() {
        this._pool = new Pool();
    }

    async addPlaylist({ name, owner }) {
        const id = `playlist-${nanoid(16)}`;

        const query = {
            text: 'INSERT INTO playlists VALUES ($1, $2, $3) RETURNING id',
            values: [id, name, owner],
        };

        const result = await this._pool.query(query);

        if (!result.rows[0].id) {
            throw new InvariantError('Playlist gagal ditambahkan');
        }

        return result.rows[0].id;
    }

    async getPlaylists(owner) {
        const query = {
            text: 'SELECT p.id, p.name, u.username FROM playlists p LEFT JOIN users u ON p.owner = u.id WHERE p.owner = $1',
            values: [owner],
        };

        const result = await this._pool.query(query);
        return result.rows;
    }

    async verifyPlaylistOwner(id, owner) {
        const query = {
            text: 'SELECT id, owner FROM playlists WHERE id = $1',
            values: [id],
        };

        const result = await this._pool.query(query);
        
        if (!result.rows.length) {
            throw new NotFoundError('Playlist tidak ditemukan');
        }
        
        const playlist = result.rows[0];

        if (playlist.owner !== owner) {
            throw new AuthorizationError('Anda tidak berhak mengakses resource ini');
        }
    }

    async deletePlaylist(id, owner) {
        await this.verifyPlaylistOwner(id, owner);

        const query = {
            text: 'DELETE FROM playlists WHERE id = $1 RETURNING id',
            values: [id],
        };
        const result = await this._pool.query(query);

        if (!result.rows.length) {
            throw new NotFoundError('Gagal menghapus playlist. Id tidak ditemukan');
        }
    }

    async addSongToPlaylist(playlistId, owner, songId) {
        await this.verifyPlaylistOwner(playlistId, owner);

        const songQuery = {
            text: 'SELECT id FROM songs WHERE id = $1',
            values: [songId],
        }

        const songResult = await this._pool.query(songQuery);
        if (!songResult.rows.length) {
            throw new NotFoundError('Gagal menambahkan musik ke playlist. Id tidak ditemukan');
        }
        
        const playlistSongId = `pl-song-${nanoid(16)}`;
        const query = {
            text: 'INSERT INTO playlist_songs VALUES ($1, $2, $3) RETURNING id',
            values: [playlistSongId, playlistId, songId],
        };

        const result = await this._pool.query(query);

        if (!result.rows[0].id) {
            throw new InvariantError('Gagal menambahkan musik ke playlist');
        }

        return result.rows[0].id;
    }

    async getSongsFromPlaylist(playlistId, owner) {
        await this.verifyPlaylistOwner(playlistId, owner);

        const queryPlaylist = {
            text: 'SELECT p.id, p.name, u.username FROM playlists p LEFT JOIN users u ON p.owner = u.id WHERE p.id = $1',
            values: [playlistId],
        }
        
        const resultPlaylist = await this._pool.query(queryPlaylist);

        if (!resultPlaylist.rows.length) {
            throw new NotFoundError('Playlist tidak ditemukan');
        }

        const query = {
            text: 'SELECT s.id, s.title, s.performer FROM songs s JOIN playlist_songs ps ON s.id = ps.song_id WHERE ps.playlist_id = $1',
            values: [playlistId],
        };

        const result = await this._pool.query(query);
        const songs = result.rows.map(({ id, title, performer }) => ({ id, title, performer }));

        return {...resultPlaylist.rows[0], songs};
    }

    async removeSongFromPlaylist(playlistId, owner, songId) {
        
        await this.verifyPlaylistOwner(playlistId, owner);

        const query = {
            text: 'DELETE FROM playlist_songs WHERE playlist_id = $1 AND song_id = $2 RETURNING id',
            values: [playlistId, songId],
        };

        const result = await this._pool.query(query);

        if (!result.rows.length) {
            throw new NotFoundError('Gagal menghapus musik dari playlist. Id musik atau playlist tidak ditemukan');
        }
    }
}

module.exports = PlaylistService;