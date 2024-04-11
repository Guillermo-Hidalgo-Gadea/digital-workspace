import ftplib, os, toml

# read the configuration file
config = toml.load('config.toml')
server = config['server']
username = config['username']
password = config['password']
directory = config['directory']
source = config['source']

ftp = ftplib.FTP(server)
ftp.login(username, password)
ftp.cwd(directory)

# walk the directory and upload the files
for root, dirs, files in os.walk(source):
    print('Uploading files to: ', root)
    for file in files:
        # construct the full path
        full_path = os.path.join(root, file)
        # construct the destination path
        dest_path = os.path.join(directory, os.path.relpath(full_path, source))
        # create the directory if it doesn't exist
        try:
            ftp.mkd(dest_path)
        except ftplib.error_perm:
            pass  # ignore the error if the file already exists
        # delete the file if it exists
        try:
            ftp.delete(dest_path)
        except ftplib.error_perm:
            pass  # ignore the error if the file doesn't exist
        # open the file and upload it
        with open(full_path, 'rb') as f:
            ftp.storbinary('STOR ' + dest_path, f)
