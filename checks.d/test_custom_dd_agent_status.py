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
            {
                "max": 0,
                "host_name": "test-server",
                "alerts": [],
            },
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
            {
                "max": 1,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 1,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": ["cpu last warning"]
                    },
                ],
            },
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
            {
                "max": 1,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 1,
                        "item": "disk",
                        "identifier": "disk:dddddddddddddddd",
                        "details": ["disk last warning"]
                    },
                ],
            },
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
            {
                "max": 1,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 1,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": ["cpu last warning"]
                    },
                    {
                        "level": 1,
                        "item": "disk",
                        "identifier": "disk:dddddddddddddddd",
                        "details": ["disk last warning"]
                    },
                ],
            },
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
            {
                "max": 1,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 1,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": ["cpu last warning"]
                    },
                    {
                        "level": 1,
                        "item": "disk",
                        "identifier": "disk:dddddddddddddddd",
                        "details":  ["disk last warning 1", "disk last warning 2"]
                    },
                ],
            },
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
            {
                "max": 2,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 2,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": "cpu last error"
                    },
                ],
            },
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
            {
                "max": 2,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 2,
                        "item": "disk",
                        "identifier": "disk:dddddddddddddddd",
                        "details": "disk last error"
                    },
                ],
            },
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
            {
                "max": 2,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 1,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": ["cpu last warning"]
                    },
                    {
                        "level": 2,
                        "item": "disk",
                        "identifier": "disk:dddddddddddddddd",
                        "details": "disk last error"
                    },
                ],
            },
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
            {
                "max": 2,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 2,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": "cpu last error"
                    },
                    {
                        "level": 1,
                        "item": "cpu",
                        "identifier": "cpu",
                        "details": ["cpu last warning"]
                    },
                ],
            },
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
            {
                "max": 3,
                "host_name": "test-server",
                "alerts": [
                    {
                        "level": 3,
                        "item": "",
                        "identifier": "",
                        "details": "KeyError('LastWarnings')"
                    },
                ]
            },
        )

    # def test_get_items(self):
    #     """ test get items """
    #     self.assertEqual(
    #         CustomStatusCheck().get_items({
    #             "warnings": [
    #                 {
    #                     "item": "cpu",
    #                     "identifier": "cpu",
    #                     "last_warnings": ["cpu last warning"]
    #                 },
    #                 {
    #                     "item": "disk",
    #                     "identifier": "disk:dddddddddddddddd",
    #                     "last_warnings": ["disk last warning"]
    #                 },
    #             ]
    #         }),
    #         [
    #             "cpu", "disk"
    #         ]
    #     )
