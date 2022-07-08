""" test CustomStatusCheck """
from unittest import TestCase

from custom_dd_agent_status import CustomStatusCheck


class TestCustomStatusCheck(TestCase):
    """ TestCustomStatusCheck """
    def test_put_summary_ok(self):
        """ test returns ok """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
            ],
        )

    def test_put_summary_warning1(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                "LastWarnings": ["cpu last warning"],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["cpu last warning"],
                    }
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
            ]
        )

    def test_put_summary_warning2(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                "LastWarnings": ["disk last warning"],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["disk last warning"],
                    }
                },
            ]
        )

    def test_put_summary_warning3(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                "LastWarnings": ["cpu last warning"],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                "LastWarnings": ["disk last warning"],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["cpu last warning"],
                    }
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["disk last warning"],
                    }
                },
            ]
        )

    def test_put_summary_warning4(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                "LastWarnings": ["cpu last warning"],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 2,
                                "LastWarnings": ["disk last warning 1", "disk last warning 2"],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["cpu last warning"],
                    }
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["disk last warning 1", "disk last warning 2"],
                    }
                },
            ]
        )

    def test_put_summary_error1(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 1,
                                "LastError": "cpu last error",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 2,
                    "details": {
                        "error": "cpu last error",
                    }
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
            ]
        )

    def test_put_summary_error2(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 1,
                                "LastError": "disk last error",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 2,
                    "details": {
                        "error": "disk last error",
                    }
                },
            ]
        )

    def test_put_summary_error3(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                "LastWarnings": ["cpu last warning"],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 1,
                                "LastError": "disk last error",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 1,
                    "details": {
                        "warnings": ["cpu last warning"],
                    }
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 2,
                    "details": {
                        "error": "disk last error",
                    }
                },
            ]
        )

    def test_put_summary_error4(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 2,
                                "LastError": "cpu last error",
                                "TotalWarnings": 1,
                                "LastWarnings": ["cpu last warning"],
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "name": "cpu",
                    "identifier": "cpu",
                    "host_name": "test-server",
                    "status": 2,
                    "details": {
                        "error": "cpu last error",
                        "warnings": ["cpu last warning"],
                    }
                },
                {
                    "name": "disk",
                    "identifier": "disk:dddddddddddddddd",
                    "host_name": "test-server",
                    "status": 0,
                    "details": {},
                },
            ]
        )

    def test_put_summary_exception(self):
        """ test returns exception """
        self.assertEqual(
            CustomStatusCheck().put_summary({
                "apmStats": {
                    "config": {
                        "Hostname": "test-server"
                    }
                },
                "runnerStats": {
                    "Checks": {
                        "cpu": {
                            "cpu": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 1,
                                # "LastWarnings": [],  # caused exception
                            }
                        },
                        "disk": {
                            "disk:dddddddddddddddd": {
                                "TotalErrors": 0,
                                "LastError": "",
                                "TotalWarnings": 0,
                                "LastWarnings": [],
                            }
                        },
                    }
                }
            }),
            [
                {
                    "host_name": "test-server",
                    "status": 3,
                    "details": {
                        "exception": "KeyError('LastWarnings')",
                    }
                }
            ]
        )
