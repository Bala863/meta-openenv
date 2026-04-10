from huggingface_hub import HfApi

api = HfApi()
info = api.whoami()
print("Name:", info.get("name"))
print("Type:", info.get("type", "unknown"))

at = info.get("accessToken", {})
print("Token role:", at.get("role", "N/A"))
print("Token name:", at.get("name", "N/A"))

fg = at.get("fineGrained", {})
if fg:
    print("Scoped:", fg.get("scoped", []))
    print("Global:", fg.get("global", []))
