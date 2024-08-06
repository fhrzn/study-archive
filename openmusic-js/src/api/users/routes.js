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
    },
    // {
    //     method: 'POST',
    //     path: '/users',
    //     handler: handler.postUserHandler,
    // },
    // {
    //     method: 'POST',
    //     path: '/users',
    //     handler: handler.postUserHandler,
    // },
    // {
    //     method: 'POST',
    //     path: '/users',
    //     handler: handler.postUserHandler,
    // },
    // {
    //     method: 'POST',
    //     path: '/users',
    //     handler: handler.postUserHandler,
    // },
];

module.exports = routes;