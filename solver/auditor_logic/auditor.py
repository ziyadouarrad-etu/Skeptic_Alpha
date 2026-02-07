import sympy as sp
import re

class Auditor:
    def __init__(self, proposer, skeptic, max_attempts=2):
        self.proposer = proposer
        self.skeptic = skeptic
        self.max_attempts = max_attempts

    def parse_tag(self, text, tag):
        pattern = rf"\[{tag}\](.*?)\[/{tag}\]"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def run_sympy_logic(self, code):
        """Executes SymPy code and returns (bool, message)."""
        if not code: 
            return False, "No code provided."
            
        local_scope = {}
        try:
            # Context for execution
            exec_context = {"sp": sp, "bool": bool, "float": float, "int": int}
            exec(code, exec_context, local_scope)
            
            # Check the logical result variable
            is_correct = local_scope.get("is_correct", False)
            
            # If the Skeptic returned a SymPy Relation (Eq) instead of a Bool
            if hasattr(is_correct, 'simplify'):
                # Force simplification to see if it's logically True
                is_correct = sp.simplify(is_correct) == True or is_correct == True
            
            if is_correct:
                return True, "Symbolic Match Confirmed", False
            else:
                return False, "Symbolic Mismatch (Math logic returned False)", False
                
        except Exception as e:
            # This captures actual syntax errors or runtime crashes
            return False, f"Execution Error: {str(e)}", True

    def process_query(self, query):
        attempts = 0
        feedback = ""
        history = []

        while attempts < self.max_attempts:
            # Phase 1: Propose
            solution = self.proposer.generate_solution(query, feedback)
            
            # Phase 2: Audit
            audit_result = self.skeptic.audit_solution(query, solution)
            
            # Phase 3: Verify & Parse
            code = self.parse_tag(audit_result, "SKEPTIC")
            LLM_status = "STATUS=TRUE" in audit_result.upper()
            corrections = self.parse_tag(audit_result, "CORRECTIONS") if not LLM_status else ""
            error_cat = self.parse_tag(audit_result, "ERROR_CATEGORY") if not LLM_status else ""
            problem_category = self.parse_tag(audit_result, "CATEGORY")
            affirmation = self.parse_tag(audit_result, "AFFIRMATION") if LLM_status else ""
            LLM_feedback = self.parse_tag(audit_result, "FEEDBACK")
            
            code_status, error_msg, is_sympy_error = self.run_sympy_logic(code)

            # Record Attempt
            current_attempt = {
                "attempt": attempts + 1, 
                "category": problem_category, 
                "error_category": error_cat, 
                "symbolic_passed": code_status, 
                "semantic_status": LLM_status, 
                "proposed_solution": solution, 
                "code": code, 
                "affirmation": affirmation,
                "error_msg": error_msg,
                "final_status": "PENDING",
                "full_LLM_output": audit_result,
                "corrections": corrections,
                "LLM_feedback": LLM_feedback,
                "is_sympy_error": is_sympy_error

            }
            
            # --- EXIT CONDITION: AT LEAST ONE PASS ---
            if code_status or LLM_status:
                if code_status and LLM_status:
                    current_attempt["final_status"] = "VERIFIED"
                    current_attempt["feedback"] = "Both symbolic and semantic verification passed."
                elif code_status:
                    current_attempt["final_status"] = "SYMBOLIC_ONLY_PASS"
                    current_attempt["feedback"] = f"Math verified by SymPy, but LLM flagged logic: {corrections}"
                else:
                    current_attempt["final_status"] = "SEMANTIC_ONLY_PASS"
                    current_attempt["feedback"] = f"LLM approved logic, but SymPy code failed: {error_msg}"
                
                history.append(current_attempt)
                return history

            # --- LOOP CONDITION: BOTH FAILED ---
            current_attempt["final_status"] = "BOTH_FAILURE"
            feedback = f"Both symbolic and semantic verification failed. SymPy: {error_msg}. Corrections: {corrections}"
            current_attempt["feedback"] = feedback
            
            history.append(current_attempt)
            attempts += 1
        
        # Return the last attempt details after exhausting max_attempts
        return history