from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400

    file = request.files['image']
    input_image = file.read()

    # Remove background
    output_image = remove(input_image)

    # Convert bytes to PNG
    img = Image.open(io.BytesIO(output_image))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Send image with proper header
    return send_file(
        img_byte_arr,
        mimetype='image/png',
        as_attachment=False,
        download_name='output.png'
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # default to 5050 locally
    app.run(host="0.0.0.0", port=port)

