const routes = (handler) => [
    {
        method: 'POST',
        path: '/playlists',
        handler: handler.postPlaylistHandler,
        options: {
            auth: 'openmusic_jwt'
        }
    },
    {
        method: 'GET',
        path: '/playlists',
        handler: handler.getPlaylistsHandler,
        options: {
            auth: 'openmusic_jwt'
        }
    },
    {
        method: 'DELETE',
        path: '/playlists/{id}',
        handler: handler.deletePlaylistHandler,
        options: {
            auth: 'openmusic_jwt'
        }
    },
    {
        method: 'POST',
        path: '/playlists/{id}/songs',
        handler: handler.postSongToPlaylist,
        options: {
            auth: 'openmusic_jwt'
        }
    },
    {
        method: 'GET',
        path: '/playlists/{id}/songs',
        handler: handler.getSongsFromPlaylist,
        options: {
            auth: 'openmusic_jwt'
        }
    },
    {
        method: 'DELETE',
        path: '/playlists/{id}/songs',
        handler: handler.deleteSongFromPlaylist,
        options: {
            auth: 'openmusic_jwt'
        }
    }
];

module.exports = routes;