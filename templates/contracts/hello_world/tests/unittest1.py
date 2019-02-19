import unittest, sys
from eosfactory.eosf import *

verbosity([Verbosity.INFO, Verbosity.OUT])

CONTRACT_WORKSPACE = sys.path[0] + "/../"

# Actors of the test:
MASTER = None
HOST = None
ALICE = None
BOB = None
CAROL = None

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)

    @classmethod
    def setUpClass(cls):
        SCENARIO('''
        Execute simple actions.
        ''')
        reset()
        create_master_account("MASTER")

        COMMENT('''
        Build and deploy the contract:
        ''')
        create_account("HOST", MASTER)
        contract = Contract(HOST, CONTRACT_WORKSPACE)
        contract.build(force=False)
        contract.deploy()

        COMMENT('''
        Create test accounts:
        ''')
        create_account("ALICE", MASTER)
        create_account("CAROL", MASTER)
        create_account("BOB", MASTER)

    def setUp(self):
        pass

    def test_01(self):
        COMMENT('''
        Test an action for Alice:
        ''')
        HOST.push_action(
            "hi", {"user":ALICE}, permission=(ALICE, Permission.ACTIVE))

        COMMENT('''
        Test an action for Carol:
        ''')
        HOST.push_action(
            "hi", {"user":CAROL}, permission=(CAROL, Permission.ACTIVE))

        COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        with self.assertRaises(MissingRequiredAuthorityError):
            HOST.push_action(
                "hi", {"user":CAROL}, permission=(BOB, Permission.ACTIVE))

    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
