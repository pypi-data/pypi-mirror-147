import sys, getopt
# from file_upload.file_client import main
from file_client import main


def start():
    argv = sys.argv[1:]
    pi = None
    path = None
    session = None
    try:
        options, args = getopt.getopt(argv, "hs:i:p:", ["help", "session=", "id=", "path="])
    except getopt.GetoptError:
        sys.exit()
    for option, value in options:
        if option in ("-h", "--help"):
            print("-s -----token")
            print("-i -----target id")
            print("-p -----file path")
            return "help"
        if option in ("-s", "--session"):
            session = "session=" + value
        if option in ("-i", "--id"):
            pi = value
        if option in ("-p", "--path"):
            path = value
    if not all([session, pi, path]):
        return "params error"
    res = main(session, pi, path)
    print(res)


if __name__ == '__main__':
    start()

