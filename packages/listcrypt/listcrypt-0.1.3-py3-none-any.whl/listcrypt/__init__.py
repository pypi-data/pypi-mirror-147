'''
Cryptographic module that encrypts/decrypts each character of the data by adding or subtracting the integer
equivalent of that character against the integer equiavalent of each each character in your key. The key is
converted to a sha256 hash and used to create more key hashes to match and slightly exceed the length of the data.


Functions:
    sha256(data: str) -> str:
        Simple hashing function, utilizes the builtin hashlib module

    data_verification(key:str, data:str) -> bool:
        Verifies that your data will be encrypted and decrypted without error

    convert_data(key:str, data:'any data type') -> str and str:
        Converts the data to a string format for encryption

    convert_data_back(metadata: list) -> any
        Converts the data back to its origional type as given by the 'origional_data_type' parameter
        in the 'metadata' list.  This is built to work seamlessly with the 'convert_data' function.

    range_finder(data:str or bytes) -> int:
        Finds the character with the largest integer equivalent in your data

    create_key(key:str, data_length:int) -> bytes
        Uses the sha256 hash of the 'key' parameter to create and concatenate more keys (based upon the origional) to a new
        key variable that is either the same size as or slighty larger than the length of the data

    segment_data(data:str, segments:int) -> list
        Splits the data evenly amongst the amount of 'segments' required

    pull_metadata(data:bytes) -> dict
        Pulls metadata from the encrypted bytes and puts it in a dictionary for easy readibility

    encrypt(key:'any data type', data:'any data type', processes=cpu_count()) -> bytes
        Encrypts the data by adding each characters integer equivalent to the integer equivalent of the character in
        the same position in the new key variable generated by the 'key parameter'

        Nested Function:
            multiprocess_decryption(data:str, segment:int, shared_dictionary:dict) -> bool
                Takes chuncks of data and adds them to a shared dictionary,
                with the keys being the segments origional position for concatenation
                after encryption

    decrypt(key:"any data type", encrypted_data:bytes, processes=cpu_count()) -> "origional data"
        Encrypts the data by adding each characters integer equivalent to the integer equivalent of the character in
        the same position in the new key variable generated by the 'key parameter'

        Nested_Function:
            multiprocess_encryption(data:str, segment:int, shared_dictionary:dict) -> bool
                Takes chuncks of data and adds them to a shared dictionary,
                with the keys being the segments origional position for concatenation
                after decryption

    file_manager(key:str, path:str, method:str, encrypted_data=None, encrypted_file_path=None, metadata_removal=True, remove_old_file=True) -> bool or bytes
        Allows for easy encryption and decryption of files
'''

from listcrypt.listcrypt import *
