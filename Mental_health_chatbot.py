"""
Ejercicio: Chatbot de salud mental con AG2 (AutoGen)
Agentes: paciente -> análisis de emociones -> recomendaciones
"""
import os
from dotenv import load_dotenv
from autogen import ConversableAgent, GroupChat, GroupChatManager

# ---------------------------------------------------------
# Configuración del LLM
# ---------------------------------------------------------
from Config import llm_config

# ---------------------------------------------------------
# Crear los agentes con roles distintos
# ---------------------------------------------------------
patient_agent = ConversableAgent(
    name="patient",
    system_message="You describe your emotions and mental health concerns.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

emotion_analysis_agent = ConversableAgent(
    name="emotion_analysis",
    system_message=(
        "You analyze the user's emotions based on their input. "
        "Do not provide treatment or self-care advice. "
        "Instead, just summarize the dominant emotions they may be experiencing. "
        "Respond in the same language as the user."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

therapy_recommendation_agent = ConversableAgent(
    name="therapy_recommendation",
    system_message=(
        "You suggest relaxation techniques and self-care methods "
        "only based on the analysis from the Emotion Analysis Agent. "
        "Do not analyze emotions, just give recommendations based on the prior response. "
        "Gently encourage talking to a mental health professional or someone they trust. "
        "If the user mentions any risk to their safety, prioritize recommending they contact "
        "local emergency services or a crisis line right away. "
        "Respond in the same language as the user."
    ),
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# ---------------------------------------------------------
# Crear el GroupChat
# ---------------------------------------------------------
groupchat = GroupChat(
    agents=[emotion_analysis_agent, therapy_recommendation_agent],
    messages=[],
    max_round=3,  # Mensaje inicial + análisis + recomendaciones
    speaker_selection_method="round_robin",
)

# ---------------------------------------------------------
# Crear el GroupChatManager
# ---------------------------------------------------------
manager = GroupChatManager(name="manager", groupchat=groupchat, llm_config=llm_config)


# ---------------------------------------------------------
# Función que inicia el chatbot
# ---------------------------------------------------------
def start_mental_health_chat():
    """Runs a chatbot for mental health support with distinct agent roles."""
    print("\nWelcome to the AI Mental Health Chatbot!")
    user_feelings = input("How are you feeling today? ")

    print("\nAnalyzing emotions...")
    response = patient_agent.initiate_chat(
        manager,
        message=f"I have been feeling {user_feelings}. Can you help?",
        max_turns=1,
    )

    # Si por alguna razón no hubo respuesta, se llama directamente al agente de terapia
    if not response or not response.chat_history:
        therapy_recommendation_agent.initiate_chat(
            manager,
            message="Based on the user's emotions, please provide therapy recommendations.",
            max_turns=1,
        )


if __name__ == "__main__":
    start_mental_health_chat()