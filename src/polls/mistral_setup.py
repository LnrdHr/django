from mistralai import Mistral
MISTRAL_API_KEY = "hG0ndtsEvV0ZtAau7ll73J0h2giSBBv3"

def get_client():
    return Mistral(api_key=MISTRAL_API_KEY)

def create_agent():
    #agent creation happens only if the session is not already created or is expired

    mistral_client = get_client()
    global mistral_agent
    mistral_agent = mistral_client.beta.agents.create(
    model="mistral-medium-latest",
    description="A simple Agent with persistent state.",
    name="Simple Agent"
    )
    return mistral_agent

def get_agent():
    return mistral_agent