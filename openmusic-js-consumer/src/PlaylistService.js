const { Pool } = require('pg');

class PlaylistService {
    constructor() {
        this._pool = new Pool();
    }

    async getPlaylists(playlistId) {

        const queryPlaylist = {
            text: 'SELECT id, name FROM playlists p WHERE id = $1',
            values: [playlistId],
        };

        const resultPlaylist  = await this._pool.query(queryPlaylist);

        const query = {
            text: 'SELECT s.id, s.title, s.performer FROM songs s JOIN playlist_songs ps ON s.id = ps.song_id WHERE ps.playlist_id = $1',
            values: [playlistId],
        };

        const result = await this._pool.query(query);
        const songs = result.rows.map(({ id, title, performer }) => ({ id, title, performer }));

        return {...resultPlaylist.rows[0], songs};
    }
}

module.exports = PlaylistService;