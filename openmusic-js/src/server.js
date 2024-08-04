require('dotenv').config();

const Hapi = require('@hapi/hapi');
const albums = require('./api/albums');
const songs = require('./api/songs');
const AlbumsService = require('./services/postgres/AlbumsServices');
const SongsService = require('./services/postgres/SongsServices');
const AlbumsValidator = require('./validator/albums');
const SongsValidator = require('./validator/songs');
const ClientError = require('./exceptions/ClientError');

const init = async () => {
    const albumsService = new AlbumsService();
    const songsService = new SongsService();
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