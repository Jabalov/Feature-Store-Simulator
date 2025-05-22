import requests

API_BASE = "http://localhost:8000"

feature_groups = [
    {
        "name": "customer_profile_features",
        "description": "Static customer information like gender, tenure, etc.",
        "owner": "ml_team"
    },
    {
        "name": "service_subscription_features",
        "description": "Details about internet, phone, and other subscriptions.",
        "owner": "ml_team"
    },
    {
        "name": "payment_behavior_features",
        "description": "Billing and payment related info.",
        "owner": "finance_team"
    },
    {
        "name": "churn_label",
        "description": "Target churn variable.",
        "owner": "ml_team"
    }
]

# ---- 2. Define Features ----
features = [
    # customer_profile_features
    {
        "name": "tenure_months",
        "feature_group_name": "customer_profile_features",
        "data_type": "int",
        "description": "Customer tenure in months.",
        "transformation": "SELECT tenure FROM telco",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 90
    },
    {
        "name": "customer_gender",
        "feature_group_name": "customer_profile_features",
        "data_type": "string",
        "description": "Gender of customer.",
        "transformation": "SELECT gender FROM telco",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 90
    },
    # service_subscription_features
    {
        "name": "has_fiber_optic",
        "feature_group_name": "service_subscription_features",
        "data_type": "boolean",
        "description": "1 if customer uses fiber optic internet, else 0.",
        "transformation": "CASE WHEN InternetService = 'Fiber optic' THEN 1 ELSE 0 END",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 60
    },
    {
        "name": "uses_phone_service",
        "feature_group_name": "service_subscription_features",
        "data_type": "boolean",
        "description": "1 if customer uses phone service.",
        "transformation": "CASE WHEN PhoneService = 'Yes' THEN 1 ELSE 0 END",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 60
    },
    # payment_behavior_features
    {
        "name": "monthly_charges",
        "feature_group_name": "payment_behavior_features",
        "data_type": "float",
        "description": "Monthly charges for the customer.",
        "transformation": "SELECT MonthlyCharges FROM telco",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 30
    },
    {
        "name": "total_charges",
        "feature_group_name": "payment_behavior_features",
        "data_type": "float",
        "description": "Total charges to date for the customer.",
        "transformation": "SELECT TotalCharges FROM telco",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 30
    },
    # churn_label
    {
        "name": "is_churned",
        "feature_group_name": "churn_label",
        "data_type": "int",
        "description": "1 if customer churned, 0 otherwise.",
        "transformation": "CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END",
        "source_table": "telco",
        "version": 1,
        "ttl_days": 90
    }
]


group_name_to_id = {}

for group in feature_groups:
    response = requests.post(f"{API_BASE}/feature-group", json=group)
    data = response.json()
    group_name_to_id[group["name"]] = data["id"]
    print(f"[+] Created Feature Group: {group['name']} (ID: {data['id']})")

# Register features
for feature in features:
    feature_payload = {
        "name": feature["name"],
        "feature_group_id": group_name_to_id[feature["feature_group_name"]],
        "data_type": feature["data_type"],
        "description": feature["description"],
        "transformation": feature["transformation"],
        "source_table": feature["source_table"],
        "version": feature["version"],
        "ttl_days": feature["ttl_days"]
    }
    response = requests.post(f"{API_BASE}/feature", json=feature_payload)
    print(f"[+] Created Feature: {feature['name']} (status: {response.status_code})")
