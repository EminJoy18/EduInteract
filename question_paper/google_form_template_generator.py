basic_starter = [{
                "createItem": {
                    "item": {
                        "title": "Name",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False  # Short answer type
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 0
                    }
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Roll Number",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False  # Short answer type
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 1
                    }
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Class",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",  # Multiple choice question
                                    "options": [
                                        {"value": "BE COMPS A"},
                                        {"value": "BE COMPS B"}
                                    ],
                                    "shuffle": False
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 2
                    }
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Email ID",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False  # Short answer type
                                }
                            }
                        }
                    },
                    "location": {
                        "index": 3
                    }
                }
            }]


def template_generator(questions):
    for i in range(len(questions)):
        basic_starter.append({
            "createItem": {
                "item": {
                    "title": questions[i]['Question'],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",  # Multiple choice question
                                "options": [
                                    {"value": questions[i]["Options"][0]},
                                    {"value": questions[i]["Options"][1]},
                                    {"value": questions[i]["Options"][2]},
                                    {"value": questions[i]["Options"][3]}
                                ],
                                "shuffle": False
                            },
                            "grading": {
                                "correctAnswers": {
                                    "answers": [{"value": questions[i]["Answer"]}]  # Set correct answer
                                },
                                "pointValue": 1  # Points for the question
                            }
                        }
                    }
                },
                "location": {
                    "index": (4 + i)
                }
                # "answerKey": {
                #     "answers": [
                #         {
                #             "value": questions[i]["Answer"],
                #             "answerFeedback": {
                #                 "text": "Correct answer!"
                #             }
                #         }
                #     ]
                # }
            }
        })

    return basic_starter