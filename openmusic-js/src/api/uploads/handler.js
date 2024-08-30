const autoBind = require('auto-bind');

class UploadsHandler {
    constructor(uploadService, albumService, validator) {
        this._uploadService = uploadService;
        this._albumService = albumService;
        this._validator = validator;

        autoBind(this);
    }

    async postUploadAlbumCoverHandler(request, h) {
        
        const { cover } = request.payload;
        
        this._validator.validateImageHeaders(cover.hapi.headers);
        
        
        const album = await this._albumService.getAlbumById(request.params.albumId)

        const filename = await this._uploadService.writeFile(cover, cover.hapi);

        album.cover = `http://${process.env.HOST}:${process.env.PORT}/upload/images/${filename}`

        await this._albumService.editAlbumById(album.id, album);
        

        const response = h.response({
            status: 'success',
            message: "Sampul berhasil diunggah"
            // data: {
            //     fileLocation: `http://${process.env.HOST}:${process.env.PORT}/upload/images/${filename}`,
            // },
        });

        response.code(201);
        return response;
    }

    testUploadHandler() {
        console.log("masuk");
        
    }
}

module.exports = UploadsHandler;