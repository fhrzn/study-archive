const routes = (handler) => [
    {
        method: 'POST',
        path: '/songs',
        handler: handler.postSongHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'GET',
        path: '/songs',
        handler: handler.getSongsHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'GET',
        path: '/songs/{id}',
        handler: handler.getSongByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'PUT',
        path: '/songs/{id}',
        handler: handler.putSongByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'DELETE',
        path: '/songs/{id}',
        handler: handler.deleteSongByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    }
];

module.exports = routes;