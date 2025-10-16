from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    """
    Endpoint to remove background from an uploaded image.
    Expects form-data with key 'image'.
    Returns a PNG image without background.
    """
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400

    file = request.files['image']
    input_image = file.read()

    try:
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

    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == "__main__":
    # Use PORT from environment (Render) or default 5050 locally
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
