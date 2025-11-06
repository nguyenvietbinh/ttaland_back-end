import aws_cdk as cdk
from backend.backend_stack import BackendStack

app = cdk.App()
BackendStack(app, "BackendStack-Dev", stage="dev")
BackendStack(app, "BackendStack-Prod", stage="prod")
app.synth()