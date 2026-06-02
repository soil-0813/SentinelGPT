from app.data_sources.log_loader import load_all_logs

logs = load_all_logs()

print("\n========== TEST RESULTS ==========")
print(f"Total records loaded: {len(logs)}")

windows_count = 0
firewall_count = 0
ids_count = 0

for log in logs:

    if "username" in log:
        windows_count += 1

    elif "destination_ip" in log:
        firewall_count += 1

    elif "alert_type" in log:
        ids_count += 1

print("\nVerification:")
print(f"Windows Logs : {windows_count}")
print(f"Firewall Logs: {firewall_count}")
print(f"IDS Alerts   : {ids_count}")