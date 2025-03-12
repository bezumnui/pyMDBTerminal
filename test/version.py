from py_mdb_terminal.mdb_client import MDBClient


def test_version_mdb():
    mdb = MDBClient("/dev/tty.usbmodem01")
    mdb.start()
    sfv = mdb.get_version()
    hwv = mdb.get_hardware_info()
    print(sfv, hwv)

if __name__ == '__main__':
    test_version_mdb()