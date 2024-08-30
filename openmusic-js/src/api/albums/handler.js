const autoBind = require("auto-bind");

class AlbumsHandler {
    constructor(service, validator) {
        this._service = service;
        this._validator = validator;

        autoBind(this);
    }

    async postAlbumHandler(request, h) {
        this._validator.validateAlbumPayload(request.payload);

        const albumId = await this._service.addAlbum(request.payload);

        const response = h.response({
            status:'success',
            message: 'Album berhasil ditambahkan',
            data: { albumId }
        });
        response.code(201);
        return response;
    }

    async getAlbumsHandler() {
        const albums = await this._service.getAlbums();
        return {
            status:'success',
            data: { albums }
        };
    }

    async getAlbumByIdHandler(request) {
        const { id } = request.params;
        const album = await this._service.getAlbumById(id);
        return {
            status:'success',
            data: { album }
        };
    }

    async putAlbumByIdHandler(request) {
        this._validator.validateAlbumPayload(request.payload);
        const { id } = request.params;
        await this._service.editAlbumById(id, request.payload);

        return {
            status:'success',
            message: 'Album berhasil diperbarui'
        };
    }

    async deleteAlbumByIdHandler(request) {
        const { id } = request.params;
        await this._service.deleteAlbumById(id);
        return {
            status:'success',
            message: 'Album berhasil dihapus'
        };
    }

    async likeAlbumByIdHandler(request, h) {
        const { id } = request.params;
        const { id: userId } = request.auth.credentials;

        await this._service.getAlbumById(id)

        await this._service.likeAlbumById(id, userId);

        const response = h.response({
            status:'success',
            message: 'Album berhasil ditambahkan ke favorit'
        });
        response.code(201);
        return response;
    }

    async dislikeAlbumByIdHandler(request) {
        const { id } = request.params;
        const { id: userId } = request.auth.credentials;

        await this._service.getAlbumById(id)

        await this._service.dislikeAlbumById(id, userId);

        return {
            status:'success',
            message: 'Album berhasil dikeluarkan dari favorit'
        };
    }

    async getAlbumLikesByIdHandler(request) {
        const { id } = request.params;

        await this._service.getAlbumById(id);

        const likes = await this._service.getAlbumLikesById(id);
        likes.likes = +likes.likes

        return {
            status: 'success',
            data: likes
        }
        
    }
}

module.exports = AlbumsHandler;