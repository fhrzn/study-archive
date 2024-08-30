const routes = (handler) => [
    {
        method: 'POST',
        path: '/users',
        handler: handler.postUserHandler,
    },
    {
        method: 'GET',
        path: '/users/{id}',
        handler: handler.getUserByIdHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
];

module.exports = routes;