import mrlou_modules.Certificate_Utils.cert_utils as cu

# Example usage:
input_pem_file = r'C:\Users\LDESCAMP\Downloads\Microsoft Azure RSA TLS Issuing CA 03 - xsign.crt'
output_dir = r'C:\Users\LDESCAMP\Downloads\root_certificates'


cu.convert_cer_to_pem(input_pem_file, output_dir)