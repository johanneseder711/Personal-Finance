def get_credentials(URL):
	# define the path to the credentials file
	PATH_CREDENTIALS = '../../data/Credentials/my_credentials.txt'
	# read the file where the credentials are stored line by line
	# new credentials start with a # and the name of the credentials site
	# in the next two lines there are the username and password stored in the file

	with open(PATH_CREDENTIALS) as f:
	    for line in f:
	        if (line.startswith('#')) and (line.split()[1].lower() in URL):
	            user,pw = [next(f).split()[0],next(f).split()[0]]
	return (user,pw)