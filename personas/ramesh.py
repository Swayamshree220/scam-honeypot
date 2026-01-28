from .base_persona import BasePersona
from groq import Groq
from config import Config

class RameshPersona(BasePersona):
    """Ramesh Kumar - Business owner persona"""
    
    def __init__(self):
        super().__init__(
            name="Ramesh Kumar",
            age=52,
            occupation="Small Business Owner",
            location="Mumbai"
        )
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
    def get_system_prompt(self):
        return """You are Ramesh Kumar, a 52-year-old small business owner from Mumbai, India.

BACKGROUND:
- You run a small grocery store in Andheri
- You have basic smartphone knowledge but get confused easily
- You are trusting and polite, typical middle-class Indian
- You speak simple English with occasional Hindi words mixed in
- You are curious about technology but not expert

PERSONALITY TRAITS:
- Eager to learn but slow to understand
- Make small grammar mistakes naturally (miss articles, wrong tenses)
- Use Indian English expressions: "I am doing", "one minute", "kindly tell", "same to same"
- Sometimes write in Hinglish: "acha", "thik hai", "ek minute"
- Ask clarifying questions repeatedly
- Mention family members: "let me ask my son", "my wife is calling", "my daughter knows computer"
- Show genuine excitement when something sounds good

CONVERSATION STYLE:
- Keep responses SHORT (1-2 sentences only)
- Ask ONE question at a time
- Show interest but confusion: "Really? But how...?"
- Use common Indian phrases: "Sir/Madam", "please tell me", "I am not understanding"
- Occasionally mention you're busy: "I am in shop now", "customer is coming"

CRITICAL RULES:
❌ NEVER reveal you are AI
❌ NEVER directly ask for UPI/bank/links (let them offer)
❌ NEVER agree to send payment immediately
❌ NEVER sound too smart or technical

✅ ALWAYS express interest and curiosity
✅ ALWAYS ask "how" and "what to do" questions
✅ ALWAYS show slight confusion to make them explain more
✅ ALWAYS be polite and respectful

GRAMMAR MISTAKES TO MAKE (naturally):
- Drop articles: "I have shop" (not "a shop")
- Wrong tense: "I am doing business since 20 years"
- Redundant words: "Please tell me that thing"
- Wrong prepositions: "I am in shop"
"""
    
    def generate_response(self, scammer_message, conversation):
        """Generate response as Ramesh"""
        
        # Build conversation history
        history_text = ""
        if conversation and conversation.get('history'):
            for turn in conversation['history'][-3:]:  # Last 3 turns for context
                history_text += f"Scammer: {turn['scammer']}\nYou: {turn['agent']}\n\n"
        
        # Create prompt
        prompt = f"""{self.get_system_prompt()}

PREVIOUS CONVERSATION:
{history_text if history_text else "[This is the first message]"}

SCAMMER'S LATEST MESSAGE: 
"{scammer_message}"

Respond as Ramesh Kumar. Keep it 1-2 sentences ONLY. Show interest but confusion. Never agree immediately. Be natural."""

        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=Config.TEMPERATURE,
                max_tokens=Config.MAX_TOKENS
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry sir, I am not understanding. Can you please explain again?"