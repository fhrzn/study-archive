const routes = (handler) => [
    {
        method: 'POST',
        path: '/authentications',
        handler: handler.postAuthenticationHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'PUT',
        path: '/authentications',
        handler: handler.putAuthenticationHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
    {
        method: 'DELETE',
        path: '/authentications',
        handler: handler.deleteAuthenticationHandler,
        // options: {
        //     auth: 'openmusic_jwt'
        // }
    },
]

module.exports = routes;