from src.deployment.app import App

app = App()

print("\n===== TEXT =====")
print(app.ask("Explain credit underwriting"))

print("\n===== IMAGE =====")
print(app.ask_image("customer process"))

print("\n===== SQL =====")
print(app.ask_sql("Show all users"))

print(app.feedback("what is underwriting", "good answer"))