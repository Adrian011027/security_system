const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Leer el argumento dinámico (como antes)
const args = process.argv.slice(2);
const dynamicKey = args[0] || '00000000000000';

console.log("🌐 Seed desde JSON iniciado para key:", dynamicKey);

// Ruta del JSON generado por el predictor
const prediccionesPath = path.join(__dirname, 'imagenesActuales.json');
const imagesFolder = path.join(__dirname, 'web', dynamicKey);

const seedImages = async () => {
  try {
    const predicciones = JSON.parse(fs.readFileSync(prediccionesPath, 'utf-8'));

    for (const item of predicciones) {
      const filePath = path.join(imagesFolder, item.filename);

      if (!fs.existsSync(filePath)) {
        console.warn(`⚠️ Imagen no encontrada: ${filePath}`);
        continue;
      }

      const buffer = fs.readFileSync(filePath);
      const base64 = buffer.toString('base64');

      const finalImage = {
        title: item.filename,
        url: `data:image/jpeg;base64,${base64}`,
        path: filePath,
        key: dynamicKey,
        clase: item.clase,
        confidence: item.confidence
      };

      const res = await axios.post('http://143.198.171.247:4321/images', finalImage, {
        headers: { 'Content-Type': 'application/json' }
      });

      console.log(`✅ Imagen enviada: ${item.filename} -> ${res.data.message}`);
    }
  } catch (error) {
    console.error('❌ Error al enviar imágenes:', error.message);
  }
};

seedImages();
