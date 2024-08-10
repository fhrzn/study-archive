const routes = (handler) => [
    {
        method: 'POST',
        path: '/albums',
        handler: handler.postAlbumHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'GET',
        path: '/albums',
        handler: handler.getAlbumsHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'GET',
        path: '/albums/{id}',
        handler: handler.getAlbumByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'PUT',
        path: '/albums/{id}',
        handler: handler.putAlbumByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'DELETE',
        path: '/albums/{id}',
        handler: handler.deleteAlbumByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    }
];

module.exports = routes;