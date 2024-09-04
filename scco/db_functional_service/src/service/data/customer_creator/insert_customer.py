request_simple = {
    "request_name": "insert_customer",
    "request_data": {
        "customer_id": "customer_3",
        "contact_info": ["telegram", "whatsup"],
        "company_name": "MIPT",
        "black_list": [
            "forbidden1",
            "forbidden2",
        ],
        "tags": [
            "backend",
            "java",
        ],
        "white_list": [
            "backend",
            "java",
            "spring",
            "kotlin"
        ],
        "specific_features": [
            "Specific feature 1",
            "Specific feature 2",
        ],
        "services": [
            {
                "service_name": "(1) First service",
                "service_desc": "First service description."
            },
            {
                "service_name": "(2) Second service",
                "service_desc": "Second service description."
            },
            {
                "service_name": "(3) Third service",
                "service_desc": "Third service description."
            }
        ]
    }
}

################################################################################

answer_simple = None
