/**
 * @type {import('node-pg-migrate').ColumnDefinitions | undefined}
 */

/**
 * @param pgm {import('node-pg-migrate').MigrationBuilder}
 * @param run {() => void | undefined}
 * @returns {Promise<void> | void}
 */
exports.up = (pgm) => {
    pgm.createTable('songs', {
        id: {
            type: 'VARCHAR(50)',
            primaryKey: true,
        },
        title: {
            type: 'VARCHAR(100)',
            notNull: true,
        },
        year: {
            type: 'INTEGER',
            notNull: true,
        },
        genre: {
            type: 'VARCHAR(100)',
            notNull: true,
        },
        performer: {
            type: 'VARCHAR(100)',
            notNull: true,
        },
        duration: {
            type: 'INTEGER',
            notNull: false,
        },
        album_id: {
            type: 'VARCHAR(50)',
            notNull: false
        }
    });

    pgm.addConstraint('songs', 'fk_songs.album.id', 'FOREIGN KEY(album_id) REFERENCES albums (id) ON DELETE CASCADE');
};

/**
 * @param pgm {import('node-pg-migrate').MigrationBuilder}
 * @param run {() => void | undefined}
 * @returns {Promise<void> | void}
 */
exports.down = (pgm) => {
    pgm.dropConstraint('songs', 'fk_songs.album.id');
    pgm.dropTable('songs')
};
