import csv
import os
import json
from kubernetes import client, config
from datetime import datetime

def parse_json_string(json_string, field_name):
    try:
        # Try parsing the JSON string directly
        parsed_json = json.loads(json_string)

        if not isinstance(parsed_json, list):
            parsed_json = [parsed_json]

        return parsed_json
    except json.JSONDecodeError as e:
        # Attempt to fix the JSON string if parsing fails
        try:
            parsed_json = json.loads(json_string.replace("'", "\"").replace("None", "null"))
            if not isinstance(parsed_json, list):
                parsed_json = [parsed_json]
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON string for {field_name}: {e}")
            return None

def flatten_subjects(subjects, namespace):
    if not subjects:
        return [""] * 5

    subject = subjects[0]
    return [
        subject.get("apiGroup", ""),
        subject.get("kind", ""),
        subject.get("name", ""),
        namespace,
        subject.get("organization", "")
    ]

def flatten_role_ref(role_ref):
    if not role_ref:
        return [""] * 2

    return [
        role_ref.get("apiGroup", ""),
        role_ref.get("kind", ""),
    ]

def create_unique_users_set(role_bindings_list):
    unique_users_set = set()
    for row in role_bindings_list:
        user_mail = row.get("user_mail")
        user_name = row.get("name")
        if user_mail and user_name and row.get("kind", "") != "ServiceAccount":
            unique_users_set.add((user_name, user_mail))
    return unique_users_set

def get_user_roles_bindings(cluster, ignored_namespaces):
    try:
        print(f"Switching to {cluster} cluster")
        config.load_kube_config(context=cluster)
        v1 = client.CoreV1Api()
        rbac_api = client.RbacAuthorizationV1Api()

        namespaces = [namespace.metadata.name for namespace in v1.list_namespace().items if namespace.metadata.name not in ignored_namespaces]
        role_bindings_list = []

        for namespace in namespaces:
            print(f"Processing namespace: {namespace}")

            # Fetch namespace details
            namespace_details = v1.read_namespace(namespace)
            namespace_labels = namespace_details.metadata.labels or {}
            organization = namespace_labels.get("organization", "")

            role_bindings = rbac_api.list_namespaced_role_binding(namespace)

            for role_binding in role_bindings.items:
                subjects_str = json.dumps([subject.to_dict() for subject in role_binding.subjects])
                subjects = parse_json_string(subjects_str, "subjects")
                if subjects is None:
                    print(f"Problematic subjects JSON string: {subjects_str}")
                    continue

                role_ref = role_binding.role_ref.to_dict()

                role_binding_data = {
                    "name": role_binding.metadata.name,
                    "creation_timestamp": role_binding.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    **dict(zip(["subject_api_group", "kind", "user_mail", "namespace","organization"], flatten_subjects(subjects, namespace))),
                    **dict(zip(["role_ref_api_group", "role_ref_kind"], flatten_role_ref(role_ref))),
                    "organization": organization
                }

                role_bindings_list.append(role_binding_data)

        return role_bindings_list

    except Exception as e:
        print(f"Error in get_user_roles_bindings: {e}")
        return []

def write_to_csv(data, filename, output_folder):
    try:
        if data:
            csv_file_path = os.path.join(output_folder, filename)

            with open(csv_file_path, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                header = ["name", "creation_timestamp", "user_mail", "namespace", "role_ref_api_group", "role_ref_kind", "organization"]
                writer.writerow(header)

                for row in data:
                    writer.writerow([
                        row.get("name", ""),
                        row.get("creation_timestamp", ""),
                        row.get("user_mail", ""),
                        row.get("namespace", ""),
                        row.get("role_ref_api_group", ""),
                        row.get("role_ref_kind", ""),
                        row.get("organization", "")
                    ])

            print(f"Data written to CSV file: {csv_file_path}")

    except Exception as e:
        print(f"Error in write_to_csv: {e}")

def write_unique_users_to_csv(unique_users_set, cluster, folder_path):
    try:
        if unique_users_set:
            csv_file_path = os.path.join(folder_path, f"unique_users_{cluster}.csv")

            with open(csv_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)

                header = ["name", "user_email"]
                writer.writerow(header)

                for user_name, user_email in unique_users_set:
                    writer.writerow([user_name, user_email])

            print(f"Unique users written to CSV file: {csv_file_path}")

    except Exception as e:
        print(f"Error in write_unique_users_to_csv: {e}")

if __name__ == "__main__":
    current_date_folder = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(current_date_folder, exist_ok=True)
    unique_users_set = set()
    clusters = ["ai-ops-brown@kubernetes", "ai-ops-bronze@kubernetes"]
    ignored_namespaces = ["kube-public", "kube-system"]

    for cluster in clusters:
        output_folder = os.path.join("/users/knvf512/Documents/csv", current_date_folder, cluster)
        os.makedirs(output_folder, exist_ok=True)
        role_bindings_csv_file = f"role_bindings_{cluster}.csv"
        role_bindings = get_user_roles_bindings(cluster, ignored_namespaces)
        unique_users_set.update(create_unique_users_set(role_bindings))
        write_to_csv(role_bindings, role_bindings_csv_file, output_folder)
        write_unique_users_to_csv(unique_users_set, cluster, output_folder)
