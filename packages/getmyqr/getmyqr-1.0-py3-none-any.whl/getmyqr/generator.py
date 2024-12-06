import requests

def generate_qr_code(data, output_file="qrcode.png", size="300x300", quality="H"):
    api_url = "https://api.qrserver.com/v1/create-qr-code/"
    
    params = {
        "data": data,
        "size": size,
        "ecc": quality
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        with open(output_file, "wb") as file:
            file.write(response.content)
        
        return output_file
    except requests.exceptions.RequestException as e:
        return f"Error generating QR code: {e}"
