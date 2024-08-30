const Joi = require('joi');

const PostPlaylistPayloadSchema = Joi.object({
    name: Joi.string().required()
});

const PostPlaylistSongPayloadSchema = Joi.object({
    songId: Joi.string().required()
});

module.exports = {
    PostPlaylistPayloadSchema,
    PostPlaylistSongPayloadSchema,
};