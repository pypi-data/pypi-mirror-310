import argparse
from getmyqr.generator import generate_qr_code

def main():
    parser = argparse.ArgumentParser(description="Generate a QR code from data.")
    parser.add_argument("data", type=str, help="Data to encode in the QR code.")
    parser.add_argument("--output", type=str, default="qrcode.png", help="Output file name (default is 'qrcode.png').")
    parser.add_argument("--size", type=str, default="300x300", help="Size of the QR code image (default is '300x300').")
    parser.add_argument("--quality", type=str, default="H", choices=["L", "M", "Q", "H"], help="Error correction level (default is 'H').")

    args = parser.parse_args()

    output_file = generate_qr_code(args.data, args.output, args.size, args.quality)
    
    if "Error" not in output_file:
        print(f"QR code successfully saved to : {output_file}")
    else:
        print(output_file)

if __name__ == "__main__":
    main()
