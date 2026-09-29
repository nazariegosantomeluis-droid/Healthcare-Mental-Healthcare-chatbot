"""
Chatbot multiagente de salud con AG2 (AutoGen)
Agentes: paciente -> diagnóstico -> farmacia -> consulta
"""
import os
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager

# ---------------------------------------------------------
# Paso 0: Cargar la API key desde el archivo .env
# ---------------------------------------------------------
from Config import llm_config

# ---------------------------------------------------------
# Paso 1: Crear los agentes con roles distintos
# ---------------------------------------------------------
patient_agent = ConversableAgent(
    name="patient",
    system_message="You describe your symptoms and ask for help.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

diagnosis_agent = ConversableAgent(
    name="diagnosis",
    system_message=(
        "You analyze the patient's symptoms and list the most likely possible causes. "
        "Do not recommend medications. Always clarify this is not a definitive diagnosis. "
        "Respond in the same language as the patient."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

pharmacy_agent = ConversableAgent(
    name="pharmacy",
    system_message=(
        "Based only on the diagnosis agent's analysis, suggest common over-the-counter "
        "options and general care measures. Mention precautions and warn about allergies "
        "or interactions. Do not diagnose. Respond in the same language as the patient."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

consultation_agent = ConversableAgent(
    name="consultation",
    system_message=(
        "Based on the previous messages, decide whether the patient should see a doctor, "
        "and how urgently (emergency, within days, or not needed). Explain the warning signs "
        "that would require immediate medical attention. Respond in the same language as the patient."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# ---------------------------------------------------------
# Paso 2: Crear el GroupChat (conversación estructurada)
# ---------------------------------------------------------
groupchat = GroupChat(
    agents=[diagnosis_agent, pharmacy_agent, consultation_agent],  # El paciente solo inicia
    messages=[],
    max_round=5,  # Limita la conversación para evitar ciclos infinitos
    speaker_selection_method="round_robin",  # Cada agente habla en orden
)

# ---------------------------------------------------------
# Paso 3: Crear el GroupChatManager (coordinador)
# ---------------------------------------------------------
manager = GroupChatManager(name="manager", groupchat=groupchat, llm_config=llm_config)

# ---------------------------------------------------------
# Paso 4: Pedir síntomas e iniciar la consulta
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n🤖 Welcome to the AI Healthcare Consultation System!")
    symptoms = input("🩺 Please describe your symptoms: ")

    print("\n🩺 Diagnosing symptoms...")
    response = patient_agent.initiate_chat(
        manager,
        message=f"I am feeling {symptoms}. Can you help?",
        max_turns=1,  # El paciente envía un mensaje y el grupo responde; evita que siga hablando solo
    )