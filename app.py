from flask import Flask, render_template, request, url_for
import qrcode
import os
from PIL import Image

app = Flask(__name__)

# Ensure necessary folders exist
os.makedirs('static/images/qr_codes', exist_ok=True)
os.makedirs('static/images/qr_codes_templates', exist_ok=True)
os.makedirs('static/qr_templates', exist_ok=True)


def get_template_names():
    """Return the list of available template filenames in the qr_templates folder."""
    return [f for f in os.listdir('static/qr_templates') if f.endswith('.png')]


@app.route('/')
def index():
    return render_template(
        'index.html',
        qr_code=None,
        qr_code_name=None,
        templates=get_template_names(),
        final_code=None
    )


@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    name = request.form['name']
    size = int(request.form['size'])

    # Generate QR code
    qr = qrcode.QRCode(version=size, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image
    qr_code_file = f'static/images/qr_codes/{name}.png'
    img.save(qr_code_file)

    return render_template(
        'index.html',
        qr_code=url_for('static', filename=f'images/qr_codes/{name}.png'),
        qr_code_name=name,
        templates=get_template_names(),
        final_code=None
    )


def combine_with_template(qr_code_file, template_file, name):
    """Combine the QR code with a selected template."""
    # Load template and QR code images
    template_img = Image.open(template_file).convert("RGBA")
    qr_code_img = Image.open(qr_code_file).convert("RGBA")

    # Default values for QR code size and offsets
    qr_code_size = (250, 250)  # Default size
    offset = 0  # Default vertical offset
    horizontal_offset = 0  # Default horizontal offset

    # Determine QR code size and offsets based on the selected template
    if "template1" in template_file:  # Adjust for template 1
        qr_code_size = (218, 218)
        offset = -30
    elif "template2" in template_file:  # Adjust for template 2
        qr_code_size = (405, 405)
        offset = 50
    elif "template3" in template_file:  # Adjust for template 3
        qr_code_size = (520, 520)
        offset = 90
    elif "template4" in template_file:  # Adjust for template 4
        qr_code_size = (2100, 2100)
        offset = -300
    elif "template5" in template_file:  # Adjust for template 5
        qr_code_size = (1250, 1250)
    elif "template6" in template_file:  # Adjust for template 6
        qr_code_size = (346, 346)
        offset = -125
        horizontal_offset = -3  # Adjust for template 6

    # Resize the QR code
    qr_code_img = qr_code_img.resize(qr_code_size)

    # Calculate position to center the QR code on the template
    template_width, template_height = template_img.size
    qr_code_width, qr_code_height = qr_code_img.size

    # Adjust the vertical and horizontal positions
    vertical_position = (template_height - qr_code_height) // 2 + offset
    horizontal_position = (template_width - qr_code_width) // 2 + horizontal_offset

    # Final position considering both vertical and horizontal offsets
    position = (horizontal_position, vertical_position)

    # Paste the QR code onto the template (with alpha composite for transparency)
    template_img.paste(qr_code_img, position, qr_code_img)

    # Save the combined image in the new folder
    combined_file = f'static/images/qr_codes_templates/final_{name}.png'
    template_img.save(combined_file)

    return f'qr_codes_templates/final_{name}.png'


@app.route('/finalize', methods=['POST'])
def finalize():
    qr_code_name = request.form['qr_code_name']
    selected_template = request.form['template']

    # Paths for QR code and selected template
    qr_code_path = f'static/images/qr_codes/{qr_code_name}.png'
    template_path = f'static/qr_templates/{selected_template}'

    # Generate the final QR code with the selected template
    final_code_file = combine_with_template(qr_code_path, template_path, qr_code_name)

    return render_template(
        'index.html',
        qr_code=url_for('static', filename=f'images/qr_codes/{qr_code_name}.png'),
        qr_code_name=qr_code_name,
        templates=get_template_names(),
        final_code=url_for('static', filename=f'images/{final_code_file}')
    )


if __name__ == '__main__':
    app.run()
