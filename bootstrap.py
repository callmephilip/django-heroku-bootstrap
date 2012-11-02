from subprocess import call

def main():
	print "Welcome to Django Heroku Bootstrap"
	print "**********************************"
	print "Are you running a virtual environment for this project? [Y/N] (If you are not sure, go with No)"

	virtual_env = raw_input().lower() == "y"

	if not virtual_env:
		print "Please create and activate a virtual environment for the project and come back"
		return

	call(["sudo", "pip", "install", "fabric"])
	call(["fab", "init"])


if __name__ == "__main__":
    main()