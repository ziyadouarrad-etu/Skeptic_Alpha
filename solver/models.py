from django.db import models

class Proof(models.Model):
    status = models.CharField(max_length=20)     # e.g., 'verified', 'failed'
    query = models.TextField()                   # What the user asked
    solution_markdown = models.TextField()       # The AI's final explanation
    skeptic_code = models.TextField()            # The Python code that proved it
    category = models.CharField(max_length=100, default="Uncategorized")  # The problem category (e.g., Calculus, Linear Algebra)
    attempts_count = models.IntegerField()       # How many retries it took
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solution for: {self.query[:30]}..."

class EngineeringProblem(models.Model):
    prompt = models.TextField()
    category = models.CharField(max_length=100, default="General")
    final_solution = models.TextField()
    verification_status = models.CharField(max_length=50)
    total_attempts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Engineering Problem: {self.prompt[:30]}..."

class VerificationAttempt(models.Model):
    problem = models.ForeignKey(EngineeringProblem, on_delete=models.CASCADE, related_name='attempts')

    sympy_code = models.TextField(default="")
    is_sympy_error = models.BooleanField(default=False)
    code_status = models.BooleanField(default=False)
    code_error_message = models.TextField(default="")

    LLM_status = models.TextField(default="")
    LLM_feedback = models.TextField(default="")
    LLM_affirmation = models.TextField(default="")
    LLM_corrections = models.TextField(default="")
    full_LLM_output = models.TextField(default="")
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attempt for Problem ID: {self.problem.id} at {self.created_at}"