require('dotenv').config();
const ClientError = require('./exceptions/ClientError');

const Hapi = require('@hapi/hapi');
const albums = require('./api/albums');
const AlbumsService = require('./services/postgres/AlbumsServices');
const AlbumsValidator = require('./validator/albums');

const songs = require('./api/songs');
const SongsService = require('./services/postgres/SongsServices');
const SongsValidator = require('./validator/songs');

const users = require('./api/users');
const UsersService = require('./services/postgres/UsersServices');
const UsersValidator = require('./validator/users');

const init = async () => {
    const albumsService = new AlbumsService();
    const songsService = new SongsService();
    const usersService = new UsersService();
    const server = Hapi.server({
        port: process.env.PORT,
        host: process.env.HOST,
        routes: {
            cors: {
                origin: ['*'],
            },
        },
    });

    await server.register({
        plugin: albums,
        options: {
            service: albumsService,
            validator: AlbumsValidator
        }
    });

    await server.register({
        plugin: songs,
        options: {
            service: songsService,
            validator: SongsValidator
        }
    });

    await server.register({
        plugin: users,
        options: {
            service: usersService,
            validator: UsersValidator
        }
    })

    server.ext('onPreResponse', (request, h) => {
        const { response } = request;

        if (response instanceof ClientError) {
            const newResponse = h.response({
                status: 'fail',
                message: response.message,
            });
            newResponse.code(response.statusCode);
            return newResponse;
        }

        return h.continue;
    });

    await server.start();
    console.log(`Server running at: ${server.info.uri}`);
};

init();