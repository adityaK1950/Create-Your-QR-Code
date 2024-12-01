// Handle QR Code generation
document.getElementById('qrForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const qrText = document.getElementById('qrText').value;
    const qrCodeImage = document.getElementById('qrCodeImage');
    const downloadNormalQR = document.getElementById('downloadNormalQR');

    // Generate the initial QR Code (Replace this URL with your backend QR generator if needed)
    const qrCodeURL = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(qrText)}`;
    qrCodeImage.src = qrCodeURL;
    qrCodeImage.style.display = 'block';
    downloadNormalQR.href = qrCodeURL;
    downloadNormalQR.style.display = 'inline-block';

    // Show template options
    document.querySelector('.template-options').style.display = 'flex';
});

// Apply selected template
function applyTemplate(templateName) {
    const qrCodeImage = document.getElementById('qrCodeImage').src;
    const finalQRCodeImage = document.getElementById('finalQRCodeImage');
    const downloadFinalQR = document.getElementById('downloadFinalQR');

    // Combine QR code with template (Server-side handling recommended for real projects)
    const combinedQRCodeURL = `your-backend-url/combine?template=${templateName}&qr=${encodeURIComponent(qrCodeImage)}`;
    
    // Display combined QR Code (Simulated URL for demonstration)
    finalQRCodeImage.src = combinedQRCodeURL;
    finalQRCodeImage.style.display = 'block';
    downloadFinalQR.href = combinedQRCodeURL;
    document.querySelector('.final-result').style.display = 'block';
}
