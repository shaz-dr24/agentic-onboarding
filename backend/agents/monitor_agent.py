def monitor(results):
    for r in results:
        if r["status"] == "failed":
            return "failure"
    return "success"