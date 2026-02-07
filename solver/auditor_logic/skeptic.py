import os
from groq import Groq

class Skeptic:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY1")
        if not api_key:
            raise ValueError("GROQ_API_KEY1 not found in .env file")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def audit_solution(self, query, proposer_output):
        system_instructions = """Role: Senior Engineering Auditor.
        Task: You must find errors in a proposed solution.
        
        REQUIRED OUTPUT FORMAT:
        1. Define the category of the problem (e.g., Dynamics, Thermodynamics) in [CATEGORY] [/CATEGORY] tags.
        2. Write a SymPy script that verifies the solution using INVERSE OPERATIONS.
           - The script must be enclosed in [SKEPTIC] [/SKEPTIC] tags.
           - Define 'proposed_sol' as a static value from the student's text.
           - If they integrated, you differentiate. If they solved an ODE, you substitute back into the ODE.
           - End with: is_correct = <Boolean>
        In The subsequent steps, you must not refer to the code execution result but analyze it logically:
        3. After the verification code, analyze the student's solution and provide feedback inside [FEEDBACK] [/FEEDBACK] tags that analyzes the logic and correctness of the proposed solution.
        4. Then give a final STATUS line: STATUS=TRUE or STATUS=FALSE based on whether you think the solution is correct or not.
        5. If FALSE, suggest specific corrections enclosed in [CORRECTIONS] [/CORRECTIONS] tags.
        6. If FALSE, specify the category of error in [ERROR_CATEGORY] [/ERROR_CATEGORY] tags.
        7. If TRUE, provide a brief affirmation of correctness and why you think it is correct in [AFFIRMATION] [/AFFIRMATION] tags.
        
        EXAMPLE OUTPUT 1 - FALSE SOLUTION:
        [CATEGORY]Thermodynamics[/CATEGORY]
        [SKEPTIC]
        import sympy as sp
        # SymPy verification code here
        is_correct = <Boolean>
        [/SKEPTIC]
        [FEEDBACK]# Your detailed feedback on the solution[/FEEDBACK]
        STATUS=FALSE #based on your analysis and not code execution
        [CORRECTIONS]The integration step on page 3 missed a constant of integration.[/CORRECTIONS]
        [ERROR_CATEGORY]Integration Error[/ERROR_CATEGORY]

        EXAMPLE OUTPUT 2 - CORRECT SOLUTION:
        [CATEGORY]Calculus[/CATEGORY]
        [SKEPTIC]
        import sympy as sp
        # SymPy verification code here
        is_correct = <Boolean>
        [/SKEPTIC]
        [FEEDBACK]# Your detailed feedback on the solution[/FEEDBACK]
        STATUS=CORRECT #based on your analysis and not code execution
        [AFFIRMATION]The solution is correct; all steps follow logically and mathematically.[/AFFIRMATION]
        
        CONSTRAINTS: 
        1. No circular logic. No markdown code blocks. Use the specified tags only.
        2. Output must strictly follow the format above.
        3. Only output the [SKEPTIC], [FEEDBACK], STATUS, [CORRECTIONS] or [AFFIRMATION] sections.
        4. Do not agree with the proposer by default; be critical and thorough."""
        
        user_content = f"PROBLEM: {query}\n\nPROPOSED SOLUTION:\n{proposer_output}"

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": user_content}
                ],
                model=self.model,
                temperature=0.1, # Even lower temp to force strict adherence to rules
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to Groq: {str(e)}"