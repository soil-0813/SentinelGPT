from app.data_sources.log_loader import load_all_logs

logs = load_all_logs()

print(logs)
print(len(logs))