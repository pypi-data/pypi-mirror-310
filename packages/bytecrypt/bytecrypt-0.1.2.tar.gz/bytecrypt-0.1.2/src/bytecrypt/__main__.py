from bytecrypt import encrypt_bytes
from bytecrypt import decrypt_bytes
from bytecrypt import encrypt_directory
from bytecrypt import decrypt_directory
from bytecrypt import encrypt_file
from bytecrypt import decrypt_file
from bytecrypt import encrypt_string
from bytecrypt import decrypt_string
from argparse import ArgumentParser

### TODO
# list of directories or files
# e.g. -e -dir "test/directory1","testdir2" -p "test"
# e.g. -e -dir "test/secret.txt","binary.exe" -p "test"

### TODO
## recursive dir encrypt
# -r    || --recursive  (loops thru all dirs)

def init_argparse() -> ArgumentParser:
    parser = ArgumentParser(
        prog="Bytecrypt",
        description="Easy data encryption / decryption"
    )
    parser.add_argument('-e', '--encrypt', action='store_true')
    parser.add_argument('-d', '--decrypt', action='store_true')
    parser.add_argument('-f', '--file')
    parser.add_argument('-dir', '--directory')

    # TODO: directory encryption stuff
    parser.add_argument('-efn', '--encrypt-filename', action='store_true')
    parser.add_argument('-r', '--recursive', action='store_true')

    parser.add_argument('-str', '--string')
    parser.add_argument('-p', '--password', required=True)
    return parser


def process_encrypting(args):
    if (args.directory and not args.file and not args.string):
        encrypt_directory(args.directory, bytes(args.password, encoding="utf-8"))
    elif (args.file and not args.directory and not args.string):
        encrypt_file(args.file, bytes(args.password, encoding="utf-8"))
    elif (args.string and not args.directory and not args.file):
        encrypt_string(args.string, bytes(args.password, encoding="utf-8"))
    else:
        print("\nWarning: passed more than one data argument (-dir, -file, -str)")


def process_decrypting(args):
    if (args.directory and not args.file and not args.string):
        decrypt_directory(args.directory, bytes(args.password, encoding="utf-8"))
    elif (args.file and not args.directory and not args.string):
        decrypt_file(args.file, bytes(args.password, encoding="utf-8"))
    elif (args.string and not args.directory and not args.file):
        decrypt_string(args.string, bytes(args.password, encoding="utf-8"))
    else:
        print("\nWarning: passed more than one data argument (-dir, -file, -str)")


def main():
    parser = init_argparse()
    args = parser.parse_args()
    # print(args)

    if (args.encrypt and not args.decrypt):
        process_encrypting(args)
    elif (args.decrypt and not args.encrypt):
        process_decrypting(args)
    else:
        print("\nWarning: passed both encrypt and decrypt flags.")


if __name__ == "__main__":
    main()

