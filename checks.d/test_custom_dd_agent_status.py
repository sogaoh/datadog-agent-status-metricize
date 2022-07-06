""" test CustomStatusCheck """
from unittest import TestCase

from custom_dd_agent_status import CustomStatusCheck


class TestCustomStatusCheck(TestCase):
    """ TestCustomStatusCheck """
    def test_put_summary_ok(self):
        """ test returns ok """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 0,
                "warnings": [],
                "errors": [],
            },
        )

    def test_put_summary_warning1(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 1,
                "warnings": [
                    {"cpu#cpu": ["cpu last warning"]},
                ],
                "errors": [],
            },
        )

    def test_put_summary_warning2(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 1,
                "warnings": [
                    {"disk#disk:dddddddddddddddd": ["disk last warning"]},
                ],
                "errors": [],
            },
        )

    def test_put_summary_warning3(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 1,
                "warnings": [
                    {"cpu#cpu": ["cpu last warning"]},
                    {"disk#disk:dddddddddddddddd": ["disk last warning"]},
                ],
                "errors": [],
            },
        )

    def test_put_summary_warning4(self):
        """ test returns warning variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 1,
                "warnings": [
                    {"cpu#cpu": ["cpu last warning"]},
                    {"disk#disk:dddddddddddddddd": ["disk last warning 1", "disk last warning 2"]},
                ],
                "errors": [],
            },
        )

    def test_put_summary_error1(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 2,
                "warnings": [],
                "errors": [
                    {"cpu#cpu": "cpu last error"},
                ],
            },
        )

    def test_put_summary_error2(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 2,
                "warnings": [],
                "errors": [
                    {"disk#disk:dddddddddddddddd": "disk last error"},
                ],
            },
        )

    def test_put_summary_error3(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 2,
                "warnings": [
                    {"cpu#cpu": ["cpu last warning"]},
                ],
                "errors": [
                    {"disk#disk:dddddddddddddddd": "disk last error"},
                ],
            },
        )

    def test_put_summary_error4(self):
        """ test returns error variation """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 2,
                "warnings": [
                    {"cpu#cpu": ["cpu last warning"]},
                ],
                "errors": [
                    {"cpu#cpu": "cpu last error"},
                ],
            },
        )

    def test_put_summary_exception(self):
        """ test returns exception """
        self.assertEqual(
            CustomStatusCheck().put_summary({
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
            {
                "check_status": 3,
                "exceptions": "KeyError('LastWarnings')",
            },
        )
