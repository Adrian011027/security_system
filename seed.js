const mongoose = require('mongoose');
const fs = require('fs'); 
const path = require('path'); 
const Image = require('./models/image.js');

// Obtener el valor de la variable key desde argumentos de la CLI
const args = process.argv.slice(2);
const dynamicKey = args[0] || '00000000000000';  // Valor por defecto si no se pasa un argumento

mongoose.connect('mongodb://143.198.171.247:27017/imageDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});
console.log("Seed")
const seedImages = async () => {
    
    try {
        const images = [
            {
                title: 'Imagen1',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/${dynamicKey}/imagen1.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/${dynamicKey}/imagen1.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen2',
                url: `data:image/jpeg;base64,${fs.readFileSync(path.join(__dirname, `./web/${dynamicKey}/imagen2.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/${dynamicKey}/imagen2.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen3',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/${dynamicKey}/imagen3.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/${dynamicKey}/imagen3.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen4',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/${dynamicKey}/imagen4.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/${dynamicKey}/imagen4.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen5',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/${dynamicKey}/imagen5.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/${dynamicKey}/imagen5.jpg`),
                key: dynamicKey,
            },
        ];

        await Image.insertMany(images);
        console.log('Imágenes agregadas con key:', dynamicKey);
    }  /*
    try {
        const images = [
            {
                title: 'Imagen1',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/20250306161027/imagen1.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/20250306161027/imagen1.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen2',
                url: `data:image/jpeg;base64,${fs.readFileSync(path.join(__dirname, `./web/20250306161027/imagen2.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/20250306161027/imagen2.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen3',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/20250306161027/imagen3.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/20250306161027/imagen3.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen4',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/20250306161027/imagen4.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./web/20250306161027/imagen4.jpg`),
                key: dynamicKey,
            },
            {
                title: 'Imagen5',
                url: `data:image/jpg;base64,${fs.readFileSync(path.join(__dirname, `./web/20250306161027/imagen5.jpg`)).toString('base64')}`,
                path: path.join(__dirname, `./ladron5.jpg`),
                key: dynamicKey,
            },
        ];

        await Image.insertMany(images);
        console.log('Imágenes agregadas con key:', dynamicKey);
    }*/
    catch (error) {
    console.error('Error al agregar las imágenes:', error);
    } finally {
        mongoose.connection.close();
    }
};

seedImages();
