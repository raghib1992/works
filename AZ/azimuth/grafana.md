# Creating grafana dashboards

### mrndevops kubernetes clusters monitoring is achieved using prometheus-grafana integration. Prometheus collects the metrics from the clusters and these metrics can be visualised using grafana dashboards.

### Creating a Grafana dashboard to monitor pod status involves several steps, from configuring data sources to designing visualizations. Here as an example, steps to create grafana dashboard to monitor failing pods with Imagepullbackofff is shown.

### Step 1: Set Up Grafana
- Install Grafana on your preferred platform by following the installation guide on the official Grafana website.

### Step 2: Configure Prometheus Data Source
- Log in to your Grafana instance.
- Navigate to "Configuration" > "Data Sources".
- Click "Add data source."
- Choose "Prometheus" as the data source type.
- Configure the Prometheus endpoint details (URL).

### Step 3: Create a Dashboard
- Click on the "+" icon on the left sidebar and choose "Dashboard."
- In the "Add new panel" section, select "Add Panel."
- In the new panel, click on "Panel Title" and select "Edit."
- In the "Query" section, choose the Prometheus data source you configured earlier.
- Click on the gear icon and select the variables option on the left. Click on "New" to create a new variable. In this instance variable namespace is created using `label_values(kube_pod_container_info,namespace)` Query.
- Write a PromQL query to retrieve pod status metrics. For example: 
```sh
kube_pod_container_status_waiting_reason{reason=~"ImagePullBackOff",namespace=~"$namespace"} > 0
```
- Customize visualization options such as visualization type (e.g., Table, Stat, Singlestat, etc.), refresh interval, and panel title.

### Step 4: Add More Panels
- To add more panels for different pod status metrics, click "Add Panel" again.
- Repeat the process of configuring data sources, queries, and visualization options for each panel.

### Step 5: Organize Panels on the Dashboard
- Arrange the panels on the dashboard by dragging and dropping them into the desired positions.
- Resize panels as needed to create an organized layout.

### Step 6: Customize the Dashboard
- Click on the gear icon at the top of the dashboard to access the dashboard settings.
- Here, you can customize the dashboard title, time range controls, and other settings to your preference.

### Step 7: Save and Share the Dashboard
- Click the "Save" button in the top menu to save the dashboard.