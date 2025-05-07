const mongoose = require('mongoose');

const imageSchema = new mongoose.Schema({
    title: String,
    url: String,
    path: String,
    key: String,
    clase: String,      
    confidence: Number  
});

const Image = mongoose.model('Image', imageSchema);

module.exports = Image;
