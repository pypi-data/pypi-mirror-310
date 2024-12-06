import mrlou_modules.Certificate_Utils.cert_utils as cu

# Example usage:
input_pem_file = r'C:\Users\LDESCAMP\Downloads\eosbc.qbetest.com\Trusted_Root_Certificates.pem'
output_dir = r'C:\Users\LDESCAMP\Downloads\certificates'

# Call the function to extract and save certificates
cu.extract_and_save_certificates(input_pem_file, output_dir)
